# flake8: noqa: E501

TERM_INPUT_PREFIX = (
    "\033[1;32m{}\033[0m "  # venv: bright green
    "\033[1;36m{}@{}\033[0m "  # user@host: cyan
    "\033[1;34m{}\033[0m "  # cwd: blue
    "> "  # prompt symbol
)

INTRODUCTION_MSG = (
    "\n\n[bold red]**** Welcome to BrixTerm! ****[/bold red]\n\n[bold blue]AVAILABLE COMMANDS:[/bold blue]\n\n"
    "[bold yellow]TERMINAL[/bold yellow] [bold yellow](default)[/bold yellow] - Type any "
    "[bold yellow]terminal command[/bold yellow]. If it fails then AI will suggest corrected version.\n"
    "[bold cyan]INTERACTIVE SHELL[/bold cyan] - Type [bold cyan]!<command>[/bold cyan] to run interactive shell. "
    "Without [bold cyan]![/bold cyan] interactive commands will timeout after 10s. E.g. try to run [bold cyan]!htop[/bold cyan]\n"
    "[bold green]CODE GEN[/bold green] - Type [bold green]c <your msg>[/bold green] to generate Python code and copy to clipboard.\n"
    "[bold blue]ANSWER[/bold blue] - Type [bold blue]a <your msg>[/bold blue] to talk to LLM chatbot.\n"
    "[bold purple]EXIT[/bold purple] - Type [bold purple]q[/bold purple] to exit.\n"
)
PHOENIX_HOST = "localhost"
PHOENIX_PORT = "4317"
