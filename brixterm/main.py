# flake8: noqa: E402
import argparse
import os

from brixterm.constants import CHAT_HIST_SIZE, CMD_HIST_SIZE, DEFAULT_GPT_MODEL

parser = argparse.ArgumentParser(description="BrixTerm AI Terminal")
parser.add_argument(
    "--dev", action="store_true", help="(optional) Run in development mode " "with Arize Phoenix tracing enabled."
)
parser.add_argument(
    "--light_mode", action="store_true", help="(optional) Optimize looks for light mode terminal (dark is default)."
)
parser.add_argument(
    "--model", help=f"(optional) Specify GPT model. (default='{DEFAULT_GPT_MODEL}')", default=DEFAULT_GPT_MODEL
)
args = parser.parse_args()

if args.dev:
    from llmbrix.tracing import configure_arize_tracing

    configure_arize_tracing(project_name="BrixTerm")

from brixterm.ai import ChatBot, CodeGenerator, SmartTerminal
from brixterm.command_executor import CommandExecutor
from brixterm.command_history import CommandHistory
from brixterm.console_printer import ConsolePrinter
from brixterm.terminal_app import TerminalApp

gpt_model = args.model
dark_mode = not args.light_mode

color_mode_var = os.getenv("BRIXTERM_COLOR_MODE")
if color_mode_var == "dark":
    dark_mode = True
if color_mode_var == "light":
    dark_mode = False

if os.getenv("BRIXTERM_MODEL"):
    gpt_model = os.getenv("BRIXTERM_MODEL")


def main():
    printer = ConsolePrinter(dark_mode=dark_mode)
    executor = CommandExecutor()
    cmd_hist = CommandHistory(size=CMD_HIST_SIZE)
    smart_terminal = SmartTerminal(
        gpt_model=gpt_model, console_printer=printer, command_executor=executor, command_history=cmd_hist
    )
    chatbot = ChatBot(gpt_model=gpt_model, chat_hist_size=CHAT_HIST_SIZE)
    code_generator = CodeGenerator(gpt_model=gpt_model, console_printer=printer, chat_hist_size=CHAT_HIST_SIZE)

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
