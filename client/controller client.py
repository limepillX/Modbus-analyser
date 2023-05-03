import os
from client.src.clients import Client
from loguru import logger
from dotenv import load_dotenv

HOST = os.getenv('IP')
PORT = os.getenv('PORT')


@logger.catch
def main():
    logger.add("logs/{time:YYYY-MM-DD}.log", rotation="12:00")
    client = Client(HOST, int(PORT), unit_id=206)
    client.start_polling(timeout=5)


if __name__ == '__main__':
    load_dotenv()
    main()
