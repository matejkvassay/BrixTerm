import os
import pty
import subprocess

import pyperclip
from llmbrix.agent import Agent
from llmbrix.chat_history import ChatHistory
from llmbrix.gpt_openai import GptOpenAI
from llmbrix.msg import SystemMsg, UserMsg
from openai import AzureOpenAI, OpenAI
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from pydantic import BaseModel
from rich.console import Console
from rich.text import Text

from brixterm.hybrid_completer import HybridCompleter

TERM_MODE_HIST = int(os.getenv("TERM_MODE_HIST", 3))
CODE_MODE_HIST = int(os.getenv("TERM_MODE_HIST", 3))
ANSWER_MODE_HIST = int(os.getenv("TERM_MODE_HIST", 5))
MODEL = os.getenv("BRIX_TERM_MODEL", "gpt-4o-mini")
HIST_FILE = os.path.expanduser("~/.llmbrix_shell_history")


def init_openai_client():
    """
    Initialize the appropriate OpenAI client based on environment variables.
    Uses AzureOpenAI if AZURE_OPENAI_ENDPOINT is set, otherwise defaults to OpenAI.
    """
    if os.getenv("AZURE_OPENAI_ENDPOINT"):
        return AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )
    else:
        return OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )


class TerminalCommand(BaseModel):
    valid_terminal_command: str


class GeneratedCode(BaseModel):
    python_code: str


openai_client = init_openai_client()

ai_bot = Agent(
    gpt=GptOpenAI(model=MODEL, openai_client=openai_client),
    chat_history=ChatHistory(max_turns=ANSWER_MODE_HIST),
    system_msg=SystemMsg(content="Super brief assistant which runs in a terminal window."),
)

code_bot = Agent(
    gpt=GptOpenAI(model=MODEL, output_format=GeneratedCode, openai_client=openai_client),
    chat_history=ChatHistory(max_turns=CODE_MODE_HIST),
    system_msg=SystemMsg(
        content="Only respond with valid Python code. No explanation. Docstrings for everything. No inline comments."
    ),
)

terminal_bot = Agent(
    gpt=GptOpenAI(model=MODEL, output_format=TerminalCommand, openai_client=openai_client),
    chat_history=ChatHistory(max_turns=TERM_MODE_HIST),
    system_msg=SystemMsg(
        content="Fix broken terminal commands or convert natural language to valid Unix commands. "
        "If not related to terminal command then return nothing."
    ),
)

console = Console()

session = PromptSession(
    completer=HybridCompleter(),
    history=FileHistory(HIST_FILE),
)


def run_shell_command(cmd, cwd):
    """
    Run `cmd` in directory `cwd` using a pseudo-terminal,
    so full interactive programs (htop, vim, etc.) work.
    Returns a CompletedProcess-like result with just the return code.
    """
    os.chdir(cwd)

    try:
        exit_code = pty.spawn(["/bin/sh", "-c", cmd])
        return subprocess.CompletedProcess(cmd, exit_code, stdout="", stderr="")
    except Exception as e:
        console.print(Text(f"Error running command: {e}", style="red"))
        return subprocess.CompletedProcess(cmd, 1, stdout="", stderr=str(e))


def suggest_and_run(cmd, cwd):
    """
    Ask the AI for a fixed command, then prompt user to run it.
    """
    resp = terminal_bot.chat(UserMsg(content=cmd))
    suggestion = getattr(resp.content_parsed, "valid_terminal_command", "")
    if suggestion and suggestion != cmd:
        console.print(Text(f"Did you mean: {suggestion}", style="yellow"))
        confirm = input("Run this? [y/N]: ").strip().lower()
        if confirm == "y":
            run_shell_command(suggestion, cwd)


def main():
    cwd = os.getcwd()
    home = os.path.expanduser("~")

    while True:
        try:
            if cwd.startswith(home):
                rel = os.path.relpath(cwd, home)
                prompt_path = "~" if rel == "." else f"~/{rel}"
            else:
                prompt_path = cwd
            prompt = f"{prompt_path} > "

            cmd = session.prompt(prompt).strip()
            if not cmd:
                continue

            if cmd in {"e", "exit", "quit", "q"}:
                break

            if cmd.startswith("cd "):
                raw = cmd[3:].strip()
                target = os.path.expanduser(raw)
                new_dir = target if os.path.isabs(target) else os.path.join(cwd, target)
                new_dir = os.path.abspath(new_dir)
                if os.path.isdir(new_dir):
                    cwd = new_dir
                else:
                    console.print(Text(f"No such directory: {raw}", style="red"))
                continue

            if cmd.startswith("a "):
                question = cmd[2:].strip()
                if question:
                    ans = ai_bot.chat(UserMsg(content=question)).content
                    console.print(ans)
                continue

            if cmd.startswith("c "):
                prompt_text = cmd[2:].strip()
                res = code_bot.chat(UserMsg(content=prompt_text))
                code = getattr(res.content_parsed, "python_code", "")
                if code:
                    pyperclip.copy(code)
                    console.print(code)
                    console.print(Text("Copied to clipboard", style="dim"))
                continue

            result = run_shell_command(cmd, cwd)
            if result.returncode != 0:
                suggest_and_run(cmd, cwd)

        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    main()
