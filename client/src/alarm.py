from loguru import logger

class Alarm:
    @staticmethod
    def start(num=None):
        logger.error(f'Ошибка [{num}]')
        logger.debug('Бип буп бип бип')
