import pyperclip
from llmbrix.gemini_model import GeminiModel
from llmbrix.msg import UserMsg
from pydantic import BaseModel, Field

from brixterm.console_printer import ConsolePrinter

SYS_PROMPT = (
    "You generate Python code based on users request."
    "Every time you only return valid Python code."
    "User can ask for some refinement of previously generated code. Pay attention to their requests."
)


class GeneratedPythonCode(BaseModel):
    explanation: str = Field(
        ..., description="Short explanation how you understood user's task and what is the generated code doing."
    )
    python_code: str = Field(
        ...,
        description="Piece of valid python code solving user's request. "
        "It will be directly copied into .py file for execution.",
    )


class CodeGenerator:
    def __init__(self, gpt: GeminiModel, console_printer: ConsolePrinter):
        self.console_printer = console_printer
        self.gpt = gpt

    def generate_and_print(self, user_input, clipboard=False):
        clipboard_mention = ", "
        if clipboard:
            user_input += f"\n\nBelow is copied code for context: ```python\n{pyperclip.paste()}\n```"
            clipboard_mention = " with code from clipboard, "

        self.console_printer.print(
            f"🧠 [bold green] Got your code generation request{clipboard_mention}working... 🤖[/bold green]"
        )
        response = self.gpt.generate(
            messages=[UserMsg(text=user_input)],
            system_instruction=SYS_PROMPT,
            response_schema=GeneratedPythonCode,
            response_mime_type="application/json",
        )
        explanation = response.parsed.explanation
        code = response.parsed.python_code
        pyperclip.copy(code)
        self.console_printer.print("🧠 [bold green] Code generation request completed.[/bold green]")
        self.console_printer.print_python(code)
        self.console_printer.print(f"🔍 🤖 [bold red]{explanation}[/bold red] 🤖")
        self.console_printer.print("✅️ [grey]Copied to clipboard... 🤖[/grey]")
