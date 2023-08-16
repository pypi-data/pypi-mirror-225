import multiprocessing as mp
from typing import Sequence, Callable


class ParallelWorker:
    """
    This class is used to execute a sequence of workers in parallel.
    :parameter workers: a sequence of callables
    :parameter queue_size: the size of the queues, default=0 (unlimited)
    :parameter ignore_output: if True, the output queue will not be filled
    """

    def __init__(self, workers: Sequence[Callable], queue_size: int = 0, ignore_output: bool = False):
        self.__workers = workers
        self.__parallel = len(workers)
        self.__ignore_output = ignore_output
        self.input = mp.Queue(maxsize=queue_size)
        self.output = mp.Queue(maxsize=queue_size)
        self.errors = mp.Queue(maxsize=queue_size)
        self.__processes: list[mp.Process] = []
        self.__start()

    def finish_input(self):
        """
        This method is used to signal the end of the input.
        :return:
        """
        for _ in range(self.__parallel):
            self.input.put(None)

    def kill(self):
        """
        This method is used to kill all the processes.
        :return:
        """
        for p in self.__processes:
            if p.is_alive():
                p.terminate()

    @property
    def is_running(self):
        """
        This property is used to check if the processes are still running.
        :return:
        """
        for p in self.__processes:
            if p.is_alive():
                return True
        return False

    def wait(self):
        """
        This method is used to wait for all processes to finish.
        :return:
        """
        for p in self.__processes:
            p.join()

    @staticmethod
    def _execute(intput_queue: mp.Queue,
                 output_queue: mp.Queue,
                 error_queue: mp.Queue,
                 worker: Callable,
                 ignore_output: bool):
        """
        This method is used to execute a worker.
        :return:
        """
        for args in iter(intput_queue.get, None):
            try:
                r = worker(*args)
                if not ignore_output:
                    output_queue.put((args, r))
            except Exception as e:
                error_queue.put((args, e))

    def __start(self):
        for worker in self.__workers:
            p = mp.Process(target=ParallelWorker._execute,
                           args=(self.input,
                                 self.output,
                                 self.errors,
                                 worker, self.__ignore_output))
            self.__processes.append(p)
            p.start()
