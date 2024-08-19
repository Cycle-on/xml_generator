import os

from config import load_config
from file_creator import create_file_from_model
from generators.ukio_generator import generate_ukio_phone_call_data
from config.dirs import create_dirs
from schemas.phonecall import Calls
from schemas.ukio_model import Ukios

config = load_config()


def main():
    create_dirs()
    ukios_list = []
    calls_list = []
    for i in range(config.files_count):
        u, c = generate_ukio_phone_call_data()
        ukios_list.append(u)
        calls_list.append(c)
    ukios = Ukios(
        Ukios=ukios_list
    )
    calls = Calls(
        Call=calls_list,
    )
    create_file_from_model(ukios, filename='ukios', basename="Ukios")
    create_file_from_model(calls, filename='calls', basename='Calls')


if __name__ == '__main__':
    main()
