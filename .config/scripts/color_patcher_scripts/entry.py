import os

class Entry:
    path: str
    cmds: list[str]
    def __init__(self, path: str, cmds: list[str] | None = None):
        if not os.path.isfile(os.path.expanduser(path)):
            print(f'path {path} is not a file')
            return None
        if not cmds:
            cmds = []
        self.path = os.path.expanduser(path)
        self.cmds = []
        for cmd in cmds:
            self.cmds.append(cmd)
