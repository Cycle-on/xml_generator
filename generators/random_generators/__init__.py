import os
import random
from pprint import pprint


def execute_district(address: str):
    for el in address:
        district = el.split()

        if 'р-не' in el:
            continue
        elif 'р-н.' in el:
            district.remove('р-н.')

        elif 'р-н' in el:
            district.remove('р-н')

        elif 'районе' in el:
            district.remove('районе')

        elif 'района' in el:
            district.remove('района')

        elif 'микрорайон' in el:
            continue
        elif 'районного' in el:
            continue
        elif 'район' in el:
            district.remove('район')
        else:
            continue

        if len(district) > 3:
            continue

        return " ".join(district), address[0]
    return None, None


def get_address_by_code(region_code: str | int = "27") -> tuple[str, str, str]:
    with open(os.path.join('generators', 'random_generators', 'addresses', f"{region_code}.txt")) as f:
        all_streets = f.readlines()
    # with open(f"{region_code}.txt") as f:
    #     all_streets = f.readlines()

    street_district = None
    random_address = None
    city = None
    while street_district is None:
        random_address = random.choice(all_streets)
        random_address = random_address.strip()
        street_district, city = execute_district(random_address.split(','))
    return random_address, street_district, city


def get_random_name(gender: str) -> list[str]:
    if gender == 'F':
        with open(os.path.join('generators', 'random_generators', 'random_names', 'female.txt')) as f:
            return random.choice(f.readlines())[:-1].split()

    with open(os.path.join('generators', 'random_generators', 'random_names', "male.txt")) as f:
        return random.choice(f.readlines())[:-1].split()


def get_random_telephone_number():
    first_part = str(random.randint(950, 999))
    second_part = str(random.randint(0, 9999999))
    return f"+7({first_part})-{second_part[:3]}-{second_part[3:]}"


def main():
    get_address_by_code()


if __name__ == '__main__':
    main()
