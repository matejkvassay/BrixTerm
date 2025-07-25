import os

from brixterm.command_executor import CommandExecutor
from brixterm.console_printer import ConsolePrinter

INTRODUCTION_MSG = "Mini Shell - type 'exit' to quit"


class TerminalApp:
    def __init__(self):
        self.executor = CommandExecutor()
        self.printer = ConsolePrinter()
        self.cwd = os.getcwd()

    def run(self):
        print(INTRODUCTION_MSG)
        while True:
            try:
                cmd = input("$ ").strip()
                if cmd.lower() in ("exit", "quit", "e", "q"):
                    break
                elif not cmd:
                    continue
                elif cmd.startswith("cd "):
                    os.chdir(cmd[3:].strip())
                    self.cwd = os.getcwd()
                else:
                    completed_process = self.executor.execute_console_cmd(cmd)
                    self.printer.print_subprocess_output(completed_process)
            except KeyboardInterrupt:
                print("\n(Interrupted)")
            except Exception as e:
                print(f"Error: {e}")
