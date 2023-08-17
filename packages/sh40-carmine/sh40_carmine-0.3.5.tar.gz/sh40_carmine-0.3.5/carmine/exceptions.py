from dataclasses import dataclass


@dataclass
class CLIException(BaseException):
    """An exception raised within the carmine CLI."""

    message: str

    def __str__(self) -> None:
        return self.message


class CLIParserException(CLIException):
    """An exception raised while building the CLI."""


class CLIRuntimeException(CLIException):
    """An exception raised while running the CLI, usually due to user input."""


class CLIUserException(CLIException):
    """A generic exception that will be pretty printed.

    Use this for your custom exceptions.
    """
