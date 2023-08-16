import multiprocessing as mp
from typing import Sequence, Any
from src.ppct.design_patterns import Factory
import time
from pathlib import Path
from src.ppct.line_reader import LineReader
from src.ppct.parallel import ParallelWorker


def work(sec:int):
    time.sleep(sec)
    return sec

def test():
    pw=ParallelWorker(workers=[work]*10)
    for _ in range(100):
        pw.input.put((1,))
    pw.finish_input()
    pw.wait()
    print('down')


if __name__ == '__main__':
    test()
