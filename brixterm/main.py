# flake8: noqa: E402
import logging

import dotenv
import pyperclip
from google.genai.types import ThinkingLevel
from llmbrix.chat_history import ChatHistory
from llmbrix.gemini_model import GeminiModel
from llmbrix.tool_agent import ToolAgent
from llmbrix.tools import CalculatorTool, DatetimeTool

from brixterm.console_printer import ConsolePrinter

logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

dotenv.load_dotenv()
USER_NAME = "User"
MODEL = "gemini-3-flash-preview"
CHAT_HISTORY_TURNS = 5
TOOL_LOOP_LIMIT = 2
SYSTEM_INSTRUCTION = "Be brief, to the point." "Use markdown to highlight and format answers. " "Use emojis"
MODEL_PREFIX = f"\n[cyan]🤖💬  {MODEL}: [/cyan]"
USER_PREFIX = f"\n[red]👤  {USER_NAME}:[/red]"
CMD_CLIPBOARD_PASTE = "ccc"

gemini_model = GeminiModel.from_gemini_api_key(model=MODEL, thinking_level=ThinkingLevel.MINIMAL)
chat_history = ChatHistory(max_turns=CHAT_HISTORY_TURNS)
chatbot = ToolAgent(
    gemini_model=gemini_model,
    chat_history=chat_history,
    loop_limit=TOOL_LOOP_LIMIT,
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[CalculatorTool(), DatetimeTool()],
)


def main():
    printer = ConsolePrinter()
    printer.print(f"\n🚀...[cyan]Starting BrixTerm with GPT model:[/cyan][red] {MODEL}[/red]... 🚀 ")

    cmd = None
    while True:
        if not cmd:
            printer.print(f"{USER_PREFIX}\n")
            cmd = input().strip()
        if cmd.lower().strip() in ("exit", "e", "quit", "q"):
            printer.print(f"{MODEL_PREFIX} See you soon {USER_NAME}!")
            break
        if cmd:
            if cmd.lower().strip().startswith(f"{CMD_CLIPBOARD_PASTE} "):
                clipboard_content = pyperclip.paste()
                cmd = cmd[4:]
                if cmd.strip() == "":
                    continue
                cmd += f"\n\n Content of user's clipboard:\n{clipboard_content}"
                printer.print(f"```\n{clipboard_content}\n```")
            printer.print(f"{MODEL_PREFIX} Thinking...")
            for msg in chatbot.chat_iter(cmd):
                if msg.is_model():
                    if msg.text is not None:
                        printer.print(f"{MODEL_PREFIX}\n")
                        printer.print_markdown(msg.text)
                    if msg.tool_calls:
                        printer.print(
                            f'{MODEL_PREFIX} Using tools: {[f"{t.name}([red]{t.args}[/red])" for t in msg.tool_calls]}...'
                        )
        cmd = None


if __name__ == "__main__":
    main()
