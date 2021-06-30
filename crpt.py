
import subprocess

class Cryptor:
    def __init__(self, exe_path):
        self.exe_path = exe_path
        self.process = None
        self.stdin = None
        self.stdout = None
        self.interactions = 0

    def run(self):
        self.process = subprocess.Popen(args=self.exe_path, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self.stdout = self.process.stdout
        self.stdin = self.process.stdin

    def interact(self, c):
        self.interactions += 1
        #print("This is interactions ",self.interactions)
        line = '{0:x}\r\n'.format(c).encode()
        self.stdin.write(line)
        self.stdin.flush()
        time = int(self.stdout.readline())
        message = int(self.stdout.readline().strip(), 16)
        return message, time

    def close(self):
        if self.process:
            self.process.kill()