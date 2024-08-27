import datetime
from copy import copy, deepcopy
from datetime import timedelta as td
import random
from pprint import pprint

from generators.eos_generator import generate_random_eos_list
import numpy as np

from config.config_data import *
from schemas.string_eos import Operator
from schemas.phonecall import PhoneCall, Call
from generators import check_event_probability, get_distribution_var_by_work_type
from schemas.string_schemas import CardStates


def generate_phone_date(recall: bool = False, dt_call=DATE_ZERO, **kwargs) \
        -> tuple[datetime.datetime,
        datetime.datetime,
        datetime.datetime,
        datetime.datetime]:
    """
    creating date params to PhoneCall model
    dt_call->dt_connect # step 1
    dt_connect -> phone_call_time # step 2
    :param recall:
    :param dt_call:
    :param kwargs: dict with step1, step2
    ** can change to one step, with True or datetime and check it with isinstance
    because it has different types
    :return: four dates
    """
    if recall:
        # we have dropped call and we need some new params

        dt_call += td(
            seconds=get_distribution_var_by_work_type(OPERATOR_WAIT_ANSWER_RECALL_WORK_TYPE, "OPERATOR_RECALL_WAITING"))
        dt_connect = dt_call + td(
            seconds=get_distribution_var_by_work_type(OPERATOR_WAITING_WORK_TYPE, "OPERATOR_WAITING"))

    else:
        # base call
        operator_reaction = get_distribution_var_by_work_type(OPERATOR_REACTION_WORK_TYPE, "OPERATOR_REACTION")
        dt_connect = dt_call + td(seconds=operator_reaction)

    if kwargs.get('step2'):
        phone_call_time = kwargs.get('step2').seconds
    else:
        phone_call_time = get_distribution_var_by_work_type(CARD_CREATE_WORK_TYPE, "CARD_CREATE")
    dt_end_call = dt_connect + td(minutes=phone_call_time // 60,
                                  seconds=phone_call_time % 60)
    random_send_data_delay = random.randint(3, 5)
    date_send = dt_end_call + td(seconds=random_send_data_delay)
    return dt_call, dt_connect, dt_end_call, date_send


def recall(dt_call: datetime.datetime) -> tuple[datetime.datetime, list[PhoneCall]]:
    calls = []
    dt_end_call = None
    for _ in range(random.randint(0, MAX_RECALL_ATTEMPTS - 1)):
        dt_call += td(
            seconds=get_distribution_var_by_work_type(OPERATOR_RECALL_WAITING_WORK_TYPE, "OPERATOR_RECALL_WAITING"))

        dt_end_call = dt_call + td(
            get_distribution_var_by_work_type(OPERATOR_WAIT_ANSWER_RECALL_WORK_TYPE, "OPERATOR_WAIT_ANSWER_RECALL")
        )

        p = PhoneCall(
            dtCall=dt_call,
            bOperatorIniciatied=True,
            aCallEnded=False,
            bCallEnded=True,
            dtEndCall=dt_end_call,
        )
        calls.append(p)
        dt_call = dt_end_call
    return dt_call if dt_end_call is None else dt_end_call, calls


def generate_phone_data(call_date, operator: Operator) -> list[PhoneCall]:
    """
    creating PhoneCall,
    if len(list) == 0, phone call not dropped,
    if len(list) > 1, phone call is dropped
    :return: list with phone calls models
    """
    phone_calls: list[PhoneCall] = []
    # random constants
    end_call_list = [True, False]
    random.shuffle(end_call_list)
    a, b = end_call_list

    DROP = False
    # operator
    dt_call, dt_connect, dt_end_call, date_send = generate_phone_date(
        dt_call=call_date
    )
    first_call_end_call_time = dt_end_call
    date_send2 = None
    # phone date info
    if check_event_probability(DROP_CALL_PROBABILITY):  # phone call is dropped
        # recall_logic
        DROP = True

        dropped_timedelta = dt_end_call - dt_connect  # count drop time phone call
        break_time = random.randint(0, dropped_timedelta.seconds)
        break_time_delta = td(seconds=break_time % 60, minutes=break_time // 60)
        step1_timedelta = dt_connect - dt_call
        # updating first call end time
        dt_end_call = dt_call + break_time_delta
        first_call_end_call_time = deepcopy(dt_end_call)
        # making recalls
        dt_end_call, recall_phonecalls_list = recall(dt_end_call)
        if break_time_delta < step1_timedelta:
            dt_call2, dt_connect2, dt_end_call2, date_send2 = generate_phone_date(
                recall=True,
                dt_call=dt_end_call,
                step1=True
            )

        else:  # step 2: dt_end_call - dt_connect
            dt_call2, dt_connect2, dt_end_call2, date_send2 = generate_phone_date(
                recall=True,
                dt_call=dt_end_call,
                step2=dropped_timedelta - break_time_delta + step1_timedelta,

            )

        phone_calls.append(
            PhoneCall(
                dtSend=date_send2,
                OperatorId=operator.operatorId,
                bOperatorIniciatied=True,
                dtCall=dt_call2,
                dtConnect=dt_connect2,
                bCallEnded=True,
                aCallEnded=False,
                dtEndCall=dt_end_call2,
            )
        )
        phone_calls.extend(recall_phonecalls_list)

    phone_calls.append(
        PhoneCall(
            dtSend=date_send2 if date_send2 is not None else date_send,
            OperatorId=operator.operatorId,
            bOperatorIniciatied=False,
            dtCall=dt_call,
            dtConnect=dt_connect,
            bCallEnded=b if not DROP else False,
            aCallEnded=a if not DROP else True,
            dtEndCall=first_call_end_call_time,
        ))
    return phone_calls[::-1]


def main():
    # random.seed(105)  # seed with dropped phone call
    for _ in range(10):
        pprint(generate_phone_data())


if __name__ == '__main__':
    main()
