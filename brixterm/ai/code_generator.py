import pyperclip
from llmbrix.agent import Agent
from llmbrix.chat_history import ChatHistory
from llmbrix.gpt_openai import GptOpenAI
from llmbrix.msg import SystemMsg, UserMsg
from pydantic import BaseModel, Field

from brixterm.console_printer import ConsolePrinter

SYS_PROMPT = (
    "You generate Python code based on users request."
    "Every time you only return valid Python code."
    "User can ask for some refinement of previously generated code. Pay attention to their requests."
)


class GeneratedPythonCode(BaseModel):
    explanation_for_user: str = Field(
        ..., description="Short explanation how you understood user's task and what is the generated code doing."
    )
    generated_python_code: str = Field(
        ...,
        description="Piece of valid python code solving user's request. "
        "It will be directly copied into .py file for execution.",
    )


class CodeGenerator:
    def __init__(
        self,
        gpt_model: str,
        console_printer: ConsolePrinter,
        chat_hist_size=10,
    ):
        self.console_printer = console_printer
        self.agent = Agent(
            gpt=GptOpenAI(model=gpt_model, output_format=GeneratedPythonCode),
            chat_history=ChatHistory(max_turns=chat_hist_size),
            system_msg=SystemMsg(content=SYS_PROMPT),
        )

    def generate_and_print(self, user_input, clipboard=False):
        clipboard_mention = ", "
        if clipboard:
            user_input += f"\n\nBelow is copied code for context: ```python\n{pyperclip.paste()}\n```"
            clipboard_mention = " with code from clipboard, "

        self.console_printer.print(
            f"🧠 [bold green] Got your code generation request{clipboard_mention}working... 🤖[/bold green]"
        )
        response = self.agent.chat(UserMsg(content=user_input))
        explanation = response.content_parsed.explanation_for_user
        code = response.content_parsed.generated_python_code
        pyperclip.copy(code)
        self.console_printer.print("🧠 [bold green] Code generation request completed.[/bold green]")
        self.console_printer.print_python(code)
        self.console_printer.print(f"🔍 🤖 [bold red]{explanation}[/bold red] 🤖")
        self.console_printer.print("✅️ [grey]Copied to clipboard... 🤖[/grey]")
