INFO = {
    '0x104': 'Манифольд',
    '0x100': 'Нагрузка на крюк',
    '0x14e': 'Положение таль блока',
    '0x14a': 'Ротор момент',
    '0x15c': 'ВП обороты'
}


class Parameter:
    def __init__(self, client, number):
        self.name = ''
        self.client = client
        self.number = number
        self.id = None
        self.hiword = None
        self.loword = None

    def get_id(self) -> str:
        self.id = hex(self.client.read_holding_registers(256 + (self.number * 10))[0])
        return self.id

    def get_hiword(self):
        self.hiword = self.client.read_holding_registers(256 + (self.number * 10) + 6)[0]
        return self.hiword

    def get_loword(self):
        self.loword = self.client.read_holding_registers(256 + (self.number * 10) + 7)[0]
        return self.loword

    def get_all_data(self) -> None:
        self.get_id()
        self.get_hiword()
        self.get_loword()
