from __future__ import annotations

import os
import re
import sys
import logging
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from datetime import datetime
from griffe.dataclasses import Docstring
from griffe.docstrings.parsers import Parser, parse
from inspect import getfullargspec, signature, Signature
from pathlib import Path
from typing import Type, Any, NamedTuple, TypeVar, Optional, Match
from textwrap import wrap

from .exceptions import (
    CLIException,
    CLIParserException,
    CLIRuntimeException,
    CLIUserException,
)

try:
    from zenith import zml, zml_escape

    ZENITH_INSTALLED = True

except ImportError as exc:
    ZENITH_INSTALLED = False

logging.getLogger("griffe").setLevel(logging.ERROR)

EMPTY = object()
TERMINAL_WIDTH = 120

try:
    TERMINAL_WIDTH = min(TERMINAL_WIDTH, os.get_terminal_size()[0])
except OSError as exc:
    if exc.errno != 25:
        raise

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
INDENT = " " * 2


def _is_optional(annotation: object) -> bool:
    """Determines whether an annotation is optional.

    This is rudimentary, but should be fine for our purposes.
    """

    return (
        hasattr(annotation, "__args__")
        and len(annotation.__args__) == 2
        and type(None) in annotation.__args__
    )


def _eval_optional(annotation: object) -> object:
    for arg in annotation.__args__:
        if arg is None:
            continue

        return arg


class Choice:
    """Represents a multiple-choice argument type.

    A special type is used to allow declaring as:

        def example(choice: Choice("one", "two", "three")) -> None:
            ...

    """

    def __init__(self, *choices: T) -> None:
        self.choices = choices

    def __call__(self, item: object) -> T:
        if not item in self.choices:
            raise CLIRuntimeException(f"invalid choice {item!r} (available: {self!s}).")

        return item

    def __str__(self) -> str:
        return f"{'|'.join(self.choices)}"


TOption = TypeVar("TOption")


class Option(NamedTuple):
    """Represents a CLI option type."""

    key: str
    doc: str
    annotation: Callable[[str | None], Type[TOption]]
    default: TOption


HELP_OPT = Option(
    key="help",
    doc="Prints this message and exits. (default: False)",
    annotation=bool,
    default=False,
)


class Command(NamedTuple):
    """Represents a CLI command.

    These commands are just nice wrappers around the functions passed in, containing
    useful metadata on them.
    """

    name: str
    real_name: str
    doc: str
    param_doc: dict[str, str]
    value: Callable[..., None]


EMPTY_COMMAND = Command("", "", "", int, 0)


def _positive_boolean_flag(value: str | None) -> bool:
    """A positive boolean flag option factory.

    This replaces the `bool` factory when `opt.default` == False.

    Returns:
        value is None (`--arg`): True
        value in ["true", "1", "yes"] (`--arg=true`): True
        else: False
    """

    if value is None:
        return True

    return value.lower() in ["true", "1", "yes"]


def _negative_boolean_flag(value: str | None) -> bool:
    """A negative boolean flag option factory.

    This replaces the `bool` factory when `opt.default` == True.

    Returns:
        value is None (`--arg`): False
        value in ["false", "0", "no"] (`--arg=false`): False
        else: True
    """

    if value is None:
        return False

    return value.lower() in ["false", "0", "no"]


def _empty_annotation(value: str) -> str:
    """Returns the value it was given.

    This is used when no type annotation is given.
    """

    return value


def _get_schema(
    command: Callable[..., None], param_docs: dict[str, str]
) -> dict[str, Option]:
    """Extracts a schema from the given command and infuses parameter documentation."""

    schema: dict[str, Option] = {}

    kwonly = getfullargspec(command).kwonlyargs

    for name, param in signature(command).parameters.items():
        default = EMPTY if param.default is Signature.empty else param.default

        default_repr = (
            str(default.resolve()) if isinstance(default, Path) else repr(default)
        )

        if name not in param_docs:
            raise CLIParserException(f"undocumented option {name!r}.")

        schema[name] = Option(
            key=name.replace("_", "-"),
            doc=(
                param_docs[name]
                + (f" (default: {default_repr})" if default is not EMPTY else "")
            ),
            annotation=param.annotation,
            default=default,
        )

    return schema


TAnnotation = TypeVar("TAnnotation")


def _get_factory_from_annotation(
    annotation: TAnnotation,
    default: TAnnotation | None,
) -> Callable[[str], TAnnotation]:
    if annotation is bool:
        if default:
            return _negative_boolean_flag

        return _positive_boolean_flag

    if annotation is datetime:
        return lambda item: datetime.strptime(item, DATE_FORMAT)

    if annotation is Signature.empty:
        return _empty_annotation

    return annotation


def _apply_factory(opt: Option, value: str) -> Any:
    """Converts `value` using `opt.factory`."""

    annotation = opt.annotation

    if hasattr(annotation, "__args__"):
        args = [arg for arg in annotation.__args__ if arg is not type(None)]
        errors = []

        for arg in args:
            if arg is None:
                continue

            try:
                factory = _get_factory_from_annotation(arg, opt.default)
                return factory(value)

            except (ValueError, TypeError) as exc:
                errors.append(exc)

        displayable = ", ".join(f"{type(exc).__name__}: {str(exc)}" for exc in errors)

        raise CLIRuntimeException(
            f"couldn't convert {value!r} to valid type: {displayable}"
        )

    try:
        factory = _get_factory_from_annotation(annotation, opt.default)

        return factory(value)

    except (ValueError, TypeError) as exc:
        raise CLIRuntimeException(f"({opt.key}) " + str(exc))


def _parse_opts(
    args: list[str], schema: dict[str, Option]
) -> tuple[list[Any], dict[str, Any]]:
    """Parses the given arguments based on the schema, converting as necessary.

    The returned object is a tuple of *args and **kwargs to pass to the function the
    schema is based on.
    """

    shorthand_lookup = {name[0]: opt for name, opt in reversed(schema.items())}
    schema_keys = [*schema]

    positionals = []
    keywords = {}

    i = 0
    while True:
        if i >= len(args):
            break

        arg = args[i]

        if arg.startswith("-"):
            is_longhand = arg.startswith("--")

            value = None
            if "=" in arg:
                arg, value = arg.split("=")

            key = arg.lstrip("-").replace("-", "_")
            opt = schema[key] if is_longhand else shorthand_lookup[key]

            if value is None and len(args) > i + 1 and not args[i + 1].startswith("-"):
                value = args.pop(i + 1)

            keywords[opt.key.replace("-", "_")] = _apply_factory(opt, value)

        else:
            index = len(positionals)

            if index >= len(schema_keys):
                raise CLIRuntimeException(
                    f"can't map positional {arg!r} at index {index} to the schema."
                )

            opt = schema[schema_keys[index]]

            if opt.default is not EMPTY:
                index += len(keywords)

                opt = schema[schema_keys[index]]

            positionals.append(_apply_factory(opt, arg))

        i += 1

    return tuple(positionals), keywords


@dataclass
class HelpFormatter:
    """A str() printable help text generator."""

    exec_line: str
    """The first term of the shell command that called the CLI, like /path/to/script.py."""

    doc: str
    """The documentation of the current command.

    It will be the __doc__ field of either the calling CLI module ('stem' mode, e.g. no
    command given), or the selected command.
    """

    schema: dict[str, Option]
    """A dictionary of option names to Option objects."""

    commands: list[Callable[..., None]]
    """The commands available in the current context.

    A list of all registered commands if running the 'stem', empty list otherwise.
    """

    @staticmethod
    def _find_max_len(seq: Iterable[str]) -> int:
        """Finds the maximum length item in the given iterable, handling empty case."""

        items = list(seq)

        if len(items) == 0:
            return 0

        return max(len(item) for item in items)

    def _align_section(self, lines: list[tuple[str, str]]) -> str:
        """Aligns a section of (left, right) lines.

        The alignment is done based on the left side.

        For example:

            >>> formatter._align_section([
            ... ("1", "one"),
            ... ("22", "two"),
            ... ("333", "three"),
            ... ("4444", "four")])

        Will return:

            1     one
            22    two
            333   three
            4444  four

        """

        left = [line[0] for line in lines]
        right = [line[1] for line in lines]

        left_width = self._find_max_len(left)
        total_left_width = left_width + 2 + 2 * len(INDENT)

        return (
            INDENT
            + f"\n{INDENT}".join(
                "\n".join(
                    wrap(
                        f"{left:<{left_width}}  {right}",
                        width=TERMINAL_WIDTH - len(INDENT),
                        subsequent_indent=total_left_width * " ",
                    )
                )
                for left, right in lines
            )
            + "\n"
        )

    def __str__(self) -> str:
        usage_text = f"Usage: {self.exec_line}"

        positionals = [opt for opt in self.schema.values() if opt.default is EMPTY]
        options = [opt for opt in self.schema.values() if opt not in positionals]

        if len(options) > 0:
            for opt in options:
                key = opt.key

                if key == "help":
                    continue

                usage_text += f" [--{key}"

                if opt.annotation not in [
                    _positive_boolean_flag,
                    _negative_boolean_flag,
                ]:
                    usage_text += " " + key.upper().replace("-", "_")

                usage_text += "]"

        if len(self.commands) > 0:
            usage_text += " <command>"

        if len(positionals) > 0:
            usage_text += " " + " ".join("{" + opt.key + "}" for opt in positionals)

        usage_text = "\n".join(wrap(usage_text, width=TERMINAL_WIDTH))

        options_text = ""
        if options:
            options_text += "Options:\n"

            lines = []
            shorthands = []
            for opt in options:
                left = f"--{opt.key}"

                if opt.key[0] not in shorthands:
                    left = f"-{opt.key[0]}, " + left

                annotation = opt.annotation

                if _is_optional(annotation):
                    annotation = _eval_optional(annotation)

                if isinstance(annotation, Choice):
                    left += " " + str(annotation)

                if annotation is datetime:
                    left += " " + DATE_FORMAT

                shorthands.append(opt.key[0])
                lines.append((left, opt.doc))

            options_text += self._align_section(lines)

        commands_text = ""
        if self.commands:
            commands_text += "Commands:\n"
            commands_text += self._align_section(
                [(cmd.name, cmd.doc) for cmd in self.commands]
            )

        doc_text = "\n\n".join(
            "\n".join(
                wrap(
                    part,
                    width=TERMINAL_WIDTH - len(INDENT),
                    initial_indent=INDENT,
                    subsequent_indent=INDENT,
                )
            )
            for part in self.doc.split("\n\n")
        )

        output = f"{usage_text}\n\n{doc_text}\n"

        if options_text:
            output += "\n" + options_text
        if commands_text:
            output += "\n" + commands_text

        return output.rstrip("\n")


class ZmlHelpFormatter(HelpFormatter):
    """A formatter to add minimal styling to the default."""

    @staticmethod
    def _dim_every_second_line(matchobj: Match) -> str:
        print(matchobj.groups())
        return ""

        print("matched", matchobj)
        lines = []
        for i, line in enumerate(matchobj[1].splitlines()):
            if i % 0:
                line = f"[dim]{line}[/dim]"

            lines.append(line)

        return "\n".join(lines)

    def __str__(self) -> str:
        text = zml_escape(super().__str__())

        # Dim every second line
        # text, count = re.subn(
        # r"(  \-.*(?:\n +  )?)\n(  \-.*(?:\n +  .*)?)",
        # r"(?m)(  \-.*(?:\n +  )?)\n((?:  \-.*(?:\n +  .*)|))",
        # r"(?m)(  \-.*(?:\n +  )?)\n((?:  \-.*(?:\n +  .*)))|(  -h, --help.*)",
        # r"[dim]\1\3[/dim]\n\2",
        # text,
        # )

        # Dim code
        text = re.sub(r"\B`([^`]+)`\B", r"[@#333333 dim] \1 [/bg /dim]", text)

        # Highlight strings
        text = re.sub(r"\B'([^']+)'\B", r"'[113]\1[/fg]'", text)

        # Embolden positional (required) options
        text = re.sub(r"\] {([a-z0-9]+)}", r"] {[bold]\1[/bold]}", text)

        # Italicizes first line (title)
        text = re.sub(
            fr"Usage: (.*\n\n{INDENT})(.*)",
            fr"Usage: \1[italic]\2[/italic]",
            text,
        )

        # Embolden section titles
        text = re.sub(
            fr"((?:\n\n)|^)((?:Usage|Commands|Options)\:)",
            fr"\1[bold]\2[/bold]",
            text,
        )

        # Italicize default values
        text = re.sub(
            r"\(default:([ \n]+)([^\)]+)\)", r"(default:\1[italic]\2[/italic])", text
        )

        return zml(text)


def _get_param_sorter(param_doc: dict[str, str]) -> Callable[[str], int]:
    """Returns a sorter that puts "help" at the end, retaining everything else's order"""

    def _key(item: tuple[str, Option]) -> str:
        name = item[0]

        if name == "help":
            return 2023_07_01_20_57_53

        return [*param_doc].index(name.replace("-", "_"))

    return _key


@contextmanager
def carmine_cli(
    module_doc: str,
    argv: list[str],
    help_formatter: Type[HelpFormatter] = (
        ZmlHelpFormatter if ZENITH_INSTALLED else HelpFormatter
    ),
) -> Iterator[None]:
    """Runs a carmine CLI application.

    Args:
        module_doc: The global `__doc__` variable.
        argv: The arguments passed to the CLI.
        help_formatter: A HelpFormatter subclass that's used to print the help text.
    """

    schema = {"help": HELP_OPT}
    commands = []

    def _register(*cmds: Callable[..., None]) -> None:
        """Registers and parses any number of commands given to it."""

        for command in cmds:
            if command is Ellipsis:
                raise CLIParserException(
                    "no commands registered (placeholder '...' still remains)."
                )

            if command.__doc__ is None:
                raise CLIParserException(
                    f"command {command.__name__!r} doesn't have a docstring."
                )

            docstring = Docstring(command.__doc__, lineno=1)
            parsed = parse(docstring, parser=Parser.google)

            doc = parsed[0].value

            params = parsed[1].value if len(parsed) > 1 else []

            param_doc = {}
            for param in params:
                param_doc[param.name] = " ".join(param.description.splitlines())

            commands.append(
                Command(
                    command.__name__.replace("_", "-"),
                    command.__name__,
                    doc,
                    param_doc,
                    command,
                )
            )

    helper = help_formatter(argv[0], module_doc, schema, commands)

    try:
        yield _register

        single_command = len(commands) == 1

        if not single_command and (len(argv) == 1 or (command_name := argv[1]) is None):
            print(helper)
            return

        if argv[1:] in (["-h"], ["--help"]):
            print(helper)
            return

        if single_command:
            command = commands.pop(0)
            argv.insert(0, command.name)

        else:
            for command in commands:
                if command.name == command_name:
                    break
            else:
                command = EMPTY_COMMAND
                raise CLIRuntimeException(f"unknown command {command_name!r}.")

        sort_key = _get_param_sorter(command.param_doc)
        schema_unsorted = schema | _get_schema(command.value, command.param_doc)

        schema = {
            key: value for key, value in sorted(schema_unsorted.items(), key=sort_key)
        }

        helper.doc = command.doc
        helper.schema = schema
        helper.commands.clear()

        args, kwargs = _parse_opts(argv[2:], schema)

        if "help" in kwargs:
            print(helper)
            return

        try:
            command.value(*args, **kwargs)

        except TypeError as exc:
            line = "'" + command.real_name + "("

            if len(args):
                line += ", ".join(str(arg) for arg in args)

            if len(kwargs):
                if not line.endswith("("):
                    line += ", "

                line += ", ".join(f"{key}={value}" for key, value in kwargs.items())

            line += f")': {str(exc).removeprefix(command.name + '() ')}"

            raise CLIRuntimeException(line)

    except (CLIRuntimeException, CLIUserException) as exc:
        if not os.getenv("ERROR_ONLY"):
            print(helper, end="\n\n")

        if os.getenv("DEBUG"):
            raise

        if command is EMPTY_COMMAND:
            error = f"error: {exc.message}"

        elif exc.message.startswith(f"'{command.real_name}"):
            error = f"error executing {exc.message}: "

        else:
            error = f"error executing {command.real_name!r}: {exc.message}"

        print(
            "\n".join(
                wrap(
                    error,
                    width=TERMINAL_WIDTH,
                    subsequent_indent=min(error.index(":"), error.index("'")) * " "
                    + 2 * INDENT,
                )
            )
        )

        sys.exit(1)
