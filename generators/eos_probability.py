import datetime
import random
from typing import TypeVar

from constants import *
from schemas import EOSType
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


def generate_eos_card(eos_value_dict: dict) -> T:
    if check_event_probability(EOS_SHARE_MIN, EOS_SHARE_MAX):
        if check_event_probability(eos_value_dict['p_min'], eos_value_dict['p_max']):
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

                elif eos_class == FireDepartment:
                    return eos_class(dtCreate=datetime.datetime.now())


def main():
    for eos_obj in EOSType:
        if eos_obj.value.get('p_min'):
            # print(eos_obj.value['name'])
            generate_eos_card(eos_obj)


if __name__ == '__main__':
    main()
