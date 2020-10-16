from multiprocessing import Process, Event
from subprocess import Popen, PIPE
from typing import Iterator, List


class Twinkle:
    """
    Twinkle CLI wrapper.

    Call run() before using any sip methods.
    """

    def __init__(self, cmd: List[str] = None, debug=False):
        """

        :param cmd: a command to execute. defaults to ['twinkle', '-c']
        :param debug: print
        """

        if cmd is None:
            cmd = ['twinkle', '-c']
        self.cmd = cmd

        self.DEBUG = debug

        self.proc: Popen = None
        self.stdout_reader: Process = None

        self._stop_reading_event = Event()

    def read_stdout(self) -> Iterator:
        """Generator, yields one line from stdout."""

        while True:
            if self._stop_reading_event.is_set():
                break
            line = self.proc.stdout.readline().decode()

            yield line

    def stop_reading(self) -> None:
        """Ask stdout reader process to exit."""

        self._stop_reading_event.set()
        if self.stdout_reader.is_alive():
            self.stdout_reader.join()

    def parse_output(self) -> None:
        """Search for patterns in twinkle output and call needed callbacks."""

        for line in self.read_stdout():
            if self.DEBUG:
                print(line)

    def run(self) -> None:
        """Start Twinkle and stdout reader processes."""
        self._stop_reading_event.clear()

        self.proc = Popen(
            self.cmd,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE
        )
        self.stdout_reader = Process(target=self.parse_output)
        self.stdout_reader.start()

    def send_command(self, command: str) -> None:
        """Send any string to stdin then line break."""

        self.proc.stdin.write(f'{command}\n'.encode())
        self.proc.stdin.flush()

    def stop_twinkle(self) -> None:
        """Send 'quit' to Twinkle CLI."""

        self.send_command('quit')
        self.stop_reading()

    ###############
    # SIP Methods #
    ###############

    def call(self, dst: str) -> None:
        self.send_command(f'call {dst}')

    def answer(self) -> None:
        raise NotImplementedError

    def answerbye(self) -> None:
        raise NotImplementedError

    def reject(self) -> None:
        raise NotImplementedError

    def redirect(self, dst: str) -> None:
        raise NotImplementedError

    def transfer(self, dst: str) -> None:
        raise NotImplementedError

    def bye(self) -> None:
        self.send_command('bye')

    def hold(self) -> None:
        raise NotImplementedError

    def retrieve(self) -> None:
        raise NotImplementedError

    def conference(self) -> None:
        raise NotImplementedError

    def mute(self) -> None:
        raise NotImplementedError

    def dtmf(self, digits: str) -> None:
        self.send_command(f'dtmf {digits}')

    def redial(self) -> None:
        raise NotImplementedError

    def register(self) -> None:
        raise NotImplementedError

    def deregister(self) -> None:
        raise NotImplementedError

    def fetch_reg(self) -> None:
        raise NotImplementedError

    def options(self) -> None:
        raise NotImplementedError

    def line(self, number: int = None) -> None:
        raise NotImplementedError

    def dnd(self) -> None:
        raise NotImplementedError

    def auto_answer(self) -> None:
        raise NotImplementedError

    def user(self) -> None:
        raise NotImplementedError

    def zrtp(self) -> None:
        raise NotImplementedError

    def message(self, dst: int, text: str) -> None:
        raise NotImplementedError

    def presence(self) -> None:
        raise NotImplementedError
