from datetime import timedelta as td
from config import load_config, ukios_info, missed_info
from config.config_data import *
from constants.constants_remaker import get_next_constants
from file_creator import create_file_from_model, create_send_info_csv_files, prepare_files_to_send
from generators.operators_and_arms import ARM_WORK, OPERATOR_WORK, create_arms_and_operators
from generators.ukio_generator import generate_ukio_phone_call_data
from config.dirs import create_dirs, clear_dir
from google_sheet_parser.parse_addresses import fill_addresses, ADDRESSES
from google_sheet_parser.parse_incident_types import fill_incident_type_lists, INCIDENT_TYPES_LIST
from schemas.phonecall import MissedCall, MissedCalls
from schemas.string_eos import OperatorWorks, ArmWorks, IncidentTypes
from schemas.ukio_model import Ukios, Ukio
from config.config_data import DATE_ZERO
from send_files import send_along, modify_xml_file_to_send
import argparse
from constants import generator
from wsdl_parser.wsdl_tester import check_fields_by_file_path

config = load_config()


def parse_args():
    parser = argparse.ArgumentParser()
    # Добавляем параметры со значениями по умолчанию
    parser.add_argument('--files-count', type=int, default=generator.files_count, help='количество файлов')
    parser.add_argument('--xmls', type=int, default=generator.xml_count_per_file,
                        help='Количество документов в одном файле')
    parser.add_argument('--send', action='store_true', help='Режим генератора')
    parser.add_argument('--date', type=str, default=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
                        help='Дата в формате: YYYY-MM-DD_HH-MM-SS')

    # Парсим аргументы
    args = parser.parse_args()
    generator.files_count = args.files_count
    generator.xml_count_per_file = args.xmls
    send_files: bool = args.send
    generator.DATE_ZERO_FORMAT = args.date

    return send_files


def generate_region_files(date_zero=DATE_ZERO, region_name: str = 'region1'):
    global ukios, missed
    send_files: bool = parse_args()
    create_dirs()
    create_arms_and_operators()
    ukios_list = []
    missed_list = []
    dt_start = datetime.datetime.now()
    models_create_time = None
    # fill with the Google sheets
    fill_incident_type_lists(region_name)
    fill_addresses(region_name)
    # generate dicts with info
    for i in range(generator.files_count):
        for j in range(generator.xml_count_per_file):

            u = generate_ukio_phone_call_data(date_zero)
            date_zero += td(seconds=AVG_DELAY_BETWEEN_CALLS_TIME)
            if u is not None:
                if isinstance(u, Ukio):
                    ukios_list.append(u)
                    ukios_info[-1]['filename'] = f'ukios_{i + j}.xml'
                elif isinstance(u, MissedCall):
                    missed_list.append(u)
                    missed_info[-1]['filename'] = f'missed_{i + j}.xml'
        # make pydantic models for dicts
        ukios = Ukios(
            Ukios=ukios_list
        )
        missed = MissedCalls(
            missedCalls=missed_list
        )

        models_create_time = datetime.datetime.now() - dt_start
        # print("models done", models_create_time)
        if GENERATE_UKIO:
            ukio_file_path = create_file_from_model(ukios, filename=f'ukios_{i}', basename="Ukios",
                                                    region_name=region_name)
            modify_xml_file_to_send(ukio_file_path, get_file_prefix(UKIO_SOAP_PREFIX),
                                    get_file_postfix(UKIO_SOAP_POSTFIX))
            print('start check ukio with wsdl fields')
            check_fields_by_file_path(ukio_file_path, 'wsdl_4_3.wsdl')
        if GENERATE_MISSED_CALLS:
            missed_calls_file_path = create_file_from_model(missed, filename=f'missed_{i}', basename='MissedCalls',
                                                            region_name=region_name)
            modify_xml_file_to_send(missed_calls_file_path, get_file_prefix(MISSED_SOAP_PREFIX),
                                    get_file_postfix(MISSED_SOAP_POSTFIX))
        if GENERATE_ARM_WORK:
            arm_works = ArmWorks(
                armWork=ARM_WORK
            )

            arm_works_file_path = create_file_from_model(arm_works, f"ArmWork_{i}", basename="ArmWorks",
                                                         region_name=region_name)
            modify_xml_file_to_send(arm_works_file_path, get_file_prefix(ARMWORK_SOAP_PREFIX),
                                    get_file_postfix(ARMWORK_SOAP_POSTFIX))
        if GENERATE_OPERATOR_WORKS:
            operator_works = OperatorWorks(
                operatorWork=OPERATOR_WORK
            )
            operator_works_file_path = create_file_from_model(operator_works, f"OperatorWork_{i}",
                                                              basename="OperatorWorks", region_name=region_name)
            modify_xml_file_to_send(operator_works_file_path, get_file_prefix(OPERATOR_WORK_SOAP_PREFIX),
                                    OPERATOR_WORK_SOAP_POSTFIX)

        if GENERATE_INCIDENT_TYPES:
            incident_types = IncidentTypes(incidentType=INCIDENT_TYPES_LIST)
            incident_types_file_path = create_file_from_model(incident_types, f'incident_types_{i}',
                                                              'IncidentTypes', region_name=region_name)
            modify_xml_file_to_send(incident_types_file_path,
                                    get_file_prefix(INCIDENT_SOAP_PREFIX),
                                    get_file_postfix(INCIDENT_SOAP_POSTFIX))

    print("finish time", datetime.datetime.now() - dt_start)
    if send_files:
        prepare_files_to_send(ukios, missed, region_name)  # split files
        print("start send files")
        if create_send_info_csv_files('missed_calls_to_send',
                                      config_send_info_list=missed_info,
                                      region_name=region_name) is False:
            pass
        create_send_info_csv_files('ukios_to_send',
                                   config_send_info_list=ukios_info,
                                   region_name=region_name)
        send_along(region_name)


def main():
    clear_dir()
    if TAKE_CONSTANTS_FROM_FILE:
        generate_region_files()
    else:
        for constants_dict in get_next_constants():
            ukios_info.clear()
            missed_info.clear()
            globals().update(constants_dict)
            generate_region_files(region_name=constants_dict["region_name/constant name"])


if __name__ == '__main__':
    main()
