import dataclasses

from pyModbusTCP.client import ModbusClient
from time import sleep
from datetime import datetime
import os

HOST = os.getenv('IP')
PORT = os.getenv('PORT')


class Parameter:
    def __init__(self, number):
        self.number = number
        self.id = None
        self.hiword = None
        self.loword = None

    def get_id(self, client):
        print(client.read_holding_registers(256 + (self.number * 10)))
        self.id = hex(client.read_holding_registers(256 + (self.number * 10))[0])
        return self.id

    def get_hiword(self, client):
        self.hiword = client.read_holding_registers(256 + (self.number * 10) + 6)[0]
        return self.hiword

    def get_loword(self, client):
        self.loword = client.read_holding_registers(256 + (self.number * 10) + 7)[0]
        return self.loword


device_address = ['Адрес устройства на шине MODBUS', 11]
serial_number_controller = ['Серийный номер модуля управления', 12]
software_version = ['Версия встроенного программного обеспечения', 13]


def logger(func):
    def wrapper():
        try:
            send_log(f'Функция {func.__name__} начала работу')
            func()
        except BaseException as ex:
            send_log(f'{func.__name__}\terr->\t{type(ex).__name__}')
            raise ex
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
    hiword = None
    loword = None
    try:
        send_log('Клиент запускается...')
        client.open()
        send_log('Клиент запущен')

        # to_get = tal_block
        # curr = Parameter(11)
        # while True:
        #     curr.get_id(client)
        #     curr.get_hiword(client)
        #     curr.get_loword(client)
        #     if hiword != curr.hiword or loword != curr.loword:
        #         hiword = curr.hiword
        #         loword = curr.loword
        #         send_log(f'{curr.id} | {curr.loword} | {curr.loword}')
        #
        #     sleep(5)
        for i in range(40):
            curr = Parameter(i)
            curr.get_id(client)
            curr.get_hiword(client)
            curr.get_loword(client)
            if curr.hiword != 65535:
                print(f'{curr.number} - {curr.id} - {curr.hiword} - {curr.loword}')
            else:
                print(f'{curr.number} - не работает')
    finally:
        client.close()


if __name__ == '__main__':
    send_log()
    start_client()
