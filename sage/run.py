import argparse
import queue
import signal
import sys
import threading

from sage.api.data import Data, DataType
from sage.aplayer.player import Player
from sage.asr.kaldi import Kaldi
from sage.bot import CalculatorBot
from sage.cfg.grammar import Calculator
from sage.cfg.parser import ResultParser, EqParser
from sage.io.socket import SocketIO
from sage.io.terminal import TerminalInput, TerminalOutput
from sage.io.voice import VoiceOutput
from sage.latex.wrapper import LatexWrapper
from sage.logger import logger
from sage.tts.intelektika import IntelektikaTTS


class Runner:
    def __init__(self, bot, audio_rec):
        logger.info("Init runner")
        self.__bot = bot
        self.__outputs = []
        self.__input_queue: queue.Queue[Data] = queue.Queue(maxsize=500)
        self.__output_queue: queue.Queue[Data] = queue.Queue(maxsize=500)
        self.__audio_rec = audio_rec

    def start(self):
        self.start_output()
        while True:
            inp = self.__input_queue.get()
            if inp is None:
                break
            if inp.type == DataType.TEXT:
                self.__bot.process(inp.data)
            elif inp.type == DataType.AUDIO:
                logger.info("got audio %d" % len(inp.data))
                self.__audio_rec.add(inp.data)
            elif inp.type == DataType.EVENT:
                logger.info("got event %s" % inp.data)
                self.__audio_rec.event(inp.data)
            else:
                logger.warning("Don't know what to do with %s data" % inp.type)
        logger.info("Exit run loop")

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

    def stop(self):
        self.__input_queue.put(None)


def main(param):
    parser = argparse.ArgumentParser(description="This app starts voice to voice bot",
                                     epilog="" + sys.argv[0] + "",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--tts_key", nargs='?', default='intelektika', help="TTS key")
    parser.add_argument("--useAudioPlayer", default=False, action=argparse.BooleanOptionalAction,
                        help="Use audio player for audio input data processing")
    parser.add_argument("--latex_url", nargs='?', default='http://localhost:5030/renderLatex',
                        help="URL of Latex equation maker")
    parser.add_argument("--port", nargs='?', default=8007, help="Service port for socketio clients")
    args = parser.parse_args(args=param)

    def out_func(d: Data):
        runner.add_output(d)

    if args.useAudioPlayer:
        rec = Player()
    else:
        rec = Kaldi(msg_func=out_func)

    runner = Runner(
        bot=CalculatorBot(out_func=out_func, cfg=Calculator(file="data/calc/grammar.cfg"), parser=ResultParser(),
                          eq_parser=EqParser(), eq_maker=LatexWrapper(url=args.latex_url)),
        audio_rec=rec)

    def in_func(d: Data):
        runner.add_input(d)

    workers = []

    def start_thread(method):
        thread = threading.Thread(target=method, daemon=True)
        thread.start()
        workers.append(thread)

    terminal = TerminalInput(msg_func=in_func)
    threading.Thread(target=terminal.start, daemon=True).start()

    start_thread(rec.start)

    ws_service = SocketIO(msg_func=in_func, port=args.port)
    start_thread(ws_service.start)

    terminal_out = TerminalOutput()
    runner.add_output_processor(terminal_out.process)
    runner.add_output_processor(ws_service.process)

    tts = IntelektikaTTS(url="https://sinteze-test.intelektika.lt/synthesis.service/prod/synthesize", key=args.tts_key,
                         voice="laimis")
    voice_out = VoiceOutput(tts=tts)
    runner.add_output_processor(voice_out.process)

    exit_c = 0

    def stop_runner(signum, frame):
        nonlocal exit_c
        if exit_c == 0:
            rec.stop()
            ws_service.stop()
            runner.stop()
        else:
            exit(1)
        exit_c = exit_c + 1

    signal.signal(signal.SIGINT, stop_runner)

    runner.start()
    for w in workers:
        w.join()
    logger.info("Exit sage")


if __name__ == "__main__":
    logger.info("Starting Sage")
    main(sys.argv[1:])
