from brixterm.command_executor import CommandExecutor
from brixterm.console_context import ConsoleContext
from brixterm.console_printer import ConsolePrinter


class SmartTerminal:
    def __init__(self, command_executor: CommandExecutor, console_printer: ConsolePrinter):
        self.command_executor = command_executor
        self.console_printer = console_printer

    def _run_and_print(self, cmd):
        completed_process = self.command_executor.execute_shell_cmd(cmd)
        self.console_printer.print_subprocess_output(completed_process)
        return completed_process

    def run(self, cmd: str, ctx: ConsoleContext):
        completed_process = self._run_and_print(cmd)
        if completed_process.returncode != 0:
            suggested_cmd = "ls -la"  # TODO
            if suggested_cmd:
                self.console_printer.print("\n[bold red]Command failed.[/bold red]")
                self.console_printer.print(f"Suggested fix:\n  [bold green]{suggested_cmd}[/bold green]")
                self.console_printer.print("\n[cyan]Do you want to run the suggested command?[/cyan]")
                user_input = input("  [y/N]: ").strip()

                if user_input.strip().lower() == "y":
                    completed_process = self._run_and_print(suggested_cmd)
        return completed_process
