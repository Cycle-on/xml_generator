import datetime
import time
from datetime import timedelta as td

from config import ukios_info, missed_info, load_config
from config.dirs import create_dirs, clear_dir
from constants import *
from constants.constants_remaker import get_next_constants
from csv_parser.parse_addresses import fill_addresses
from csv_parser.parse_incident_types import fill_incident_type_lists, INCIDENT_TYPES_LIST
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

    dt_start = datetime.datetime.now()
    # models_create_time = None
    # fill with the Google sheets
    fill_incident_type_lists(region_name)
    fill_addresses(region_name)
    # generate dicts with info
    for i in range(globals().get("files_count")):
        ukios_list = []
        missed_list = []
        for j in range(globals().get("xml_count_per_file")):

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

        # models_create_time = datetime.datetime.now() - dt_start
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
        pass
        for _ in range(ALL_TIME // SENDER_DELAY):
            ukios_info.clear()
            missed_info.clear()

            if config.send_files:
                # print(random.randint(sender.COEF_MIN, sender.COEF_MAX))
                globals()["xml_count_per_file"] *= random.randint(sender.COEF_MIN, sender.COEF_MAX) / 100
                globals()["xml_count_per_file"] = int(globals()["xml_count_per_file"])
                # print("ff", globals()["xml_count_per_file"])
                globals()["files_count"] = 1

            if TAKE_CONSTANTS_FROM_FILE:
                generate_region_files()
                if config.send_files:
                    send_files('region1')
            else:
                for constants_dict in get_next_constants():
                    ukios_info.clear()
                    missed_info.clear()
                    # GLOBALS_DICT = (globals())
                    # GLOBALS_DICT.update(constants_dict)
                    globals().update(constants_dict)

                    generate_region_files(region_name=constants_dict["region_name/constant name"])
                    if config.send_files:
                        send_files(constants_dict["region_name/constant name"])
            time.sleep(SENDER_DELAY)
    else:

        if TAKE_CONSTANTS_FROM_FILE:
            generate_region_files()
            if config.send_files:
                send_files('region1')
        else:
            for constants_dict in get_next_constants():
                ukios_info.clear()
                missed_info.clear()
                # GLOBALS_DICT = (globals())
                # GLOBALS_DICT.update(constants_dict)
                globals().update(constants_dict)

                generate_region_files(region_name=constants_dict["region_name/constant name"])


if __name__ == '__main__':
    main()
