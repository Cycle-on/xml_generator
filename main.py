from datetime import timedelta as td
from config import load_config
from config.config_data import *
from file_creator import create_file_from_model
from generators.ukio_generator import generate_ukio_phone_call_data
from config.dirs import create_dirs
from schemas.phonecall import Calls
from schemas.ukio_model import Ukios
from config.config_data import DATE_ZERO

config = load_config()


def main(date_zero=DATE_ZERO):
    create_dirs()
    ukios_list = []
    calls_list = []
    dt_start = datetime.datetime.now()
    models_create_time = None
    for i in range(config.files_count):
        for _ in range(xml_count_per_file):

            u, c = generate_ukio_phone_call_data(date_zero)
            date_zero += td(seconds=AVG_DELAY_BETWEEN_CALLS_TIME)
            if u is not None:
                ukios_list.append(u)
            calls_list.append(c)
        ukios = Ukios(
            Ukios=ukios_list
        )
        calls = Calls(
            Call=calls_list,
        )
        models_create_time = datetime.datetime.now() - dt_start
        print("models done", models_create_time)
        create_file_from_model(ukios, filename=f'ukios_{i}', basename="Ukios")
        create_file_from_model(calls, filename=f'calls_{i}', basename='Calls')

    print("finish time", datetime.datetime.now() - dt_start)


if __name__ == '__main__':
    main()
