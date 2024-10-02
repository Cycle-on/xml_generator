from datetime import timedelta as td
from config import load_config, ukios_info, missed_info
from config.config_data import *
from file_creator import create_file_from_model, create_send_info_csv_files
from generators.incident_type_generator.incident_type_generator import create_incident_type_file
from generators.operators_and_arms import create_operators, create_arm_ops_files
from generators.ukio_generator import generate_ukio_phone_call_data
from config.dirs import create_dirs
from google_sheet_parser.parse_addresses import fill_addresses
from google_sheet_parser.parse_incident_types import fill_incident_type_lists
from schemas.phonecall import MissedCall, MissedCalls
from schemas.ukio_model import Ukios, Ukio
from config.config_data import DATE_ZERO
from send_files import send_along
import argparse
import constants

config = load_config()

"""
Не забудь заменить запросы в гугл таблице
"""


def parse_args():
    parser = argparse.ArgumentParser()
    # Добавляем параметры со значениями по умолчанию
    parser.add_argument('--files-count', type=int, default=1, help='количество файлов')
    parser.add_argument('--xmls', type=int, default=100, help='Количество документов в одном файле')
    parser.add_argument('--send', action='store_true', help='Режим генератора')
    parser.add_argument('--date', type=str, default=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
                        help='Дата в формате: YYYY-MM-DD_HH-MM-SS')

    # Парсим аргументы
    args = parser.parse_args()
    constants.files_count = args.files_count
    constants.xml_count_per_file = args.xmls
    send_files: bool = args.send
    constants.DATE_ZERO_FORMAT = args.date

    return send_files


def main(date_zero=DATE_ZERO):
    send_files: bool = parse_args()
    create_dirs()
    create_operators()
    ukios_list = []
    missed_list = []
    dt_start = datetime.datetime.now()
    models_create_time = None
    # fill with the Google sheets
    fill_incident_type_lists()
    fill_addresses()

    print("заполнил incident types")
    for i in range(config.files_count):
        for _ in range(xml_count_per_file):

            u = generate_ukio_phone_call_data(date_zero)
            date_zero += td(seconds=AVG_DELAY_BETWEEN_CALLS_TIME)
            if u is not None:
                if isinstance(u, Ukio):
                    ukios_list.append(u)
                    ukios_info[-1]['filename'] = f'ukios_{i}.xml'
                elif isinstance(u, MissedCall):
                    missed_list.append(u)
                    missed_info[-1]['filename'] = f'missed_{i}.xml'

        ukios = Ukios(
            Ukios=ukios_list
        )
        missed = MissedCalls(
            missedCalls=missed_list
        )

        ukios_list = []
        models_create_time = datetime.datetime.now() - dt_start
        # print("models done", models_create_time)
        create_file_from_model(ukios, filename=f'ukios_{i}', basename="Ukios")
        create_file_from_model(missed, filename=f'missed_{i}', basename='MissedCalls')
        create_arm_ops_files()
        create_incident_type_file()
    print("finish time", datetime.datetime.now() - dt_start)

    if send_files:
        print("start send files")
        if create_send_info_csv_files('missed_calls_to_send', missed_info) is False:
            pass
        create_send_info_csv_files('ukios_to_send', ukios_info)
        send_along()


if __name__ == '__main__':
    main()
