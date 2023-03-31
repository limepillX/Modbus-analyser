from pyModbusTCP.client import ModbusClient
from time import sleep
from datetime import datetime
import os

HOST = os.getenv('IP')
PORT = os.getenv('PORT')


def get_parameter(x):
    return 256 + (x * 10)


device_address = ['Адрес устройства на шине MODBUS', 11]
serial_number_controller = ['Серийный номер модуля управления', 12]
software_version = ['Версия встроенного программного обеспечения', 13]
tal_block = ['ПОЛОЖЕНИЕ ТАЛЬ-БЛОКА', get_parameter(6)]
hook_load = ['НАГРУЗКА НА КРЮК', get_parameter(7)]
pressure_pj_input = ['МОМЕНТ НА РОТОРЕ', get_parameter(18)]


def logger(func):
    def wrapper():
        try:
            send_log(f'Функция {func.__name__} начала работу')
            func()
        except BaseException as ex:
            send_log(f'{func.__name__}\terr->\t{type(ex).__name__}')
            exit('Shutting down...')
        else:
            send_log(f'Функция {func.__name__} завершила работу без ошибок')

    return wrapper


def send_log(text: str = ''):
    print(text)
    with open('temporary_logs', 'a+') as f:
        if text:
            f.write(f'[#]{str(datetime.now())[:-7]}\t{text}\n')
        else:
            f.write('\n')


@logger
def start_client():
    client = ModbusClient(host=HOST, port=int(PORT), unit_id=206)
    state = None
    try:
        send_log('Клиент запускается...')
        client.open()
        send_log('Клиент запущен')

        to_get = hook_load

        while True:
            if state != client.read_holding_registers(to_get[1]):
                state = client.read_holding_registers(to_get[1])
                send_log(f'Запрос: {to_get}')
                send_log(f'Ответ: {to_get[0]} = {",".join([str(i) for i in state])}')

            sleep(5)

    finally:
        client.close()


if __name__ == '__main__':
    send_log()
    start_client()
