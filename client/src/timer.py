import time
from loguru import logger


class Timer:
    def __init__(self):
        self.is_started = False
        self.start_time: float
        self.seconds: int

    def start(self, seconds):
        if not self.is_started:
            self.is_started = True
            self.seconds = seconds
            self.start_time = time.time()
            logger.info(f'Таймер запущен')

    def check(self):
        if self.is_started:
            return time.time() >= self.start_time + self.seconds

    def restart(self, seconds=None):
        if self.is_started:
            if seconds:
                self.seconds = seconds
            self.start_time = time.time()
            logger.info(f'Таймер перезапущен')

    def stop(self):
        if self.is_started:
            self.is_started = False
            self.seconds = None
            self.start_time = None
            logger.info(f'Таймер остановлен')
