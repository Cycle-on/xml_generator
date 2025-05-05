import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from config.config_data import ALL_PROJ_CONSTANTS
from schemas import BaseModelWithId


class StringEos(BaseModel):
    name: str
    code: str
    p_min: Optional[int] = None
    p_max: Optional[int] = None
    id: int
    class_: Optional[str] = ""


class StringEosType(BaseModel):
    values: list[StringEos]


def get_string_eos_type():
    class StringEosTypeStrings(dict, Enum):
        s112 = {
            "name": "Система 112",
            "code": "112",
            "p_min": ALL_PROJ_CONSTANTS["CONSULT_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["CONSULT_SHARE_MAX"],
            "class": "consult",
            "id": 1,
        }
        fireDepartment = {
            "name": "Пожарная служба",
            "code": "01",
            "p_min": ALL_PROJ_CONSTANTS["FIRE_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["FIRE_SHARE_MAX"],
            "class": "card01",
            "id": 2,
        }
        police = {
            "name": "Полиция",
            "code": "02",
            "p_min": ALL_PROJ_CONSTANTS["POLICE_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["POLICE_SHARE_MAX"],
            "class": "card02",
            "id": 3,
        }
        ambulance = {
            "name": "Скорая помощь",
            "code": "03",
            "p_min": ALL_PROJ_CONSTANTS["AMBULANCE_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["AMBULANCE_SHARE_MAX"],
            "class": "card03",
            "id": 4,
        }
        gasDepartment = {
            "name": "Газовая служба",
            "code": "04",
            "p_min": ALL_PROJ_CONSTANTS["GAS_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["GAS_SHARE_MAX"],
            "class": "card04",
            "id": 5,
        }
        antiTerror = {
            "name": "Антитеррор",
            "code": "05",
            "p_min": ALL_PROJ_CONSTANTS["CARD_AT_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["CARD_AT_SHARE_MAX"],
            "class": "cardat",
            "id": 6,
        }
        houseDepartment = {
            "name": "ЖКХ",
            "code": "06",
            "class": "cardcommserv",
            "id": 7,
            "p_min": ALL_PROJ_CONSTANTS["CARD_CS_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["CARD_CS_SHARE_MAX"],
        }
        edds = {
            "name": "ЕДДС",
            "code": "07",
            "p_min": ALL_PROJ_CONSTANTS["EDDS_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["EDDS_SHARE_MAX"],
            "id": 8,
        }
        psycho = {
            "name": "Психологическая поддержка",
            "code": "08",
            "p_min": ALL_PROJ_CONSTANTS["PSYCHO_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["PSYCHO_SHARE_MAX"],
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
            "p_min": ALL_PROJ_CONSTANTS["MCHS_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["MCHS_SHARE_MAX"],
            "id": 11,
        }
        rosGuardian = {
            "name": "Росгвардия",
            "code": "11",
            "p_min": ALL_PROJ_CONSTANTS["ROSGV_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["ROSGV_SHARE_MAX"],
            "id": 12,
        }
        flyForestSecurity = {
            "name": 'ФБУ "Авиалесоохрана"',
            "code": "12",
            "p_min": ALL_PROJ_CONSTANTS["AVIALES_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["AVIALES_SHARE_MAX"],
            "id": 13,
        }
        rosAutoDor = {
            "name": "Росавтодор",
            "code": "13",
            "p_min": ALL_PROJ_CONSTANTS["ROSAVTODOR_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["ROSAVTODOR_SHARE_MAX"],
            "id": 14,
        }
        rosLesXoz = {
            "name": "Рослесхоз",
            "code": "14",
            "p_min": ALL_PROJ_CONSTANTS["ROSLESHOZ_SHARE_MIN"],
            "p_max": ALL_PROJ_CONSTANTS["ROSLESHOZ_SHARE_MAX"],
            "id": 15,
        }

    values = []
    for el in StringEosTypeStrings:
        d = {}
        for k, v in el.items():
            if "class" in k:
                k = "class_"
            d[k] = v
        values.append(StringEos(**d))
    return StringEosType(values=values)


class Operator(BaseModelWithId):
    operatorId: str = Field(
        default_factory=lambda: Operator._BaseModelWithId__get_next_id()
    )
    strOperatorPost: str = None
    strOperatorSurname: str = None
    strOperatorName: str = None
    strOperatorLastName: str = None
    strOperatorInfo: str = None
    isPsychologist: bool = None
    bOperatorTranslator: bool = None
    strLanguage: list[str] = None
    eosClassTypeId: list[StringEosType] = None
    dtSend: datetime.datetime = None


class Arm(BaseModelWithId):
    armId: str = Field(default_factory=lambda: Arm._BaseModelWithId__get_next_id())
    strArmNumber: str = None
    strArmPlace: str = None
    dtSend: datetime.datetime = None


class ArmWork(BaseModelWithId):
    armStatusId: str = Field(
        default_factory=lambda: ArmWork._BaseModelWithId__get_next_id()
    )
    arm: Arm = None
    armId: str = None
    strArmStatus: str = None
    dtAction: datetime.datetime = None
    dtSend: datetime.datetime = None


class OperatorWork(BaseModelWithId):
    operatorStatusId: str = Field(
        default_factory=lambda: OperatorWork._BaseModelWithId__get_next_id()
    )
    strOperatorStatus: str = None
    dtAction: datetime.datetime = None
    operator: Operator = None
    operatorId: str = None
    arm: Arm = None
    armId: str = None
    dtSend: datetime.datetime = None


class Consult(BaseModelWithId):
    consultId: str = Field(
        default_factory=lambda: Consult._BaseModelWithId__get_next_id()
    )
    operator: Operator = None
    operatorId: str = None
    dtConsultStart: datetime.datetime
    dtConsultEnd: datetime.datetime


class Psycho(BaseModelWithId):
    psychoId: str = Field(
        default_factory=lambda: Psycho._BaseModelWithId__get_next_id()
    )
    operator: Operator = None
    operatorId: str = None
    bPsychoInHouse: bool = None
    dtPsychoStart: datetime.datetime
    dtPsychoEnd: datetime.datetime


class OperatorWorks(BaseModel):
    operatorWork: list[OperatorWork]


class ArmWorks(BaseModel):
    armWork: list[ArmWork]


class IncidentType(BaseModel):
    incidentId: int
    parentIncidentId: int = None
    incidentTitle: str = None
    eosClassTypeId: list[int] = None
    dtSend: datetime.datetime = None


class IncidentTypes(BaseModel):
    incidentType: list[IncidentType]
