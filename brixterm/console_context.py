from dataclasses import dataclass


@dataclass
class ConsoleContext:
    cwd: str
    cwd_name: str
