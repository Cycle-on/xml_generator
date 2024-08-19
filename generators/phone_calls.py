import datetime
from datetime import timedelta as td
import random
from pprint import pprint

from generators.eos_probability import generate_random_eos_list
import numpy as np

from constants import *
from config import load_config
from schemas.string_eos import Operator
from schemas.phonecall import PhoneCall, Call
from generators import check_event_probability
from schemas.string_schemas import CardStates

config = load_config()


def generate_call_from_phone_call(phone_call: PhoneCall) -> Call:
    return Call(
        strCallStatus=random.choice(list(CardStates)),
        PhoneCall=phone_call,
        PhoneCallID=phone_call.phoneCallId,
        dtCall=phone_call.dtCall,
    )


def generate_phone_date(recall: bool = False, dt_call=datetime.datetime.now(), **kwargs):
    """
    creating date params to PhoneCall model
    dt_call->dt_connect # step 1
    dt_connect -> phone_call_time # step 2
    :param recall:
    :param dt_call:
    :param kwargs: dict with step1, step2
    ** can change to one step, with True or datetime and check it with isinstance
    because it has different types
    :return:
    """
    if recall:
        # we have dropped call and we need some new params

        operator_recall_time = abs(np.random.normal(AVG_TIME_OPERATOR_RECALL_WAITING, OPERATOR_RECALL_WAITING_SCALE))
        dt_call += td(seconds=operator_recall_time)
        operator_wait_call_answer_time = abs(np.random.normal(AVG_TIME_OPERATOR_WAITING, OPERATOR_TIME_WAITING_SCALE))
        dt_connect = dt_call + td(seconds=operator_wait_call_answer_time)

    else:
        # base call from someone
        operator_reaction = abs(np.random.normal(OPERATOR_REACTION_TIME, OPERATOR_REACTION_TIME_SCALE))
        dt_connect = dt_call + td(seconds=operator_reaction)

    if kwargs.get('step2'):
        phone_call_time = kwargs.get('step2').second

    else:
        phone_call_time = abs(np.random.normal(AVERAGE_CARD_CREATE_TIME, CARD_CREATE_TIME_SCALE))

    dt_end_call = dt_connect + td(minutes=phone_call_time // 60,
                                  seconds=phone_call_time % 60)
    random_send_data_delay = random.randint(3, 5)
    date_send = dt_end_call + td(seconds=random_send_data_delay)
    return dt_call, dt_connect, dt_end_call, date_send


def generate_phone_data() -> list[PhoneCall]:
    """
    creating PhoneCall,
    if len(list) == 0, phone call not dropped,
    if len(list) == 1, phone call is dropped
    :return: list with phone calls models
    """
    phone_calls: list[PhoneCall] = []
    # random constants
    end_call_list = [True, False]
    random.shuffle(end_call_list)
    a, b = end_call_list

    # operator
    random_EOS = generate_random_eos_list()
    operator = Operator()
    dt_call, dt_connect, dt_end_call, date_send = generate_phone_date()
    date_send2 = None
    # phone date info
    if check_event_probability(config.dropped_call_probability,
                               config.dropped_call_probability):  # phone call is dropped
        dropped_timedelta = dt_end_call - dt_connect
        break_time = random.randint(0, dropped_timedelta.seconds)
        break_time_delta = td(seconds=break_time % 60, minutes=break_time // 60)
        step1_timedelta = dt_connect - dt_call
        dt_end_call = dt_call + break_time_delta
        if break_time_delta < step1_timedelta:
            dt_call2, dt_connect2, dt_end_call2, date_send2 = generate_phone_date(
                recall=True,
                dt_call=dt_call + break_time_delta,
                step1=True
            )

        else:  # step 2: dt_end_call - dt_connect
            dt_call2, dt_connect2, dt_end_call2, date_send2 = generate_phone_date(
                recall=True,
                dt_call=dt_call + break_time_delta,
                step2=dt_end_call - break_time_delta,

            )
        phone_calls.append(
            PhoneCall(
                dtSend=date_send2,
                OperatorId=operator.operatorId,
                bOperatorIniciatied=True,
                dtCall=dt_call2,
                dtConnect=dt_connect2,
                bCallEnded=b,
                aCallEnded=a,
                dtEndCall=dt_end_call2,

            )
        )
    phone_calls.append(
        PhoneCall(
            dtSend=date_send2 if date_send2 is not None else date_send,
            OperatorId=operator.operatorId,
            bOperatorIniciatied=False,
            dtCall=dt_call,
            dtConnect=dt_connect,
            bCallEnded=b,
            aCallEnded=a,
            dtEndCall=dt_end_call,
            # redirectCall=redirect_call
        ))
    return phone_calls[::-1]


def main():
    # random.seed(105)  # seed with dropped phone call
    for _ in range(10):
        pprint(generate_phone_data())


if __name__ == '__main__':
    main()
