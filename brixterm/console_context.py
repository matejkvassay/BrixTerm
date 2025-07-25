from dataclasses import dataclass


@dataclass
class ConsoleContext:
    cwd: str
    cwd_name: str
    venv: str
    user: str
    host: str
