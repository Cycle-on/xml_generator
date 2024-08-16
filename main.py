import os

from config import load_config
from file_creator import create_file_from_model
from generators.ukio_generator import generate_ukio_phone_call_data
from config.dirs import create_dirs

config = load_config()


def main():
    create_dirs()
    for i in range(config.files_count):
        u, c = generate_ukio_phone_call_data()
        create_file_from_model(u, filename=os.path.join('ukios', str(i)), basename='ukio')
        create_file_from_model(c, filename=os.path.join('calls', str(i)), basename='calls')


if __name__ == '__main__':
    main()
