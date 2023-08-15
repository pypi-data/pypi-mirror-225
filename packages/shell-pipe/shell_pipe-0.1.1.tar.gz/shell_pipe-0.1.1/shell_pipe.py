#!/usr/bin/python

import subprocess

__version__ = '0.1.1'

class ShellPipe:
    def __init__(self, needDebug=None):
        self.needDebug = needDebug
        self.lastCmdProcess = None

    def __or__(self, rightCmd : str):
        self._call_process(rightCmd)
        return self

    def __ror__(self, leftCmd):
        self._call_process(leftCmd)
        return self
    
    def _call_process(self, cmd : str):
        stdin = None
        if self.lastCmdProcess != None:
            stdin = self.lastCmdProcess.stdout
        self.lastCmdProcess = subprocess.Popen(cmd, shell=True, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def communicate(self):
        stdout, stderr = self.lastCmdProcess.communicate()
        self.lastCmdProcess = None
        return stdout.decode(), stderr.decode()
        
    


if __name__ == "__main__":
    import sys
    lib = sys.argv[1]

    p=ShellPipe()

    # |p| 模拟 Shell中的 管道线 |
    p = f"ldd {lib}" |p| f'egrep -o "/.* "'

    lddStdout, _ = p.communicate()
