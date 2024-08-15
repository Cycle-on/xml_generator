from enum import Enum

from constants import *
from schemas.eos_for_ukio_models import *


class EOSType(dict, Enum):
    s112 = {
        'name': 'Система 112',
        'code': "112",
        'p_min': CONSULT_SHARE_MIN,
        'p_max': CONSULT_SHARE_MAX,
        'class': "consult"

    }
    fireDepartment = {
        "name": 'Пожарная Служба',
        "code": "01",
        "p_min": FIRE_SHARE_MIN,
        'p_max': FIRE_SHARE_MAX,
        "class": card01
    }
    police = {
        "name": 'Полиция',
        "code": "02",
        "p_min": POLICE_SHARE_MIN,
        'p_max': POLICE_SHARE_MAX,
        "class": card02
    }
    ambulance = {
        "name": 'Скорая помощь',
        "code": "03",
        'p_min': AMBULANCE_SHARE_MIN,
        'p_max': AMBULANCE_SHARE_MAX,
        "class": card03
    }
    gasDepartment = {
        "name": 'Газовая служба',
        "code": "04",
        "p_min": GAS_SHARE_MIN,
        "p_max": GAS_SHARE_MAX,
        "class": card04
    }
    antiTerror = {
        "name": 'Антитеррор',
        "code": "05",
        "p_min": CARD_AT_SHARE_MIN,
        "p_max": CARD_AT_SHARE_MAX,
        "class": cardAT
    }
    houseDepartment = {
        "name": "ЖКХ",
        "code": "06",
        "class": cardCommServ,
    }
    edds = {
        "name": "ЕДДС",
        "code": "07",
        "p_min": EDDS_SHARE_MIN,
        "p_max": EDDS_SHARE_MAX
    }
    psycho = {
        "name": "Психологическая поддержка",
        "code": "08",
        "p_min": PSYCHO_SHARE_MIN,
        'p_max': PSYCHO_SHARE_MAX,
        "class": "psycho"
    }
    translators = {
        "name": "Переводчики",
        "code": "09"
    }
    mchs = {
        "name": "МЧС",
        "code": "10",
        "p_min": MCHS_SHARE_MIN,
        "p_max": MCHS_SHARE_MAX,
    }
    rosGuardian = {
        "name": "Росгвардия",
        "code": "11",
        "p_min": ROSGV_SHARE_MIN,
        "p_max": ROSGV_SHARE_MAX}
    flyForestSecurity = {
        "name": 'ФБУ "Авиалесоохрана"',
        "code": "12",
        "p_min": AVIALES_SHARE_MIN,
        "p_max": AVIALES_SHARE_MAX
    }
    rosAutoDor = {
        "name": "Росавтодор",
        "code": "13",
        "p_min": ROSAVTODOR_SHARE_MIN,
        "p_max": ROSAVTODOR_SHARE_MAX,
    }
    rosLesXoz = {
        "name": "Рослесхоз",
        "code": "14",
        "p_min": ROSLESHOZ_SHARE_MIN,
        "p_max": ROSLESHOZ_SHARE_MAX
    }


class Operator(BaseModelWithId):
    operatorId: str = Field(default_factory=lambda: Operator._BaseModelWithId__get_next_id())
    eosClassTypeId: list[EOSType] = None


class consult(BaseModelWithId):
    consultId: str = Field(default_factory=lambda: consult._BaseModelWithId__get_next_id())
    dtConsultStart: datetime.datetime
    dtConsultEnd: datetime.datetime


class psycho(BaseModelWithId):
    psychoid: str = Field(default_factory=lambda: psycho._BaseModelWithId__get_next_id())
    dtPsychoStart: datetime.datetime
    dtPsychoEnd: datetime.datetime


if __name__ == '__main__':
    o1 = Operator(
        eosClassTypeId=[EOSType.s112]
    )
    print(o1.eosClassTypeId)
