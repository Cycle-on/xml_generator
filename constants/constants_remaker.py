from constants import ALL_PROJ_CONSTANTS
from csv_reader import get_csv_from_url


def get_next_constants() -> dict:
    for row in get_csv_from_url(ALL_PROJ_CONSTANTS["CONSTANTS_URL"]):
        yield row.to_dict()
