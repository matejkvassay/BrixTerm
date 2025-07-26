import json
from collections import deque
from subprocess import CompletedProcess


class CommandHistory:
    def __init__(self, size: int = 5):
        self.hist = deque(maxlen=size)

    def add(self, completed_process: CompletedProcess):
        self.hist.append(completed_process)

    def to_json(self) -> str:
        serializable_cmds = [
            {"args": proc.args, "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
            for proc in self.hist
        ]
        return json.dumps(serializable_cmds)
