from constants import CONSTANTS_URL
from csv_reader import get_csv_from_url


def get_next_constants() -> dict:
    for row in get_csv_from_url(CONSTANTS_URL):
        yield row.to_dict()
