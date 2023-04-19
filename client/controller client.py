import os
from client.src.clients import Client

HOST = os.getenv('IP')
PORT = os.getenv('PORT')


def main():
    client = Client(HOST, int(PORT), unit_id=206)
    client.start_polling(timeout=5)


if __name__ == '__main__':
    main()
