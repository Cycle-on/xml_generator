from datetime import timedelta as td
from typing import TypeVar

import numpy as np

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


def generate_card_from_eos_model(eos_value_dict: dict, date_from: datetime.datetime) -> T:
    """
    take eos_class from string_eos and converts it to the model in eos_for_ukio_models
    :param eos_value_dict: dict with eos models from string_eos
    :param date_from
    :return:
    """
    if eos_value_dict.get('class'):
        eos_class = eos_value_dict['class']
        if eos_class == 'consult':
            start_consult = date_from
            return consult(
                dtConsultStart=start_consult,
                dtConsultEnd=start_consult + td(minutes=CONSULT_TIME // 60, seconds=CONSULT_TIME % 60)
            )

        elif eos_class == 'psycho':

            start_psycho = date_from
            psycho_time = round(np.random.normal(AVG_PSYCHO_TIME, PSYCHO_SCALE), 3)
            return psycho(
                dtPsychoStart=start_psycho,
                dtPsychoEnd=start_psycho + td(minutes=int(psycho_time), seconds=psycho_time * 60 % 60)
            )
        elif eos_class == card04:
            return card04(
                dtCreate=date_from,
                dtConfirm=date_from + td(seconds=abs(np.random.normal(AVG_DEPARTMENT_ANSWER, DEPARTMENT_SCALE)))
            )
        else:
            return eos_class(
                dtCreate=date_from + td(
                    seconds=abs(np.random.normal(AVERAGE_EOS_CARD_CREATE_TIME, EOS_CARD_CREATE_SCALE))
                )
            )


def _check_eos_probability(eos_value_dict: dict) -> bool:
    """
    takes string_eos and check eos probability by p_min and p_max
    :param eos_value_dict: dict from string_eos
    :return:
    """
    if check_event_probability(EOS_SHARE_MIN, EOS_SHARE_MAX):
        return check_event_probability(eos_value_dict['p_min'], eos_value_dict['p_max'])


def generate_random_eos_list() -> list[EOSType]:
    """
    creates a list with random eos dicts from string_eos

    :return:
    """
    eos_list = []
    for eos_obj in EOSType:
        if eos_obj.value.get('p_min') is not None and eos_obj.value.get('class'):
            if _check_eos_probability(eos_obj):
                eos_list.append(eos_obj)
    return eos_list


# consult seed 30
# Psycho seed 86
# random.seed(30)


def main():
    for _ in range(100000):
        d = generate_random_eos_list()
        print(d)


if __name__ == '__main__':
    main()
