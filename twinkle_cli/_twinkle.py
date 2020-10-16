from subprocess import Popen, PIPE
from multiprocessing import Process, Event


class Twinkle:
    """
    Twinkle CLI wrapper.

    Call run() before using any sip methods.
    """

    def __init__(self, cmd: list = None):
        if cmd is None:
            cmd = ['twinkle', '-c']
        self.cmd = cmd

        self.proc: Popen = None
        self.stdout_reader: Process = None

        self._stop_print_event = Event()

    def print_stdout(self) -> None:

        while True:
            if self._stop_print_event.is_set():
                break
            line = self.proc.stdout.readline()
            print(line.decode())

    def stop_print(self) -> None:
        self._stop_print_event.set()
        self.stdout_reader.join()

    def run(self) -> None:
        self.proc = Popen(
            self.cmd,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE
        )
        self.stdout_reader = Process(target=self.print_stdout)
        self.stdout_reader.start()

    def kill(self) -> None:
        self.stop_print()
        self.proc.kill()

    def send_command(self, command: str) -> None:
        self.proc.stdin.write(f'{command}\n'.encode())
        self.proc.stdin.flush()

    def stop_proc(self) -> None:
        self.send_command('quit')
        self.stop_print()
