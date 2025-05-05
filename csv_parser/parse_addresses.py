import random

from constants import ALL_PROJ_CONSTANTS
from csv_reader import get_csv_from_url
from schemas.ukio_model import Address

ADDRESSES = []


def fill_with_address_headers(headers: list[str], address: list[str]):
    address_dict = {}
    for i in range(len(address)):
        if address[i] == "":
            continue
        if address[i][0] == "n":
            address[i] = int(address[i])
        elif address[i][0] == "b":
            address[i] = bool(address[i])
        address_dict[headers[i]] = address[i]
    return address_dict


def fill_addresses(region_name: str = ""):
    """
    send request to google sheets and saving addresses in the list
    :return:
    """
    global ADDRESSES
    ADDRESSES.clear()
    resp = list(get_csv_from_url(ALL_PROJ_CONSTANTS["ADDRESSES_URL"]))

    for el in resp:
        el = el.dropna().astype(str).to_dict()
        el_region = str(el["region_name"])
        param_region = str(region_name)

        if el_region == param_region and region_name != "" or region_name == "":
            ADDRESSES.append(Address(**el))


def get_random_address() -> tuple[str, str, str, str, str, str, str]:
    """
    :return: string_address, lat, long, city, district, kladr, fias
    """
    global ADDRESSES

    return random.choice(ADDRESSES)


if __name__ == "__main__":
    fill_addresses()
    print(get_random_address())
