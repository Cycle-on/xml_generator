import csv
import time
from config import load_config
import requests
import threading
from config.config_data import *
from constants.sender import *

config = load_config()


def modify_xml_file_to_send(file_path: str, prefix_var_name: str, postfix_var_name: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        middle_file = [prefix_var_name]
        for row in f:
            middle_file.append(row)
        middle_file.append(postfix_var_name)
    with open(file_path, 'w+', encoding='utf-8') as f:
        f.writelines(middle_file)


def __send_file(region_name:str, filename: str, prefix:str):
    # print('ЗАТЫЧКА! - файл отправлен')
    # return
    headers = {
        "Content-Type": "application/xml",
    }

    file_data = open(os.path.join(config.output_directory_name,region_name,prefix, filename), 'r', encoding='utf-8').read()
    # print("send file_data", filename)
    session = requests.Session()
    session.auth = (SERVER_LOGIN, SERVER_PASSWORD)
    req = session.post(url=SERVER_ADDRESS, data=file_data, headers=headers)
    print(req.status_code)
    print(req.text)



def send_by_csv(csv_filename: str):
    file_path = csv_filename

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Используем DictReader для чтения в виде словарей
        for row in reader:
            filename = row['filename']
            if SENDER_WORK_TYPE == 'by_delay':
                while 1:
                    __send_file(filename)
                    time.sleep(SENDER_DELAY)
                    break
            elif SENDER_WORK_TYPE == 'by_date':
                date_send: datetime.datetime = datetime.datetime.strptime(row['dt_send'], '%Y-%m-%d %H:%M:%S.%f')
                while 1:
                    now = datetime.datetime.now()
                    if now >= date_send:
                        __send_file(filename)
                        break
                    time.sleep(0.5)


def send_along(region_name: str):
    csv_files_dir_path = os.path.join('files', files_prefix, region_name)
    thread1 = threading.Thread(target=lambda: send_by_csv(os.path.join(csv_files_dir_path, 'missed_calls_to_send.csv')))
    thread1.start()
    thread1.join()

    thread2 = threading.Thread(target=lambda: send_by_csv(os.path.join(csv_files_dir_path, 'ukios_to_send.csv')))
    thread2.start()
    thread2.join()


def main():
    send_along()


if __name__ == '__main__':
    main()
