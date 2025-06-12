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
        content="Only respond with valid Python code. No explanation. Docstrings for everything. No inline comments."
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
    """
    Run `cmd` in directory `cwd`, printing stdout and stderr.
    Returns the CompletedProcess so caller can inspect returncode & stderr.
    """
    env = os.environ.copy()
    env["PWD"] = cwd

    try:
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
            # Print stderr as info on success, or in red on failure
            style = None if result.returncode == 0 else "red"
            console.print(Text(result.stderr.strip(), style=style))
        return result

    except Exception as e:
        console.print(Text(f"Error running command: {e}", style="red"))
        # create a dummy CompletedProcess with non-zero returncode
        dummy = subprocess.CompletedProcess(cmd, 1, stdout="", stderr=str(e))
        return dummy


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
            # build a cleaner prompt
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

            # run anything else
            result = run_shell_command(cmd, cwd)
            # decide whether to suggest a fix
            if result.returncode != 0:
                base = cmd.split()[0]
                stderr = (result.stderr or "").lower()
                need_suggest = True
                if base == "git":
                    # only on real git errors
                    need_suggest = ("fatal:" in stderr) or ("error:" in stderr)
                if need_suggest:
                    suggest_and_run(cmd, cwd)

        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    main()
