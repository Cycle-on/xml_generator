from enum import Enum

from config.config_data import *
from schemas.eos_for_ukio_models import *


class StringEosType(dict, Enum):
    s112 = {
        'name': 'Система 112',
        'code': "112",
        'p_min': CONSULT_SHARE_MIN,
        'p_max': CONSULT_SHARE_MAX,
        'class': "consult",
        "id": 1,

    }
    fireDepartment = {
        "name": 'Пожарная Служба',
        "code": "01",
        "p_min": FIRE_SHARE_MIN,
        'p_max': FIRE_SHARE_MAX,
        "class": "card01",
        "id": 2,
    }
    police = {
        "name": 'Полиция',
        "code": "02",
        "p_min": POLICE_SHARE_MIN,
        'p_max': POLICE_SHARE_MAX,
        "class": "card02",
        "id": 3,
    }
    ambulance = {
        "name": 'Скорая помощь',
        "code": "03",
        'p_min': AMBULANCE_SHARE_MIN,
        'p_max': AMBULANCE_SHARE_MAX,
        "class": "card03",
        "id": 4,
    }
    gasDepartment = {
        "name": 'Газовая служба',
        "code": "04",
        "p_min": GAS_SHARE_MIN,
        "p_max": GAS_SHARE_MAX,
        "class": "card04",
        "id": 5,
    }
    antiTerror = {
        "name": 'Антитеррор',
        "code": "05",
        "p_min": CARD_AT_SHARE_MIN,
        "p_max": CARD_AT_SHARE_MAX,
        "class": "cardat",
        "id": 6,
    }
    houseDepartment = {
        "name": "ЖКХ",
        "code": "06",
        "class": "cardcommserv",
        "id": 7,
    }
    edds = {
        "name": "ЕДДС",
        "code": "07",
        "p_min": EDDS_SHARE_MIN,
        "p_max": EDDS_SHARE_MAX,
        "id": 8,
    }
    psycho = {
        "name": "Психологическая поддержка",
        "code": "08",
        "p_min": PSYCHO_SHARE_MIN,
        'p_max': PSYCHO_SHARE_MAX,
        "class": "psycho",
        "id": 9,
    }
    translators = {
        "name": "Переводчики",
        "code": "09",
        "id": 10,
    }
    mchs = {
        "name": "МЧС",
        "code": "10",
        "p_min": MCHS_SHARE_MIN,
        "p_max": MCHS_SHARE_MAX,
        "id": 11,
    }
    rosGuardian = {
        "name": "Росгвардия",
        "code": "11",
        "p_min": ROSGV_SHARE_MIN,
        "p_max": ROSGV_SHARE_MAX,
        "id": 12,
    }
    flyForestSecurity = {
        "name": 'ФБУ "Авиалесоохрана"',
        "code": "12",
        "p_min": AVIALES_SHARE_MIN,
        "p_max": AVIALES_SHARE_MAX,
        "id": 13,
    }
    rosAutoDor = {
        "name": "Росавтодор",
        "code": "13",
        "p_min": ROSAVTODOR_SHARE_MIN,
        "p_max": ROSAVTODOR_SHARE_MAX,
        "id": 14,
    }
    rosLesXoz = {
        "name": "Рослесхоз",
        "code": "14",
        "p_min": ROSLESHOZ_SHARE_MIN,
        "p_max": ROSLESHOZ_SHARE_MAX,
        "id": 15,
    }


class Operator(BaseModelWithId):
    operatorId: str = Field(default_factory=lambda: Operator._BaseModelWithId__get_next_id())
    strOperatorPost: str = None
    strOperatorSurname: str = None
    strOperatorName: str = None
    strOperatorLastName: str = None
    strOperatorInfo: str = None
    isPsychologist: bool = None
    bOperatorTranslator: bool = None
    strLanguage: str = None
    eosClassTypeId: list[StringEosType] = None
    dtSend: datetime.datetime = None


class Arm(BaseModelWithId):
    armId: str = Field(default_factory=lambda: Arm._BaseModelWithId__get_next_id())
    strArmNumber: str = None
    strArmPlace: str = None
    dtSend: datetime.datetime = None


class ArmWork:
    armStatusId: str = None
    arm: Arm = None
    armId: str = None
    strArmStatus: str = None
    dtAction: datetime.datetime = None
    dtSend: datetime.datetime = None


class OperatorWork(BaseModelWithId):
    operatorStatusId: str = None
    strOperatorStatus: str = None
    dtAction: datetime.datetime = None
    operator: Operator = None
    operatorId: str = None
    arm: Arm = None
    armId: str = None
    dtSend: datetime.datetime = None


class Consult(BaseModelWithId):
    consultId: str = Field(default_factory=lambda: Consult._BaseModelWithId__get_next_id())
    operator: Operator = None
    operatorId: str = None
    dtConsultStart: datetime.datetime
    dtConsultEnd: datetime.datetime


class Psycho(BaseModelWithId):
    psychoId: str = Field(default_factory=lambda: Psycho._BaseModelWithId__get_next_id())
    operator: Operator = None
    operatorId: str = None
    bPsychoInHouse: bool = None
    dtPsychoStart: datetime.datetime
    dtPsychoEnd: datetime.datetime


if __name__ == '__main__':
    o1 = Operator(
        eosClassTypeId=[StringEosType.s112]
    )
    print(o1.eosClassTypeId)
