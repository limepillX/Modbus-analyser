from datetime import datetime


def send_log(text: str = ''):
    print(text)
    with open(f'logs/{datetime.now().date()} - logs.log', 'a+') as f:
        if text:
            f.write(f'[#]{str(datetime.now())[:-7]}\t{text}\n')
        else:
            f.write('\n')


def logger(func):
    def wrapper(args):
        try:
            send_log(f'Функция {func.__name__} начала работу')
            func(args)
        except BaseException as ex:
            send_log(f'{func.__name__}\terr->\t{type(ex).__name__}')
            raise ex
        else:
            send_log(f'Функция {func.__name__} завершила работу без ошибок')

    return wrapper
