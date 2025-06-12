import os
import subprocess

import pyperclip
from llmbrix.agent import Agent
from llmbrix.chat_history import ChatHistory
from llmbrix.gpt_openai import GptOpenAI
from llmbrix.msg import SystemMsg, UserMsg
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.history import FileHistory
from pydantic import BaseModel
from rich.console import Console
from rich.text import Text


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
    system_msg=SystemMsg(content="Concise assistant in a terminal window."),
)

code_bot = Agent(
    gpt=GptOpenAI(model=MODEL, output_format=GeneratedCode),
    chat_history=ChatHistory(),
    system_msg=SystemMsg(content="Only respond with valid Python code. No explanation."),
)

terminal_bot = Agent(
    gpt=GptOpenAI(model=MODEL, output_format=TerminalCommand),
    chat_history=ChatHistory(),
    system_msg=SystemMsg(content="Fix broken terminal commands or convert natural language to valid Unix commands."),
)

# ========== Terminal Logic ==========
console = Console()
session = PromptSession(
    completer=PathCompleter(),
    history=FileHistory(HIST_FILE),
)


def run_shell_command(cmd, cwd):
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout:
            console.print(result.stdout.strip())
        if result.stderr:
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
    while True:
        try:
            prompt_path = os.path.relpath(cwd, os.path.expanduser("~"))
            if not prompt_path.startswith(".."):
                prompt_path = f"~/{prompt_path}".lstrip("~/")
            prompt = f"{prompt_path} > "

            cmd = session.prompt(prompt).strip()

            if cmd in {"e", "exit", "quit", "q"}:
                break
            elif cmd.startswith("cd "):
                target = os.path.expanduser(cmd[3:].strip())
                new_dir = os.path.abspath(target)
                if os.path.isdir(new_dir):
                    cwd = new_dir
                else:
                    console.print(Text(f"No such directory: {target}", style="red"))
            elif cmd.startswith("a "):
                question = cmd[2:].strip()
                if question:
                    result = ai_bot.chat(UserMsg(content=question)).content
                    console.print(result)  # no markdown formatting
            elif cmd.startswith("c "):
                prompt = cmd[2:].strip()
                res = code_bot.chat(UserMsg(content=prompt))
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
