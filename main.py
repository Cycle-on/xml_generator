from datetime import timedelta as td
from config import load_config, calls_info, ukios_info
from config.config_data import *
from file_creator import create_file_from_model, create_send_info_csv_files
from generators.ukio_generator import generate_ukio_phone_call_data
from config.dirs import create_dirs
from google_sheet_parser.parse_addresses import fill_addresses
from google_sheet_parser.parse_incident_types import fill_incident_type_lists
from schemas.phonecall import Calls
from schemas.ukio_model import Ukios
from config.config_data import DATE_ZERO
from send_files import send_along

config = load_config()


def main(date_zero=DATE_ZERO):
    create_dirs()
    ukios_list = []
    calls_list = []
    dt_start = datetime.datetime.now()
    models_create_time = None
    fill_incident_type_lists()
    fill_addresses()
    print("заполнил incident types")
    for i in range(config.files_count):
        for _ in range(xml_count_per_file):

            u, c, = generate_ukio_phone_call_data(date_zero)
            date_zero += td(seconds=AVG_DELAY_BETWEEN_CALLS_TIME)
            if u is not None:
                ukios_list.append(u)
                ukios_info[-1]['filename'] = f'ukios_{i}.xml'

            calls_list.append(c)
            calls_info[-1]['filename'] = f'calls_{i}.xml'
        ukios = Ukios(
            Ukios=ukios_list
        )
        calls = Calls(
            Call=calls_list,
        )

        ukios_list = []
        calls_list = []
        models_create_time = datetime.datetime.now() - dt_start
        # print("models done", models_create_time)
        create_file_from_model(ukios, filename=f'ukios_{i}', basename="Ukios")
        create_file_from_model(calls, filename=f'calls_{i}', basename='Calls')
    create_send_info_csv_files('calls_to_send', calls_info)
    create_send_info_csv_files('ukios_to_send', ukios_info)
    print("finish time", datetime.datetime.now() - dt_start)
    print("start send files")
    send_along()


if __name__ == '__main__':
    main()
