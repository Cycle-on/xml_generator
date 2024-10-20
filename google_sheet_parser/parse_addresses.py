import random

import pandas as pd

from csv_reader import get_csv_from_url
from constants import *
from schemas.ukio_model import Address

ADDRESSES = []


def fill_with_address_headers(headers: list[str], address: list[str]):
    address_dict = {}
    for i in range(len(address)):
        if address[i] == '':
            continue
        if address[i][0] == 'n':
            address[i] = int(address[i])
        elif address[i][0] == 'b':
            address[i] = bool(address[i])
        address_dict[headers[i]] = address[i]
    return address_dict


def fill_addresses(region_name: str = ''):
    """
    send request to google sheets and saving addresses in the list
    :return:
    """
    global ADDRESSES
    resp: pd.Series = get_csv_from_url(ADDRESSES_URL)
    ADDRESSES.clear()
    for el in resp:
        el = el.dropna().astype(str).to_dict()
        if el['region_name'] == region_name and region_name != '':
            ADDRESSES.append(Address(**el))
        elif region_name == '':
            ADDRESSES.append(Address(**el))


def get_random_address() -> tuple[str, str, str, str, str, str, str]:
    """
    :return: string_address, lat, long, city, district, kladr, fias
    """
    global ADDRESSES

    return random.choice(ADDRESSES)


if __name__ == '__main__':
    fill_addresses()
    print(get_random_address())
