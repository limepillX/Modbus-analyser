from enum import Enum
from loguru import logger
from client.src.timer import Timer
from client.src.alarm import Alarm


class Scenario(Enum):
    DOWN = 1,
    UP = 2


class Scenarios:
    def __init__(self, client):
        self.client = client
        self.timer_delay = 20
        self.timer = Timer()
        self.previous_TB_value: int = 0
        self.previous_hook_load_value: int = 0
        self.previous_SVP_value: int = 0
        self.second_point = False

    def __renew_prev_values(self):
        self.previous_hook_load_value = self.client.parameters['Нагрузка на крюк'].loword
        self.previous_TB_value = self.client.parameters['Положение таль блока'].loword
        self.previous_SVP_value = self.client.parameters['ВП обороты'].loword

    def __get_scenarios(self):
        # TODO: Общение с бэкэндом
        return Scenario.DOWN

    def launch_scenarios(self):
        if self.__get_scenarios() == Scenario.DOWN:
            self.__down_scenario_check()
        elif self.__get_scenarios() == Scenario.UP:
            self.__up_scenario_check()

    def __is_moving(self):
        # TODO: Добавить погрешность
        return self.client.parameters['Положение таль блока'].loword != self.previous_TB_value

    def __is_rotating(self):
        # TODO: Добавить погрешность
        rotation = self.client.parameters['ВП обороты'].loword
        if 0 < rotation < 10:
            return 0
        return rotation

    def __get_hook_load(self):
        load = self.client.parameters['Нагрузка на крюк'].loword
        # TODO: Добавить погрешность
        if 0 < load < 10:
            return 0
        return load

    def __down_scenario_check(self):
        # TODO: Сигналы о неисправности если не фиксируется один из параметров
        if all([
            not self.__is_moving(),  # Нет движения
            not self.__get_hook_load(),  # Отсутствует вес
        ]):
            self.timer.start(self.timer_delay)
            if self.timer.check():
                Alarm.start('down scenario')

        else:
            self.timer.stop()

        self.__renew_prev_values()

    def __up_scenario_check(self):
        if all([
            self.__is_rotating(),  # Фиксирует вращение
            not self.__get_hook_load(),  # Отсутствует вес
            not self.__is_moving(),  # Нет движения
        ]):

            self.timer.start(self.timer_delay)

            if self.second_point:
                self.timer.stop()
                self.second_point = False

        elif all([
            self.timer.is_started,
            not self.__is_rotating(),  # Нет вращения
            200 < self.__get_hook_load() < 300,  # Вес ~250КГ
            self.__is_moving(),  # Фиксирует движение
        ]):
            logger.debug('Вторая точка активна')
            self.second_point = True

        elif all([
            self.timer.check(),
            not self.__is_rotating(),  # Нет вращения
            not self.__get_hook_load(),  # Отсутствует вес
            not self.__is_moving(),  # Нет движения
        ]):
            Alarm.start('up scenario')

        elif all([
            not self.__is_rotating(),  # Нет вращения
            self.__get_hook_load() > 1000,  # Вес больше 1Т
            self.__is_moving()  # Фиксирует движение
        ]):
            self.second_point = False
            self.timer.stop()

        self.__renew_prev_values()
