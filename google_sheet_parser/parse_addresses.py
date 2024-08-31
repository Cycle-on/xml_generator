import random

from google_sheet_parser import _get_service_acc
from constants import *

ADDRESSES = []


def fill_addresses():
    """
    send request to google sheets and saving addresses in the list
    :return:
    """
    global ADDRESSES

    resp = _get_service_acc().spreadsheets().values().get(spreadsheetId=SHEET_ID,
                                                            range=f"{ADDRESSES_LIST_NAME}!A1:I999").execute()
    ADDRESSES = resp['values'][1:]


def get_random_address() -> tuple[str, str, str, str, str, str, str]:
    """
    :return: string_address, lat, long, city, district, kladr, fias
    """
    global ADDRESSES
    return random.choice(ADDRESSES)
