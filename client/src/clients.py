from pyModbusTCP.client import ModbusClient
from time import sleep

from client.src.parameters import Parameter, INFO
from client.src.logger import send_log


class Client:
    def __init__(self, host: str, port: int, unit_id: int) -> None:
        send_log('[#] Клиент запускается')
        self.unit_id: int = unit_id
        self.connection = ModbusClient(host=host, port=port, unit_id=self.unit_id)
        self.amount_of_sensors: int
        self.parameters_info = INFO
        self.parameters: dict[str, Parameter] = {}
        # self.manifold: Parameter
        # self.rotor: Parameter
        # self.VP_moment: Parameter
        # self.tal_block: Parameter
        # self.hook_load: Parameter

    def open_client(self) -> bool:
        send_log('[#] Открываем соединение')
        return self.connection.open()

    def get_amount_of_sensors(self):
        # send_log('[#] Проверяем кол-во активных датчиков')
        return self.connection.read_holding_registers(255)[0]

    def check_data_registers(self):
        self.amount_of_sensors = self.get_amount_of_sensors()
        send_log('[#] Сбор регистров датчиков')
        for index in range(self.amount_of_sensors):
            current_parameter = Parameter(self.connection, index)
            current_parameter.get_all_data()
            self.is_needed_parameter(current_parameter)
        send_log('[#] Сбор закончен')

        self.check_needed()

    def check_needed(self):
        for parameter in self.parameters_info.values():
            if parameter not in self.parameters.keys():
                send_log(f'[#] Не хватает {parameter}')

    def is_needed_parameter(self, current_parameter):
        if current_parameter.id in self.parameters_info.keys():
            current_parameter.name = self.parameters_info[current_parameter.id]
            self.parameters[current_parameter.name] = current_parameter
            print(f"{current_parameter.name} -- есть")

    def print_data(self, first_time: bool = False):
        prev_parameters = [result.loword for result in self.parameters.values()]
        now_parameters = [result.get_loword() for result in self.parameters.values()]
        if first_time:
            send_log(' | '.join(self.parameters.keys()))
        if prev_parameters != now_parameters or first_time:
            send_log(' | '.join(str(p.get_loword()).center(len(p.name)) for p in self.parameters.values()))

    def get_scenarios(self):
        return 1

    def start_polling(self, timeout=5):
        try:
            self.open_client()
            self.check_data_registers()
            self.print_data(first_time=True)
            while True:

                if self.amount_of_sensors != self.get_amount_of_sensors():
                    self.check_data_registers()
                    send_log('Изменилось количество сенсоров!')

                self.print_data()

                sleep(timeout)
        finally:
            self.connection.close()
            send_log('Программа завершила работу')
