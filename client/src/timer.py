import time


class Timer:
    def __init__(self):
        self.start_time = None
        self.is_started = False
        self.start_time: float
        self.seconds: int

    def start(self, seconds):
        if not self.is_started:
            self.seconds = seconds
            self.start_time = time.time()
            print(f'[#] Таймер запущен в {self.start_time}')

    def check(self):
        if self.is_started:
            return time.time() >= self.start_time + self.seconds

    def restart(self, seconds=None):
        if self.is_started:
            if seconds:
                self.seconds = seconds
            self.start_time = time.time()
        else:
            print('[#] Таймер не был запущен')

    def stop(self):
        if self.is_started:
            self.is_started = False
            self.seconds = None
            self.start_time = None
        else:
            print('[#] Таймер и так не запущен')
