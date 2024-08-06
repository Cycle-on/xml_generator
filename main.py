import datetime
import random
from copy import copy

import numpy as np

from constants import *
from config import load_config
from schemas import Operator, EOSType
from schemas.Phone import Phone
from schemas.string_schemas import CallSource, IncidentType, CardStates
from file_creator import create_file_from_model

config = load_config()


def generate_phone_data():
    # random constants
    operator_reaction = np.random.normal(8, 3)
    phone_call_time = np.random.normal(75, 10)
    random_send_data_delay = random.randint(3, 5)
    operator_indicate = False

    end_call_list = [True, False]
    random.shuffle(end_call_list)
    # phone date info
    dt_call = datetime.datetime.now()
    dt_connect = dt_call + datetime.timedelta(seconds=operator_reaction)
    dt_end_call = dt_connect + datetime.timedelta(seconds=phone_call_time)
    date_send = dt_end_call + datetime.timedelta(seconds=random_send_data_delay)
    # operator
    random_EOS = list(EOSType)[random.randint(0, len(list(EOSType)) - 1)]
    operator = Operator(eosClassTypeId=[random_EOS])
    a, b = end_call_list
    # redirect_call = None
    return Phone(
        dtSend_=date_send,
        operator=operator,
        OperatorIniciatied=operator_indicate,
        dtCall_=dt_call,
        dtConnect_=dt_connect,
        bCallEnded=b,
        aCallEnded=a,
        dtEndCall=dt_end_call,
        # redirectCall=redirect_call
    )

    # print(f"Дата вызова:{" " * 45} {dt_call} +({operator_reaction})")
    # print(f"Дата ответа оператора от момента установления соединения: {dt_connect} +({phone_call_time})")
    # print(f"Дата завершения вызова:{" " * 34} {dt_end_call}")


def generate_ukio_date():
    random_card_create_time = np.random.normal(AVERAGE_CARD_CREATE_TIME, 10)
    random_send_date = datetime.datetime.now()
    random_create_date = random_send_date - datetime.timedelta(seconds=random_card_create_time)
    random_update_date = copy(random_create_date)


def generate_other_ukio_data():
    random_card_state = list(CardStates)[random.randint(0, len(list(CardStates)) - 1)]
    random_incident_type = list(IncidentType)[random.randint(0, len(list(IncidentType)) - 1)]
    casualties = None  # get from config
    wrong = False
    child_play = False


def generate_card():
    pass


def main():
    for i in range(5):
        p = generate_phone_data()
        create_file_from_model(p, filename=f'{i}', basename='phoneCall')
        print("_______________________")


if __name__ == '__main__':
    main()
