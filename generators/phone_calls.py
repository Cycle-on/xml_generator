import datetime
from datetime import timedelta as td
import random
from pprint import pprint

import numpy as np

from constants import *
from config import load_config
from schemas import Operator, EOSType
from schemas.phone import Phone
from generators import check_event_probability

config = load_config()


def _generate_phone_date(recall: bool = False):
    dt_call = datetime.datetime.now()

    if recall:
        operator_recall_time = abs(np.random.normal(AVG_TIME_OPERATOR_RECALL_WAITING, OPERATOR_RECALL_WAITING_SCALE))
        operator_wait_call_answer_time = abs(np.random.normal(AVG_TIME_OPERATOR_WAITING, OPERATOR_TIME_WAITING_SCALE))

        dt_connect = dt_call + td(seconds=operator_recall_time) + td(seconds=operator_wait_call_answer_time)

    else:
        operator_reaction = abs(np.random.normal(OPERATOR_REACTION_TIME, OPERATOR_REACTION_TIME_SCALE))

        dt_connect = dt_call + td(seconds=operator_reaction)

    phone_call_time = abs(np.random.normal(AVERAGE_CARD_CREATE_TIME, CARD_CREATE_TIME_SCALE))
    random_send_data_delay = random.randint(3, 5)
    dt_end_call = dt_connect + td(minutes=phone_call_time // 60,
                                  seconds=phone_call_time % 60)

    date_send = dt_end_call + td(seconds=random_send_data_delay)
    return dt_call, dt_connect, dt_end_call, date_send


def generate_phone_data() -> Phone:
    # random constants
    end_call_list = [True, False]
    random.shuffle(end_call_list)
    a, b = end_call_list
    operator_indicate = False

    # operator
    random_EOS = list(EOSType)[random.randint(0, len(list(EOSType)) - 1)]
    operator = Operator(eosClassTypeId=[random_EOS])

    # phone date info
    if check_event_probability(1, 1):  # phone call is dropped
        # ^ mean 1 percent probability ^
        operator_indicate = True
        dt_call, dt_connect, dt_end_call, date_send = _generate_phone_date(recall=True)
    else:
        dt_call, dt_connect, dt_end_call, date_send = _generate_phone_date()
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
    # random.seed(105)  # seed with dropped phone call
    for _ in range(100):
        print(generate_phone_data())


if __name__ == '__main__':
    main()
