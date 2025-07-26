# flake8: noqa: E402
import argparse

parser = argparse.ArgumentParser(description="BrixTerm AI Terminal")
parser.add_argument("--dev", action="store_true", help="Enable Arize tracing")
args = parser.parse_args()

if args.dev:
    from llmbrix.tracing import configure_arize_tracing

    configure_arize_tracing(project_name="BrixTerm")

from brixterm.ai import ChatBot, CodeGenerator, SmartTerminal
from brixterm.command_executor import CommandExecutor
from brixterm.command_history import CommandHistory
from brixterm.console_printer import ConsolePrinter
from brixterm.terminal_app import TerminalApp

GPT_MODEL = "gpt-4o-mini"
CMD_HIST_SIZE = 10
CHAT_HIST_SIZE = 10


def main():
    printer = ConsolePrinter()
    executor = CommandExecutor()
    cmd_hist = CommandHistory(size=CMD_HIST_SIZE)
    smart_terminal = SmartTerminal(
        gpt_model=GPT_MODEL, console_printer=printer, command_executor=executor, command_history=cmd_hist
    )
    chatbot = ChatBot(gpt_model=GPT_MODEL, chat_hist_size=CHAT_HIST_SIZE)
    code_generator = CodeGenerator(gpt_model=GPT_MODEL, console_printer=printer, chat_hist_size=CHAT_HIST_SIZE)

    app = TerminalApp(
        console_printer=printer,
        command_executor=executor,
        smart_terminal=smart_terminal,
        chatbot=chatbot,
        code_generator=code_generator,
        command_history=cmd_hist,
    )
    app.run()


if __name__ == "__main__":
    main()
