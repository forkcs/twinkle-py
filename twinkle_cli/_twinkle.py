from multiprocessing import Process, Event
from subprocess import Popen, PIPE
from typing import Iterator, List


class Twinkle:
    """
    Twinkle CLI wrapper.

    Call run() before using any sip methods.
    You can inherit from this class and redefine callbacks.

    Twinkle version: 1.10.2 - 14 February 2018
    """

    def __init__(self, cmd: List[str] = None, debug=False):
        """

        :param cmd: a command to execute. defaults to ['twinkle', '-c']
        :param debug: print Twinkle input to console
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
            if line == '':
                continue
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

    #############
    # Callbacks #
    #############

    def on_call(self) -> None:
        if self.DEBUG:
            print('on_call() was called.')

    ###############
    # SIP Methods #
    ###############

    def call(self, dst: str) -> None:
        self.send_command(f'call {dst}')

    def answer(self) -> None:
        self.send_command('answer')

    def answerbye(self) -> None:
        self.send_command('answerbye')

    def reject(self) -> None:
        self.send_command('reject')

    def redirect(self, dst: str) -> None:
        self.send_command(f'redirect {dst}')

    def transfer(self, dst: str) -> None:
        self.send_command(f'transfer {dst}')

    def bye(self) -> None:
        self.send_command('bye')

    def hold(self) -> None:
        self.send_command('hold')

    def retrieve(self) -> None:
        self.send_command('retrieve')

    def conference(self) -> None:
        self.send_command('conference')

    def mute(self) -> None:
        self.send_command('mute')

    def dtmf(self, digits: str) -> None:
        self.send_command(f'dtmf {digits}')

    def redial(self) -> None:
        self.send_command('redial')

    def register(self) -> None:
        self.send_command('register')

    def deregister(self) -> None:
        self.send_command('deregister')

    def fetch_reg(self) -> None:
        self.send_command('fetch_reg')

    def options(self, dst: str = None) -> None:
        if dst is None:
            dst = ''
        self.send_command(f'options {dst}')

    def line(self, number: int = None) -> None:
        if number is None:
            number = ''
        self.send_command(f'line {number}')

    def dnd(self) -> None:
        self.send_command('dnd')

    def auto_answer(self) -> None:
        self.send_command('auto_answer')

    def user(self, name: str = None) -> None:
        if name is None:
            name = ''
        self.send_command(f'user {name}')

    def zrtp(self, command: str) -> None:
        zrtp_commands = ['encrypt', 'go-clear', 'confirm-sas', 'reset-sas']
        if command not in zrtp_commands:
            raise ValueError(f'Invalid command. Avaliable commands are: {zrtp_commands}.')
        self.send_command(f'zrtp {command}')

    def message(self, dst: int, text: str) -> None:
        self.send_command(f'message {dst} "{text}"')

    def presence(self, state: str) -> None:
        self.send_command(f'presence {state}')
