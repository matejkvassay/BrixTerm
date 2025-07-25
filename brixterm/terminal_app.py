import os

from brixterm.command_executor import CommandExecutor
from brixterm.console_context import ConsoleContext
from brixterm.console_printer import ConsolePrinter
from brixterm.constants import INTRODUCTION_MSG, TERM_INPUT_PREFIX


class TerminalApp:
    def __init__(self):
        self.executor = CommandExecutor()
        self.printer = ConsolePrinter()
        self.cwd = os.getcwd()
        self.logical_cwd = os.environ.get("PWD", self.cwd)

    @staticmethod
    def get_logical_cwd_name(cwd: str) -> str:
        path = os.path.abspath(cwd)
        base = os.path.basename(path)
        parent = os.path.dirname(path)
        if parent == "/":
            return f"/{base}"
        return base

    def get_context(self) -> ConsoleContext:
        cwd_name = self.get_logical_cwd_name(self.logical_cwd)
        return ConsoleContext(cwd=self.cwd, cwd_name=cwd_name)

    def read_input(self) -> str:
        prefix = TERM_INPUT_PREFIX.format(self.get_context().cwd_name)
        return input(prefix).strip()

    def run(self):
        self.printer.print(INTRODUCTION_MSG)
        while True:
            try:
                cmd = self.read_input()
                if cmd.lower() in ("exit", "quit", "e", "q"):
                    break
                elif not cmd:
                    continue
                elif cmd.startswith("cd "):
                    self.cwd, self.logical_cwd = self.executor.execute_cd_command(cmd)
                else:
                    completed_process = self.executor.execute_console_cmd(cmd)
                    self.printer.print_subprocess_output(completed_process)
            except KeyboardInterrupt:
                self.printer.print("\n(Interrupted)")
            except Exception as e:
                self.printer.print(f"Error: {e}")
