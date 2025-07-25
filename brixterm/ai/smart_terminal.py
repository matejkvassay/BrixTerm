from subprocess import CompletedProcess

from llmbrix.agent import Agent
from llmbrix.chat_history import ChatHistory
from llmbrix.gpt_openai import GptOpenAI
from llmbrix.msg import SystemMsg, UserMsg
from llmbrix.prompt import Prompt
from pydantic import BaseModel

from brixterm.command_executor import CommandExecutor
from brixterm.console_context import ConsoleContext
from brixterm.console_printer import ConsolePrinter

SYS_PROMPT = (
    "User will typed command into terminal but it failed."
    "If the command seems like user tried to execute some unix terminal command but did a mistake or typo "
    "then try to suggest corrected version of that command."
    "If the command doesnt resemble valid unix command then return nothing."
)

USER_PROMPT = Prompt(
    """
    # Command typed by user

        ```bash
        {{cmd}}
        ```

    # Outputs from attempted command execution

    ## Stdout
        ```text
            {{stdout}}
        ```

    ## Stderr
        ```text
        {{stderr}}
        ```

    ## Return code

        ```text
        {{return_code}}
        ```

    # Additional information

    ## List of files in current dir

        ```text
        {{list_dir}}
        ```
    """
)


class TerminalCommand(BaseModel):
    valid_terminal_command: str


class SmartTerminal:
    def __init__(
        self, gpt_model: str, command_executor: CommandExecutor, console_printer: ConsolePrinter, chat_max_turns=10
    ):
        self.command_executor = command_executor
        self.console_printer = console_printer
        self.terminal_agent = Agent(
            gpt=GptOpenAI(model=gpt_model, output_format=TerminalCommand),
            chat_history=ChatHistory(max_turns=chat_max_turns),
            system_msg=SystemMsg(content=SYS_PROMPT),
        )

    def _run_and_print(self, cmd):
        completed_process = self.command_executor.execute_shell_cmd(cmd)
        self.console_printer.print_subprocess_output(completed_process)
        return completed_process

    def _suggest_command(self, cmd: str, completed_process: CompletedProcess, ctx: ConsoleContext):
        user_msg = USER_PROMPT.render(
            {
                "cmd": cmd,
                "stdout": completed_process.stdout,
                "stderr": completed_process.stderr,
                "return_code": completed_process.returncode,
                "list_dir": ctx.list_dir,
            }
        )
        response = self.terminal_agent.chat(UserMsg(content=user_msg))
        return response.content_parsed.valid_terminal_command

    def run(self, cmd: str, ctx: ConsoleContext):
        completed_process = self._run_and_print(cmd)
        if completed_process.returncode != 0:
            suggested_cmd = self._suggest_command(cmd=cmd, completed_process=completed_process, ctx=ctx)
            if suggested_cmd:
                self.console_printer.print("\n[bold red]Command failed.[/bold red]")
                self.console_printer.print(f"Suggested fix:\n  [bold green]{suggested_cmd}[/bold green]")
                self.console_printer.print("\n[cyan]Do you want to run the suggested command?[/cyan]")
                user_input = input("  [y/N]: ").strip()

                if user_input.strip().lower() == "y":
                    return suggested_cmd
