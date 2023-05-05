from enum import Enum

from loguru import logger


class AlarmSounds(Enum):
    DOWN = 'client/audios/down.wav',
    UP = 'client/audios/up.wav',
    PARAMETERS = 'client/audios/parameters.wav',


class Alarm:
    @staticmethod
    def make_test(num: AlarmSounds):
        logger.error(f'Нарушение [{num.name}]')
        logger.debug('Вызвана сигнализация')

    @staticmethod
    def make_alarm(file_path: AlarmSounds):
        import RPi.GPIO as GPIO
        import os
        import time

        logger.error(f'Нарушение [{file_path.name}]')
        path_to_file = os.path.abspath(file_path.value[0])

        logger.debug(path_to_file)
        relay_pin = 23
        logger.debug(f'Используем пин под номером {relay_pin}')

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(relay_pin, GPIO.OUT)
        logger.debug('GPIO initialized')

        GPIO.output(relay_pin, GPIO.HIGH)
        logger.debug('rele turned ON')

        os.system(f'mpg321 {path_to_file}')
        logger.debug('audio file started')

        time.sleep(5)
        logger.debug('file finished')

        GPIO.output(relay_pin, GPIO.LOW)
        logger.debug('rele turned OFF')

        # Выключение библиотеки RPi.GPIO
        GPIO.cleanup()
        logger.debug('cleaning up')
