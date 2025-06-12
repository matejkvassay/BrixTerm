import os

from prompt_toolkit.completion import Completer, Completion, PathCompleter, WordCompleter
from prompt_toolkit.document import Document


class HybridCompleter(Completer):
    def __init__(self):
        # Only directories (for `cd`)
        self.dir_completer = PathCompleter(expanduser=True, only_directories=True)
        # Both files & directories
        self.file_completer = PathCompleter(expanduser=True, only_directories=False)
        # Executables in $PATH for command names
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
        # Split into tokens; keep the last one for path completion
        tokens = text.split(" ")
        current = tokens[-1]

        # Are we at the very first token?
        if len(tokens) == 1:
            # If it looks like a path, do file completion
            if current.startswith(("./", "/", "~")):
                sub = Document(current, cursor_position=len(current))
                for c in self.file_completer.get_completions(sub, complete_event):
                    yield Completion(c.text, c.start_position, display=c.display)
            else:
                # Otherwise complete commands
                yield from self.command_completer.get_completions(document, complete_event)

        else:
            # Some argument after a command
            cmd = tokens[0]
            # Choose only-dirs for cd, else files+dirs
            comp = self.dir_completer if cmd == "cd" else self.file_completer
            sub = Document(current, cursor_position=len(current))
            for c in comp.get_completions(sub, complete_event):
                yield Completion(c.text, c.start_position, display=c.display)
