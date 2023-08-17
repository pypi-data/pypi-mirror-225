"""Carmine's utility CLI."""

import sys
from pathlib import Path

from .cli import carmine_cli, CLIUserException

EXAMPLE_FUNCTION = """\
def hello(
    name: str, age: int = 2, *, message_template: str = \"Hello {name} of {age}!\"
) -> None:
    \"\"\"Says hello to someone.

    In this example, `name` and `age` can be passed as either positional or keyword
    options (`--arg`), but `message_template` must always be passed by keyword, denoted
    using the `*` operator.

    This behaviour follows the same rules as when calling the function within Python,
    since that's what's happening under the hood.

    Args:
        name: The name of the person to say hello to.
        age: The age of the person.
        message_template: The template to format our greeting with.
    \"\"\"

    print(message_template.format(name=name, age=age))

"""


TEMPLATE = """\
\"\"\"{doc}\"\"\"

import sys
from carmine import carmine_cli

{example}
def main(argv: list[str] | None = sys.argv) -> None:
    \"\"\"Runs the application.\"\"\"

    with carmine_cli(__doc__, argv) as register:
        {register_line}


if __name__ == \"__main__\":
    main()
"""


def run(module: str) -> None:
    """Runs the given module.

    Args:
        module: The qualified path.to.module.
    """


def init(
    path: Path, *, example: bool = False, doc: str = "My Carmine application."
) -> None:
    """Initializes a Carmine application.

    Args:
        path: The path to create the runner file at.
        doc: The application's 'main' (module-level) documentation string.
        example: Whether to include the example function in the runner file.
    """

    if not path.parent.exists():
        raise CLIUserException(f"no parent for path {path!s}.")

    path.write_text(
        TEMPLATE.format(
            doc=doc,
            example=EXAMPLE_FUNCTION if example else "",
            register_line="register(hello)" if example else "register(...)",
        )
    )

    print(f"Sucessfully created runner file at {path!s}.")


def main(argv: list[str] = sys.argv) -> None:
    """Runs the application."""

    with carmine_cli(__doc__, argv) as register:
        register(init, run)


if __name__ == "__main__":
    import sys

    main(sys.argv)
