import csv
import datetime
import os
import time

from constants import SERVER_ADDRESS
from config import load_config
import requests

config = load_config()


def send_file(filename: str):
    print(f'file {filename} was successfully send')
    return
    with open(os.path.join('files', config.output_directory_name, filename), 'rb') as f:
        requests.post(SERVER_ADDRESS, files={filename: f})


def check_time(csv_filename: str):
    # Укажите путь к вашему CSV файлу
    file_path = csv_filename

    # Открываем файл на чтение
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Используем DictReader для чтения в виде словарей
        for row in reader:
            filename = row['filename']
            date_send: datetime.datetime = datetime.datetime.strptime(row['dt_send'], '%Y-%m-%d %H:%M:%S.%f')

            while 1:
                now = datetime.datetime.now()
                if now >= date_send:
                    send_file(filename)
                    break
                time.sleep(0.5)


def main():
    check_time('calls_to_send.csv')


if __name__ == '__main__':
    main()
