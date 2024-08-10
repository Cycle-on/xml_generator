import datetime
from datetime import timedelta as td
import random

import numpy as np

from constants import *
from config import load_config
from schemas import Operator, EOSType
from schemas.phone import Phone

from generators import check_event_probability

config = load_config()


def generate_cut_phone_call() -> Phone:
    operator_indicate = True
    operator = Operator()
    dt_call, dt_connect, dt_end_call, date_send = _generate_cut_phone_date()

    end_call_list = [True, False]
    random.shuffle(end_call_list)
    a, b = end_call_list
    return Phone(
        dtSend_=date_send,
        operator=operator,
        OperatorIniciatied=operator_indicate,
        dtCall_=dt_call,
        dtConnect_=dt_connect,
        bCallEnded=b,
        aCallEnded=a,
        dtEndCall_=dt_end_call,
    )


def _generate_cut_phone_date():
    operator_recall_time = np.random.normal(AVG_TIME_OPERATOR_RECALL_WAITING, OPERATOR_RECALL_WAITING_SCALE)
    phone_call_time = np.random.normal(AVERAGE_CARD_CREATE_TIME, CARD_CREATE_TIME_SCALE)

    operator_wait_call_answer_time = np.random.normal(AVG_TIME_OPERATOR_WAITING, OPERATOR_TIME_WAITING_SCALE)
    random_send_data_delay = random.randint(3, 5)

    dt_call = datetime.datetime.now()
    dt_connect = dt_call + td(seconds=operator_recall_time) + td(seconds=operator_wait_call_answer_time)
    dt_end_call = dt_connect + td(seconds=phone_call_time)
    date_send = dt_end_call + td(seconds=random_send_data_delay)

    return dt_call, dt_connect, dt_end_call, date_send


def _generate_phone_date():
    operator_reaction = np.random.normal(OPERATOR_REACTION_TIME, OPERATOR_REACTION_TIME_SCALE)
    phone_call_time = np.random.normal(AVERAGE_CARD_CREATE_TIME, CARD_CREATE_TIME_SCALE)
    random_send_data_delay = random.randint(3, 5)

    dt_call = datetime.datetime.now()
    dt_connect = dt_call + td(seconds=operator_reaction)
    dt_end_call = dt_connect + td(minutes=phone_call_time // 60, seconds=phone_call_time % 60)
    date_send = dt_end_call + td(seconds=random_send_data_delay)
    return dt_call, dt_connect, dt_end_call, date_send


def generate_phone_data() -> Phone:
    if check_event_probability(1, 1):  # phone call is dropped
        # ^ mean 1 percent probability ^
        re_call_time = np.random.normal(3, 5)
        print(re_call_time)
        return

        # random constants
    operator_indicate = False

    end_call_list = [True, False]
    random.shuffle(end_call_list)
    a, b = end_call_list

    # phone date info
    dt_call, dt_connect, dt_end_call, date_send = _generate_phone_date()
    # operator
    random_EOS = list(EOSType)[random.randint(0, len(list(EOSType)) - 1)]
    operator = Operator(eosClassTypeId=[random_EOS])
    # redirect_call = None
    return Phone(
        dtSend_=date_send,
        operator=operator,
        OperatorIniciatied=operator_indicate,
        dtCall_=dt_call,
        dtConnect_=dt_connect,
        bCallEnded=b,
        aCallEnded=a,
        dtEndCall_=dt_end_call,
        # redirectCall=redirect_call
    )


def main():
    random.seed(184)  # seed with dropped phone call
    generate_phone_data()


if __name__ == '__main__':
    main()
