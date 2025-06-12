import os
import subprocess

import pyperclip
from llmbrix.agent import Agent
from llmbrix.chat_history import ChatHistory
from llmbrix.gpt_openai import GptOpenAI
from llmbrix.msg import SystemMsg, UserMsg
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from pydantic import BaseModel
from rich.console import Console
from rich.text import Text

from brixterm.hybrid_completer import HybridCompleter


# ========== Models ==========
class TerminalCommand(BaseModel):
    valid_terminal_command: str


class GeneratedCode(BaseModel):
    python_code: str


# ========== AI Setup ==========
MODEL = "gpt-4o-mini"
HIST_FILE = os.path.expanduser("~/.llmbrix_shell_history")

ai_bot = Agent(
    gpt=GptOpenAI(model=MODEL),
    chat_history=ChatHistory(),
    system_msg=SystemMsg(content="Super brief assistant which runs in a terminal window."),
)

code_bot = Agent(
    gpt=GptOpenAI(model=MODEL, output_format=GeneratedCode),
    chat_history=ChatHistory(),
    system_msg=SystemMsg(
        content="Only respond with valid Python code. No explanation. Docstrings for everything. " "No inline comments."
    ),
)

terminal_bot = Agent(
    gpt=GptOpenAI(model=MODEL, output_format=TerminalCommand),
    chat_history=ChatHistory(),
    system_msg=SystemMsg(
        content="Fix broken terminal commands or convert natural language to valid Unix commands. "
        "If not related to terminal command then return nothing."
    ),
)

# ========== Terminal Logic ==========
console = Console()

session = PromptSession(
    completer=HybridCompleter(),
    history=FileHistory(HIST_FILE),
)


def run_shell_command(cmd, cwd):
    try:
        # Force child shells to use our logical PWD
        env = os.environ.copy()
        env["PWD"] = cwd

        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.stdout:
            console.print(result.stdout.strip())

        if result.stderr:
            if result.returncode == 0:
                console.print(result.stderr.strip())
            else:
                console.print(Text(result.stderr.strip(), style="red"))

        return result.returncode

    except Exception as e:
        console.print(Text(f"Error: {e}", style="red"))
        return 1


def suggest_and_run(cmd, cwd):
    resp = terminal_bot.chat(UserMsg(content=cmd))
    suggestion = getattr(resp.content_parsed, "valid_terminal_command", "")
    if suggestion:
        console.print(Text(f"Did you mean: {suggestion}", style="yellow"))
        confirm = input("Run this? [y/N]: ").strip().lower()
        if confirm == "y":
            return run_shell_command(suggestion, cwd)
    return 1


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

            if cmd in {"e", "exit", "quit", "q"}:
                break

            elif cmd.startswith("cd "):
                raw = cmd[3:].strip()
                target = os.path.expanduser(raw)
                if os.path.isabs(target):
                    new_dir = os.path.abspath(target)
                else:
                    new_dir = os.path.abspath(os.path.join(cwd, target))

                if os.path.isdir(new_dir):
                    cwd = new_dir
                else:
                    console.print(Text(f"No such directory: {raw}", style="red"))

            elif cmd.startswith("a "):
                question = cmd[2:].strip()
                if question:
                    result = ai_bot.chat(UserMsg(content=question)).content
                    console.print(result)

            elif cmd.startswith("c "):
                prompt_text = cmd[2:].strip()
                res = code_bot.chat(UserMsg(content=prompt_text))
                code = getattr(res.content_parsed, "python_code", "")
                if code:
                    pyperclip.copy(code)
                    console.print(code)
                    console.print(Text("Copied to clipboard", style="dim"))

            elif cmd:
                result = run_shell_command(cmd, cwd)
                if result != 0:
                    suggest_and_run(cmd, cwd)

        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    main()
