import os
from subprocess import CompletedProcess, run


class CommandExecutor:
    @staticmethod
    def execute_console_cmd(cmd: str) -> CompletedProcess:
        return run(cmd, shell=True, text=True, capture_output=True)

    @staticmethod
    def execute_cd_cmd(cmd: str) -> tuple[str, str]:
        path_arg = cmd[3:].strip()
        target_path = os.path.abspath(os.path.expanduser(path_arg))

        os.chdir(target_path)
        cwd = os.getcwd()

        logical_cwd = os.path.normpath(os.path.expanduser(path_arg))
        if not os.path.isabs(logical_cwd):
            logical_cwd = os.path.abspath(logical_cwd)

        return cwd, logical_cwd
