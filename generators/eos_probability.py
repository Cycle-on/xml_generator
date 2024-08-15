from datetime import timedelta as td
import random
from typing import TypeVar

import numpy as np

from constants import *
from schemas.string_eos import EOSType, Operator
from schemas.string_eos import *
from schemas.string_eos import Psycho, Consult
from schemas.eos_for_ukio_models import *
from generators import check_event_probability

T = TypeVar(
    "T",
    Psycho,
    Consult,
    Card03,
    Card02,
    Card01,
    Card04,
    CardAT,
    CardCommServ
)


def generate_card_from_eos_model(eos_value_dict: dict) -> T:
    if eos_value_dict.get('class'):
        eos_class = eos_value_dict['class']
        if eos_class == Card01:
            # random_incident = list(IncidentType)[random.randint(0, len(list(IncidentType)) - 1)]
            return Card01(
                dtCreate=datetime.datetime.now(),
                # strIncidentType=random_incident,
            )
        elif eos_class == CardAT:
            return CardAT(
                dtCreate=datetime.datetime.now(),
            )
        elif eos_class == 'Consult':
            start_consult = datetime.datetime.now()
            return Consult(
                operator=Operator(
                    eosClassTypeId=[EOSType.s112]
                ),
                dtConsultStart=start_consult,
                dtConsultEnd=start_consult + td(minutes=CONSULT_TIME // 60, seconds=CONSULT_TIME % 60)
            )

        elif eos_class == 'Psycho':

            start_psycho = datetime.datetime.now()
            psycho_time = round(np.random.normal(AVG_PSYCHO_TIME, PSYCHO_SCALE), 3)
            return Psycho(
                operator=Operator(
                    eosClassTypeId=[EOSType.psycho],
                ),
                bPsychoInHouse=False,
                dtPsychoStart=start_psycho,
                dtPsychoEnd=start_psycho + td(minutes=int(psycho_time), seconds=psycho_time * 60 % 60)
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
        if eos_obj.value.get('p_min') is not None:
            if _check_eos_probability(eos_obj):
                eos_list.append(eos_obj)
    return eos_list


# consult seed 30
# Psycho seed 86
# random.seed(<int>)


def main():
    print(generate_random_eos_list())
    pass


if __name__ == '__main__':
    main()
