# flake8: noqa: E402
import logging
import os
from llmbrix.gemini_model import GeminiModel
from brixterm.constants import CHAT_HIST_SIZE, CMD_HIST_SIZE, DEFAULT_GPT_MODEL

from brixterm.ai import ChatBot, CodeGenerator, SmartTerminal
from brixterm.command_executor import CommandExecutor
from brixterm.command_history import CommandHistory
from brixterm.console_printer import ConsolePrinter
from brixterm.terminal_app import TerminalApp

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

MODEL = "gemini-2.5-flash-lite"


gpt = GeminiModel.from_gemini_api_key(gpt_model=MODEL)

def main():
    printer = ConsolePrinter()
    executor = CommandExecutor()
    cmd_hist = CommandHistory(size=CMD_HIST_SIZE)
    smart_terminal = SmartTerminal(
        gpt=gpt, console_printer=printer, command_executor=executor, command_history=cmd_hist
    )
    chatbot = ChatBot(gpt=gpt, chat_hist_size=CHAT_HIST_SIZE)
    code_generator = CodeGenerator(gpt=gpt, console_printer=printer, chat_hist_size=CHAT_HIST_SIZE)
    app = TerminalApp(
        console_printer=printer,
        command_executor=executor,
        smart_terminal=smart_terminal,
        chatbot=chatbot,
        code_generator=code_generator,
        command_history=cmd_hist,
    )
    printer.print(f"\n🚀 [cyan]... Starting BrixTerm with GPT model:[/cyan] [red]💣 {gpt_model} 💣[/red]... 🚀")
    app.run()


if __name__ == "__main__":
    main()
