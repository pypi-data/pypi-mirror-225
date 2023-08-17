from threading import Thread


class Jobs:

    def __init__(self, count, task):
        self.__jobs = [Thread(target=task) for _ in range(count)]

    def start(self):
        for job in self.__jobs:
            job.start()

    def wait(self):
        for job in self.__jobs:
            job.join()

    def start_and_wait(self):
        self.start()
        self.wait()
