from subprocess import CompletedProcess, run


class CommandExecutor:
    @staticmethod
    def execute_console_cmd(cmd: str) -> CompletedProcess:
        return run(cmd, shell=True, text=True, capture_output=True)
