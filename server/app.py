from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
import logging

app = Flask(__name__)

# Определите путь для файлов журнала
log_file_path = '../temporary_logs'


@app.route('/')
def index():
    # Отображение лог-файла на странице сайта
    return render_template('index.html')


@app.route('/api/sendlog')
def send_log():
    date = request.args.get('date')
    time = request.args.get('time')
    body = request.args.get('body')
    importance = request.args.get('importance')

    if not all([date, time, body, importance]):
        return 'error, missing parameters'

    with open(f'{datetime.now().date()}_logs.txt', 'r+') as f:
        prev_text = f.read()
        f.write(f'{date}|{time}|{body}|{importance}'.rstrip('\r\n') + '\n' + prev_text)

    return 'ok'


@app.route('/api/get_logs')
def get_logs():
    result = dict()
    with open(log_file_path, 'r') as f:
        logs = f.readlines(40)

    for idx, log in logs:
        result[idx] = str(log)

    return jsonify(result)


if __name__ == '__main__':
    app.run()
