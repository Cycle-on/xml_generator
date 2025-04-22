import datetime
import random
import time
from datetime import timedelta as td
from pprint import pprint

from constants import fill_constants

fill_constants()
from constants import ALL_PROJ_CONSTANTS, get_file_prefix, get_file_postfix

from config import ukios_info, missed_info, load_config
from config.dirs import create_dirs, clear_dir
from constants.constants_remaker import get_next_constants
from csv_parser.parse_addresses import fill_addresses
from csv_parser.parse_incident_types import fill_incident_type_lists
from file_creator import create_file_from_model
from generators.operators_and_arms import ARM_WORK, OPERATOR_WORK, create_arms_and_operators
from generators.ukio_generator import generate_ukio_phone_call_data
from schemas.phonecall import MissedCall, MissedCalls
from schemas.string_eos import OperatorWorks, ArmWorks, IncidentTypes
from schemas.ukio_model import Ukios, Ukio
from send_files import modify_xml_file_to_send, __send_file
from wsdl_parser.wsdl_tester import check_fields_by_file_path

config = load_config()


def generate_region_files(date_zero=config.date_zero, region_name: str = 'region1'):
    create_dirs()
    create_arms_and_operators()
    date_zero = datetime.datetime.now() - td(hours=3)
    dt_start = datetime.datetime.now()
    fill_incident_type_lists(region_name)
    # models_create_time = None
    # fill with the Google sheets
    fill_addresses(region_name)
    # generate dicts with info
    for i in range(ALL_PROJ_CONSTANTS.get("files_count")):
        ukios_list = []
        missed_list = []
        for j in range(ALL_PROJ_CONSTANTS.get("xml_count_per_file")):

            u = generate_ukio_phone_call_data(date_zero)
            date_zero += td(seconds=ALL_PROJ_CONSTANTS['AVG_DELAY_BETWEEN_CALLS_TIME'])
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

        # models_create_time = datetime.datetime.now() - dt_start
        # print("models done", models_create_time)
        if ALL_PROJ_CONSTANTS['GENERATE_UKIO']:
            ukio_file_path = create_file_from_model(ukios, filename=f'ukios_{i}', basename="Ukios",
                                                    region_name=region_name)
            modify_xml_file_to_send(ukio_file_path, get_file_prefix(ALL_PROJ_CONSTANTS['UKIO_SOAP_PREFIX']),
                                    get_file_postfix(ALL_PROJ_CONSTANTS['UKIO_SOAP_POSTFIX']))
            print('start check ukio with wsdl fields')
            check_fields_by_file_path(ukio_file_path, 'wsdl_4_3.wsdl')
        if ALL_PROJ_CONSTANTS['GENERATE_MISSED_CALLS']:
            missed_calls_file_path = create_file_from_model(missed, filename=f'missed_{i}', basename='MissedCalls',
                                                            region_name=region_name)
            modify_xml_file_to_send(missed_calls_file_path, get_file_prefix(ALL_PROJ_CONSTANTS['MISSED_SOAP_PREFIX']),
                                    get_file_postfix(ALL_PROJ_CONSTANTS['MISSED_SOAP_POSTFIX']))
        if ALL_PROJ_CONSTANTS['GENERATE_ARM_WORK']:
            arm_works = ArmWorks(
                armWork=ARM_WORK
            )

            arm_works_file_path = create_file_from_model(arm_works, f"ArmWork_{i}", basename="ArmWorks",
                                                         region_name=region_name)
            modify_xml_file_to_send(arm_works_file_path, get_file_prefix(ALL_PROJ_CONSTANTS['ARMWORK_SOAP_PREFIX']),
                                    get_file_postfix(ALL_PROJ_CONSTANTS['ARMWORK_SOAP_POSTFIX']))
        if ALL_PROJ_CONSTANTS['GENERATE_OPERATOR_WORKS']:
            operator_works = OperatorWorks(
                operatorWork=OPERATOR_WORK
            )
            operator_works_file_path = create_file_from_model(operator_works, f"OperatorWork_{i}",
                                                              basename="OperatorWorks", region_name=region_name)
            modify_xml_file_to_send(operator_works_file_path,
                                    get_file_prefix(ALL_PROJ_CONSTANTS['OPERATOR_WORK_SOAP_PREFIX']),
                                    ALL_PROJ_CONSTANTS['OPERATOR_WORK_SOAP_POSTFIX'])

        if ALL_PROJ_CONSTANTS['GENERATE_INCIDENT_TYPES']:
            incident_types = IncidentTypes(incidentType=ALL_PROJ_CONSTANTS['INCIDENT_TYPES_LIST'])
            incident_types_file_path = create_file_from_model(incident_types, f'incident_types_{i}',
                                                              'IncidentTypes', region_name=region_name)
            modify_xml_file_to_send(incident_types_file_path,
                                    get_file_prefix(ALL_PROJ_CONSTANTS['INCIDENT_SOAP_PREFIX']),
                                    get_file_postfix(ALL_PROJ_CONSTANTS['INCIDENT_SOAP_POSTFIX']))

    print("finish time", datetime.datetime.now() - dt_start)


def send_files(region_name):
    # prepare_files_to_send(ukios, missed, region_name)  # split files
    print("start send files")
    # if create_send_info_csv_files('missed_calls_to_send',
    #                               config_send_info_list=missed_info,
    #                               region_name=region_name) is False:
    #     pass
    # create_send_info_csv_files('ukios_to_send',
    #                            config_send_info_list=ukios_info,
    #                            region_name=region_name)

    # csv_files_dir_path = os.path.join('files', files_prefix, region_name, 'ukios_to_send.csv')
    # with open(csv_files_dir_path, mode='r', encoding='utf-8') as file:
    #     reader = csv.DictReader(file)  # Используем DictReader для чтения в виде словарей
    #     for row in reader:
    #         filename = row['filename']
    __send_file(region_name, 'ukios_0.xml', prefix='Ukios')
    print('continue file generating')
    # send_along(region_name)


def main():
    config.date_zero = datetime.datetime.now() - td(hours=3)
    clear_dir()
    if config.send_files:

        for _ in range(ALL_PROJ_CONSTANTS['ALL_TIME'] // ALL_PROJ_CONSTANTS['SENDER_DELAY']):
            ukios_info.clear()
            missed_info.clear()

            if config.send_files:
                # print(random.randint(sender.COEF_MIN, sender.COEF_MAX))
                ALL_PROJ_CONSTANTS["xml_count_per_file"] *= random.randint(ALL_PROJ_CONSTANTS['COEF_MIN'],
                                                                           ALL_PROJ_CONSTANTS['COEF_MAX']) / 100
                ALL_PROJ_CONSTANTS["xml_count_per_file"] = int(ALL_PROJ_CONSTANTS["xml_count_per_file"])
                # print("ff", ALL_PROJ_CONSTANTS["xml_count_per_file"])
                ALL_PROJ_CONSTANTS["files_count"] = 1

            if ALL_PROJ_CONSTANTS['TAKE_CONSTANTS_FROM_FILE']:
                generate_region_files('region1')
                if config.send_files:
                    send_files('region1')
            else:
                for constants_dict in get_next_constants():
                    ukios_info.clear()
                    missed_info.clear()
                    ALL_PROJ_CONSTANTS.update(constants_dict)
                    for k, v in ALL_PROJ_CONSTANTS.items():
                        if isinstance(v, str) and '[' in v:
                            ALL_PROJ_CONSTANTS[k] = eval(v)

                    generate_region_files(region_name=constants_dict["region_name/constant name"])
                    if config.send_files:
                        send_files(constants_dict["region_name/constant name"])
            time.sleep(ALL_PROJ_CONSTANTS['SENDER_DELAY'])
    else:

        if ALL_PROJ_CONSTANTS['TAKE_CONSTANTS_FROM_FILE']:
            generate_region_files(region_name='region1')

            if config.send_files:
                send_files('region1')
        else:
            for constants_dict in get_next_constants():
                ukios_info.clear()
                missed_info.clear()

                ALL_PROJ_CONSTANTS.update(constants_dict)
                # make lists from strings
                for k, v in ALL_PROJ_CONSTANTS.items():
                    if isinstance(v, str) and '[' in v:
                        ALL_PROJ_CONSTANTS[k] = eval(v)

                generate_region_files(region_name=constants_dict["region_name/constant name"])


if __name__ == '__main__':
    main()
