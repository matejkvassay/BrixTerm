from subprocess import CompletedProcess

from rich.console import Console
from rich.markdown import Markdown


class ConsolePrinter:
    def __init__(self):
        self.console = Console(color_system="truecolor")

    def print_markdown(self, content: str):
        markdown = Markdown(content)
        self.console.print(markdown)

    def print_subprocess_output(self, completed_process: CompletedProcess):
        if completed_process.stdout:
            self.console.print(f"[bold green]STDOUT:[/bold green]\n{completed_process.stdout}")
        if completed_process.stderr:
            self.console.print(f"[bold red]STDERR:[/bold red]\n{completed_process.stderr}")
        self.console.print(f"[dim]Return code: {completed_process.returncode}[/dim]")
