from time import sleep

from pyModbusTCP.client import ModbusClient
from loguru import logger

from client.src.alarm import Alarm
from client.src.parameters import Parameter, INFO
from client.src.scenarios import Scenarios


class Client:
    def __init__(self, host: str, port: int, unit_id: int) -> None:
        logger.info('Клиент запускается')
        self.unit_id: int = unit_id
        self.connection = ModbusClient(host=host, port=port, unit_id=self.unit_id)
        self.amount_of_sensors: int
        self.parameters_info = INFO
        self.parameters: dict[str, Parameter] = {}
        self.scenario_checker: Scenarios = Scenarios(self)

    def open_client(self) -> bool:
        logger.info('Открываем соединение')
        return self.connection.open()

    def get_amount_of_sensors(self):
        return self.connection.read_holding_registers(255)[0]

    def check_data_registers(self):
        self.amount_of_sensors = self.get_amount_of_sensors()
        logger.info('Сбор регистров датчиков')
        for index in range(self.amount_of_sensors):
            current_parameter = Parameter(self.connection, index)
            current_parameter.get_all_data()
            self.is_needed_parameter(current_parameter)
        logger.info('Сбор закончен')

        self.check_needed()

    def check_needed(self):
        wrong_amount = False
        for parameter in self.parameters_info.values():
            if parameter not in self.parameters.keys():
                wrong_amount = True
                logger.error(f'Не хватает {parameter}')

        if wrong_amount:
            Alarm.test('wrong parameters amount')

    def is_needed_parameter(self, current_parameter):
        if current_parameter.id in self.parameters_info.keys():
            current_parameter.name = self.parameters_info[current_parameter.id]
            self.parameters[current_parameter.name] = current_parameter
            logger.debug(f"{current_parameter.name} -- есть")

    def print_data(self, first_time: bool = False):
        prev_parameters = [result.loword for result in self.parameters.values()]
        now_parameters = [result.get_loword() for result in self.parameters.values()]
        if first_time:
            logger.info(' | '.join(self.parameters.keys()))
        if prev_parameters != now_parameters or first_time:
            logger.info(' | '.join(str(p.get_loword()).center(len(p.name)) for p in self.parameters.values()))

    def start_polling(self, timeout=5):
        try:
            self.open_client()
            self.check_data_registers()
            self.print_data(first_time=True)
            while True:

                if self.amount_of_sensors != self.get_amount_of_sensors():
                    self.check_data_registers()
                    logger.info('Изменилось количество сенсоров!')

                self.print_data()

                self.scenario_checker.launch_scenarios()

                sleep(timeout)
        finally:
            self.connection.close()
            logger.info('Программа завершила работу')
