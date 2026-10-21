"""Typed errors. `cli` turns them into messages and exit codes."""


class ShuttleError(Exception):
    """Base class for all expected errors."""

    exit_code = 3


class SourceError(ShuttleError):
    """An agent or skill source is invalid."""

    exit_code = 2


class ConfigError(ShuttleError):
    """`models.toml` is invalid or does not resolve a model."""

    exit_code = 2


class UsageError(ShuttleError):
    """The command line is invalid."""

    exit_code = 3
