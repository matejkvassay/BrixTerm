from brixterm.ai import SmartTerminal
from brixterm.command_executor import CommandExecutor
from brixterm.configure_phoenix import configure_phoenix
from brixterm.console_printer import ConsolePrinter
from brixterm.terminal_app import TerminalApp

configure_phoenix()

GPT_MODEL = "gpt-4o"


def main():
    printer = ConsolePrinter()
    executor = CommandExecutor()
    smart_terminal = SmartTerminal(gpt_model=GPT_MODEL, console_printer=printer, command_executor=executor)
    app = TerminalApp(console_printer=printer, command_executor=executor, smart_terminal=smart_terminal)
    app.run()


if __name__ == "__main__":
    main()
