class CommandExecutionError(Exception):
    """Raised when a shell command fails."""

    def __init__(self, message="Command execution failed."):
        super().__init__(message)
