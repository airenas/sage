import argparse
import queue
import signal
import sys
import threading

from sage.api.data import Data, DataType
from sage.bot import CalculatorBot
from sage.cfg.grammar import Calculator
from sage.cfg.parser import ResultParser
from sage.io.terminal import TerminalInput, TerminalOutput
from sage.io.voice import VoiceOutput
from sage.logger import logger
from sage.tts.intelektika import IntelektikaTTS


class Runner:
    def __init__(self, bot):
        logger.info("Init runner")
        self.__bot = bot
        self.__outputs = []
        self.__input_queue: queue.Queue[Data] = queue.Queue(maxsize=500)
        self.__output_queue: queue.Queue[Data] = queue.Queue(maxsize=500)

    def start(self):
        self.start_output()
        while True:
            inp = self.__input_queue.get()
            if inp.type == DataType.TEXT:
                self.__bot.process(inp.data)
            else:
                logger.warning("Don't know what to do with %s data" % inp.type)

    def start_output(self):
        def run():
            while True:
                inp = self.__output_queue.get()
                for out_proc in self.__outputs:
                    out_proc(inp)

        threading.Thread(target=run, daemon=True).start()

    def add_input(self, d: Data):
        self.__input_queue.put(d)

    def add_output(self, d: Data):
        self.__output_queue.put(d)

    def add_output_processor(self, proc):
        self.__outputs.append(proc)


def handler(signum, frame):
    logger.info("Exit sage")
    exit(0)


def main(param):
    parser = argparse.ArgumentParser(description="This app starts voice to voice bot",
                                     epilog="" + sys.argv[0] + "",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--tts_key", nargs='?', default='intelektika', help="TTS key")
    args = parser.parse_args(args=param)

    signal.signal(signal.SIGINT, handler)

    def out_func(d: Data):
        runner.add_output(d)

    runner = Runner(
        bot=CalculatorBot(out_func=out_func, cfg=Calculator(file="data/calc/grammar.cfg"), parser=ResultParser()))

    def in_func(d: Data):
        runner.add_input(d)

    terminal = TerminalInput(msg_func=in_func)
    threading.Thread(target=terminal.start, daemon=True).start()

    terminal_out = TerminalOutput()
    runner.add_output_processor(terminal_out.process)

    tts = IntelektikaTTS(url="https://sinteze-test.intelektika.lt/synthesis.service/prod/synthesize", key=args.tts_key,
                         voice="laimis")
    voice_out = VoiceOutput(tts=tts)
    runner.add_output_processor(voice_out.process)

    runner.start()


if __name__ == "__main__":
    logger.info("Starting Sage")
    main(sys.argv[1:])
