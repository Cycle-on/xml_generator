import datetime

from datetime import timedelta as td
import random
from copy import copy

import numpy as np

from constants import *
from schemas.string_schemas import IncidentType, CardStates


def generate_other_ukio_data():
    random_card_state = list(CardStates)[random.randint(0, len(list(CardStates)) - 1)]
    random_incident_type = list(IncidentType)[random.randint(0, len(list(IncidentType)) - 1)]
    casualties = None  # get from config
    wrong = False
    child_play = False
    print(random_card_state)


def generate_ukio_date():
    random_card_create_time = np.random.normal(AVERAGE_CARD_CREATE_TIME, CARD_CREATE_TIME_SCALE)
    random_send_date = datetime.datetime.now()
    random_create_date = random_send_date - td(seconds=random_card_create_time)
    random_update_date = copy(random_create_date)


def generate_card():
    pass


def main():
    generate_other_ukio_data()


if __name__ == '__main__':
    main()
