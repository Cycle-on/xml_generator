from config import load_config
from generators.phone_calls import generate_phone_data
from file_creator import create_file_from_model

config = load_config()


def main():
    for i in range(5):
        p = generate_phone_data()
        create_file_from_model(p, filename=f'{i}', basename='phoneCall')
        # print("_______________________")


if __name__ == '__main__':
    main()
