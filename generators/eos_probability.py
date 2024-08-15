import datetime
from datetime import timedelta as td
import random
from pprint import pprint
from typing import TypeVar

import numpy as np

from constants import *
from schemas.string_eos import EOSType, Operator
from schemas.string_eos import *
from schemas.string_eos import psycho, consult
from schemas.eos_for_ukio_models import *
from generators import check_event_probability

T = TypeVar(
    "T",
    psycho,
    consult,
    card03,
    card02,
    card01,
    card04,
    cardAT,
    cardCommServ
)


def generate_card_from_eos_model(eos_value_dict: dict) -> T:
    if eos_value_dict.get('class'):
        eos_class = eos_value_dict['class']
        if eos_class == card01:
            # random_incident = list(IncidentType)[random.randint(0, len(list(IncidentType)) - 1)]
            return card01(
                dtCreate=datetime.datetime.now(),
                # strIncidentType=random_incident,
            )
        elif eos_class == cardAT:
            return cardAT(
                dtCreate=datetime.datetime.now(),
            )
        elif eos_class == 'consult':
            start_consult = datetime.datetime.now()
            return consult(
                dtConsultStart=start_consult,
                dtConsultEnd=start_consult + td(minutes=CONSULT_TIME // 60, seconds=CONSULT_TIME % 60)
            )

        elif eos_class == 'psycho':

            start_psycho = datetime.datetime.now()
            psycho_time = round(np.random.normal(AVG_PSYCHO_TIME, PSYCHO_SCALE), 3)
            return psycho(
                dtPsychoStart=start_psycho,
                dtPsychoEnd=start_psycho + td(minutes=int(psycho_time), seconds=psycho_time * 60 % 60)
            )
        elif eos_class == card04:
            dtCreate = datetime.datetime.now()
            return card04(
                dtCreate=dtCreate,
                dtConfirm=dtCreate + td(seconds=abs(np.random.normal(AVG_DEPARTMENT_ANSWER, DEPARTMENT_SCALE)))
            )
        else:
            return eos_class(dtCreate=datetime.datetime.now())


def _check_eos_probability(eos_value_dict: dict) -> EOSType:
    if check_event_probability(EOS_SHARE_MIN, EOS_SHARE_MAX):
        if check_event_probability(eos_value_dict['p_min'], eos_value_dict['p_max']):
            return True
    return False


def generate_random_eos_list() -> list[EOSType]:
    eos_list = []
    for eos_obj in EOSType:
        if eos_obj.value.get('p_min') is not None and eos_obj.value.get('class'):
            if _check_eos_probability(eos_obj):
                eos_list.append(eos_obj)
    return eos_list


# consult seed 30r
# Psycho seed 86
# random.seed(30)


def main():
    for _ in range(100000):
        d = generate_random_eos_list()
        print(d)


if __name__ == '__main__':
    main()
