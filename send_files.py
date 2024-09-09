import csv
import datetime
import os
import time

from constants import SERVER_ADDRESS
from config import load_config
import requests
import threading

config = load_config()


def __send_file(filename: str):
    print(f'file {filename} was successfully send')
    return
    headers = {
        "password": SERVER_PASSWORD,
        "login": SERVER_LOGIN
    }
    with open(os.path.join('files', config.output_directory_name, filename), 'rb') as f:
        requests.post(SERVER_ADDRESS, headers=headers, files={filename: f})


def send_by_csv(csv_filename: str):
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
                    __send_file(filename)
                    break
                time.sleep(0.5)


def send_along():
    thread1 = threading.Thread(target=lambda: send_by_csv('calls_to_send.csv'))
    thread2 = threading.Thread(target=lambda: send_by_csv('ukios_to_send.csv'))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


def main():
    send_along()


if __name__ == '__main__':
    main()
