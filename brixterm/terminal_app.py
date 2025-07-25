import getpass
import os
import readline  # noqa: F401
import socket

from brixterm.ai import SmartTerminal
from brixterm.console_context import ConsoleContext
from brixterm.console_printer import ConsolePrinter
from brixterm.constants import INTRODUCTION_MSG, TERM_INPUT_PREFIX


class TerminalApp:
    def __init__(self, console_printer: ConsolePrinter, smart_terminal: SmartTerminal):
        self.smart_terminal = smart_terminal
        self.console_printer = console_printer
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
        venv = os.environ.get("VIRTUAL_ENV")
        venv = f"({os.path.basename(venv)})" if venv else ""
        user = getpass.getuser()
        host = socket.gethostname()
        cwd_name = self.get_logical_cwd_name(self.logical_cwd)
        return ConsoleContext(cwd=self.cwd, cwd_name=cwd_name, user=user, host=host, venv=venv)

    def read_input(self) -> tuple[str, ConsoleContext]:
        ctx = self.get_context()
        content = TERM_INPUT_PREFIX.format(ctx.venv, ctx.user, ctx.host, ctx.cwd_name)
        cmd = input(content).strip()
        return cmd, ctx

    def run(self):
        self.console_printer.print(INTRODUCTION_MSG)
        while True:
            try:
                cmd, ctx = self.read_input()

                if cmd.lower() in ("exit", "e", "quit", "q"):
                    break
                elif not cmd:
                    continue
                elif cmd.startswith("!"):
                    self.executor.execute_interactive_shell_cmd(cmd[1:])
                elif cmd.startswith("cd "):
                    self.cwd, self.logical_cwd = self.executor.execute_cd_cmd(cmd)
                elif cmd == "clear":
                    os.system("cls" if os.name == "nt" else "clear")
                else:
                    cmd_name = cmd.split(" ")[0].strip()
                    cmd_content = " ".join(cmd.split(" ")[1:])

                    if cmd_name == "a":
                        self.console_printer.print(f"Asking LLM: {cmd_content}")
                        continue
                    elif cmd_name == "c":
                        self.console_printer.print(f"Generating code for question: {cmd_content}")
                        continue
                    elif cmd_name == "cr":
                        self.console_printer.print(f"Running code review for: {cmd_content}")
                        continue
                    else:
                        self.smart_terminal.run(cmd, ctx)
            except KeyboardInterrupt:
                self.console_printer.print("\n(Interrupted)")
            except Exception as e:
                self.console_printer.print(f"Error: {e}")
