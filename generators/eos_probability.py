from datetime import timedelta as td
import random
from typing import TypeVar

import numpy as np

from constants import *
from schemas import EOSType, Operator
from schemas.eos_models import *
from schemas import Psycho, Consult

from generators import check_event_probability

T = TypeVar(
    "T",
    Psycho,
    Consult,
    Ambulance,
    Police,
    FireDepartment,
    GasDepartment,
    AntiTerror,
    HouseDepartment
)


def _generate_card_from_eos_model(eos_value_dict: dict) -> T:
    if eos_value_dict.get('class'):

        eos_class = eos_value_dict['class']
        if eos_class == FireDepartment:
            random_incident = list(IncidentType)[random.randint(0, len(list(IncidentType)) - 1)]
            return FireDepartment(
                dtCreate=datetime.datetime.now(),
                strIncidentType=random_incident,
            )
        elif eos_class == AntiTerror:
            return AntiTerror(
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
