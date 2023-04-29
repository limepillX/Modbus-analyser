import csv
from time import sleep
from loguru import logger
from client.src.scenarios import Scenarios

TEST_FILE = 'test_down_1.csv'


class Parameter:
    def __init__(self):
        self.hiword = None
        self.loword = None


class Client:
    def __init__(self):
        self.parameters: dict[str, Parameter] = {}

    def print_data(self, first_time: bool = False):
        names = ['ВП обороты', 'Нагрузка на крюк', 'Положение ТБ']
        if first_time:
            logger.info(' | '.join(name.center(len(names[1])) for name in names))
        else:
            logger.info(' | '.join(str(p.loword).center(len(names[1])) for p in self.parameters.values()))


def get_next_values():
    with open(TEST_FILE, 'r') as file:
        reader = file.readlines()[1:]
        for row in reader:
            row_data = row.strip().split(';')
            for _ in range(int(row_data[0])):
                yield row_data[1:]


if __name__ == '__main__':
    client = Client()
    gen = get_next_values()
    scenario_checker = Scenarios(client)

    client.print_data(first_time=True)
    client.parameters['ВП обороты'] = Parameter()
    client.parameters['Нагрузка на крюк'] = Parameter()
    client.parameters['Положение таль блока'] = Parameter()

    while True:
        data = next(gen)
        client.parameters['ВП обороты'].loword = int(data[0])
        client.parameters['Нагрузка на крюк'].loword = int(data[1])
        client.parameters['Положение таль блока'].loword = int(data[2])
        client.print_data()
        scenario_checker.launch_scenarios()

        sleep(1)
