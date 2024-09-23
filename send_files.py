import csv
import datetime
import os
import time

from constants import SERVER_ADDRESS
from config import load_config
import requests
import threading
from config.config_data import *

config = load_config()


def modify_xml_file_to_send(file_path: str):
    with open(file_path, 'r') as f:
        middle_file = ["""<?xml version="1.0" encoding="UTF-8"?> 
    <SOAP-ENV:Envelope 
     xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
     xmlns:ns1="s112"> 
     <SOAP-ENV:Body>"""]
        for row in f:
            middle_file.append(row)

        middle_file.append("""</SOAP-ENV:Body> 
    </SOAP-ENV:Envelope>""")
    with open(file_path, 'w+') as f:
        f.writelines(middle_file)


def __send_file(filename: str):
    # print(f'file {filename} was successfully send')
    headers = {

    }
    json = {
        "authentication":
            {
                "password": SERVER_PASSWORD,
                "username": SERVER_LOGIN,
            }

    }
    data1 = """<Ukios> 
    <Ukio> 
        <globalId>TEST_YYY</globalId> 
        <dtSend>2024-09-10T20:39:58.684566</dtSend> 
        <dtCreate>2024-09-10T20:39:35.684566</dtCreate> 
        <dtUpdate>2024-09-10T20:39:58.684566</dtUpdate> 
        <bHumanThreat>False</bHumanThreat> 
        <bChs>False</bChs> 
        <bWrong>False</bWrong> 
        <bChildPlay>False</bChildPlay> 
        <phoneCall> 
            <phoneCallId>393c4cbf-1a10-411c-84b4-efc3193d562f</phoneCallId> 
            <dtSend>2024-09-10T20:39:58.684566</dtSend> 
            <bOperatorIniciatied>False</bOperatorIniciatied> 
            <dtCall>2024-09-10T20:38:05</dtCall> 
            <dtConnect>2024-09-10T20:38:05.647146</dtConnect> 
            <bCallEnded>False</bCallEnded> 
            <aCallEnded>True</aCallEnded> 
            <dtEndCall>2024-09-10T20:39:14</dtEndCall> 
            <OperatorId>e7e96b1d-32a1-4240-ada4-50c7e9b5f968</OperatorId> 
        </phoneCall> 
        <phoneCall> 
            <phoneCallId>63ce549e-d141-4a22-96e6-6a5ef166f87a</phoneCallId> 
            <dtSend>2024-09-10T20:39:58.684566</dtSend> 
            <bOperatorIniciatied>True</bOperatorIniciatied> 
            <dtCall>2024-09-10T20:39:20.787909</dtCall> 
            <dtConnect>2024-09-10T20:39:35.684566</dtConnect> 
            <bCallEnded>True</bCallEnded> 
            <aCallEnded>False</aCallEnded> 
            <dtEndCall>2024-09-10T20:39:55.684566</dtEndCall> 
            <OperatorId>e7e96b1d-32a1-4240-ada4-50c7e9b5f968</OperatorId> 
        </phoneCall> 
        <callContent> 
            <callContentId>c6441205-b370-4083-b455-6a4a13e30bc1</callContentId> 
            <strLastName>Ефимов</strLastName> 
            <strName>Роман</strName> 
            <strMiddleName>Игоревич</strMiddleName> 
            <strCallerContactPhone>+7(964)-921-8599</strCallerContactPhone> 
            <strCgPN>+7(964)-921-8599</strCgPN> 
            <appResAddress>Хабаровский край, Солнечный район, ст. Горин</appResAddress> 
            <strLanguage>ru</strLanguage> 
            <strIncidentDescription>desc2</strIncidentDescription> 
            <appLocAddress>Хабаровский край, р-н Имени Полины Осипенко, в долине ручья Большие Сулаки</appLocAddress> 
        </callContent> 
        <address> 
            <addressId>0cf6342a-d164-4ded-9f6b-e12874f43855</addressId> 
            <strAddress>Промышленная улица, 19к1, Хабаровск</strAddress> 
            <geoLatitude>48.494561</geoLatitude> 
            <geoLongitude>135.104112</geoLongitude> 
            <strDistrict>железнодорожный район</strDistrict> 
            <strCity>Хабаровск</strCity> 
            <strStreet>Промышленная</strStreet> 
            <strHouse>19</strHouse> 
            <strCorps>1</strCorps> 
            <strCityKLADR>2701800000000</strCityKLADR> 
            <strCityFIAS>e037f0b4-b7cc-4a06-9a08-70c4bc429452</strCityFIAS> 
        </address> 
    </Ukio> 
</Ukios>"""
    res = open(os.path.join(config.output_directory_name, filename), 'r').read()
    data = """<?xml version="1.0" encoding="UTF-8"?> 
<SOAP-ENV:Envelope 
 xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
 xmlns:ns1="s112"> 
 <SOAP-ENV:Body>""" + data1 + """</SOAP-ENV:Body> 
</SOAP-ENV:Envelope>"""
    req = requests.post(url=SERVER_ADDRESS, json=json, data=data)
    print(req.status_code)
    print(req.text)


def send_by_csv(csv_filename: str):
    # Укажите путь к вашему CSV файлу
    file_path = csv_filename

    # Открываем файл на чтение
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Используем DictReader для чтения в виде словарей
        for row in reader:
            filename = row['filename']
            while 1:
                __send_file(filename)
                time.sleep(3)

            # date_send: datetime.datetime = datetime.datetime.strptime(row['dt_send'], '%Y-%m-%d %H:%M:%S.%f')
            # while 1:
            #     now = datetime.datetime.now()
            #     if now >= date_send:
            #         __send_file(filename)
            #         break
            #     time.sleep(0.5)


def send_along():
    # thread1 = threading.Thread(target=lambda: send_by_csv('missed_calls_to_send.csv'))
    # thread1.start()
    # thread1.join()

    thread2 = threading.Thread(target=lambda: send_by_csv('ukios_to_send.csv'))
    thread2.start()
    thread2.join()


def main():
    send_along()


if __name__ == '__main__':
    main()
