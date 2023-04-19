from client.src.clients import Client
from client.src.timer import Timer

from client.src.alarm import Alarm

class Scenarios:
    def __init__(self, client: Client):
        self.client = client
        self.timer = Timer()
        self.previous_TB_value: int = 0
        self.previous_hook_load_value: int = 0
        self.previous_SVP_value: int = 0

    def down_scenario_check(self):
        if all([
            self.client.parameters['Нагрузка на крюк'].loword == 0,
            self.client.parameters['Нагрузка на крюк'].loword == self.previous_hook_load_value
        ]):
            self.previous_hook_load_value = self.client.parameters['Положение таль блока'].loword
            self.previous_TB_value = self.client.parameters['Положение таль блока'].loword
            self.timer.start(2.5 * 60)
            if self.timer.check():
                Alarm.start()
        else:
            self.timer.stop()
