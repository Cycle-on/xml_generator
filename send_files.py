import csv
import time
from config import load_config
import requests
import threading
from config.config_data import *
from constants import *
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
    response = requests.post(
        url=config.url,
        headers=headers,
        data=file_data,
        verify=False
    )
    if response.status_code != 200:
        print(f"Error sending file {filename}: {response.status_code}")
        print(response.text)
    time.sleep(globals()['SENDER_DELAY'])


def send_by_csv(csv_filename: str):
    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            __send_file(row[0], row[1], row[2])


def send_along(region_name: str):
    for prefix in [globals()['UKIO_SOAP_PREFIX'], globals()['MISSED_SOAP_PREFIX'], globals()['ARMWORK_SOAP_PREFIX'], globals()['OPERATOR_WORK_SOAP_PREFIX'], globals()['INCIDENT_SOAP_PREFIX']]:
        for filename in os.listdir(os.path.join(config.output_directory_name,region_name,prefix)):
            __send_file(region_name, filename, prefix)


def main():
    pass


if __name__ == '__main__':
    main()
