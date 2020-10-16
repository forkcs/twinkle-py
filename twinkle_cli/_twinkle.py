from typing import Iterator, List
from subprocess import Popen, PIPE
from multiprocessing import Process, Event


class Twinkle:
    """
    Twinkle CLI wrapper.

    Call run() before using any sip methods.
    """

    def __init__(self, cmd: List[str] = None):
        """

        :param cmd: command to execute. defaults to ['twinkle', '-c']
        """

        if cmd is None:
            cmd = ['twinkle', '-c']
        self.cmd = cmd

        self.proc: Popen = None
        self.stdout_reader: Process = None

        self._stop_reading_event = Event()

    def read_stdout(self) -> Iterator:
        """Generator, yields one line from stdout."""

        while True:
            if self._stop_reading_event.is_set():
                break
            line = self.proc.stdout.readline()
            yield line.decode()

    def stop_reading(self) -> None:
        """Ask stdout reader process to exit."""

        self._stop_reading_event.set()
        self.stdout_reader.join()

    def run(self) -> None:
        """Start Twinkle and stdout reader processes."""
        self._stop_reading_event.clear()

        self.proc = Popen(
            self.cmd,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE
        )
        self.stdout_reader = Process(target=self.read_stdout)
        self.stdout_reader.start()

    def send_command(self, command: str) -> None:
        """Send any string to stdin then line break."""

        self.proc.stdin.write(f'{command}\n'.encode())
        self.proc.stdin.flush()

    def stop_twinkle(self) -> None:
        """Send 'quit' to Twinkle CLI."""

        self.send_command('quit')
        self.stop_reading()
