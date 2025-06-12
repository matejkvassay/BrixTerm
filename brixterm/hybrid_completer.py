import os

from prompt_toolkit.completion import Completer, Completion, PathCompleter, WordCompleter
from prompt_toolkit.document import Document


class HybridCompleter(Completer):
    def __init__(self):
        self.dir_completer = PathCompleter(expanduser=True, only_directories=True)
        self.file_completer = PathCompleter(expanduser=True, only_directories=False)
        paths = os.environ.get("PATH", "").split(os.pathsep)
        cmds = set()
        for p in paths:
            if os.path.isdir(p):
                for name in os.listdir(p):
                    full = os.path.join(p, name)
                    if os.access(full, os.X_OK) and not os.path.isdir(full):
                        cmds.add(name)
        self.command_completer = WordCompleter(sorted(cmds), ignore_case=True)

    def get_completions(self, document: Document, complete_event):
        text = document.text_before_cursor
        tokens = text.split(" ")
        current = tokens[-1]

        if len(tokens) == 1:
            if current.startswith(("./", "/", "~")):
                sub = Document(current, cursor_position=len(current))
                for c in self.file_completer.get_completions(sub, complete_event):
                    yield Completion(c.text, c.start_position, display=c.display)
            else:
                yield from self.command_completer.get_completions(document, complete_event)

        else:
            cmd = tokens[0]
            comp = self.dir_completer if cmd == "cd" else self.file_completer
            sub = Document(current, cursor_position=len(current))
            for c in comp.get_completions(sub, complete_event):
                yield Completion(c.text, c.start_position, display=c.display)
