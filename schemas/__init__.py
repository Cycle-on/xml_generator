from enum import Enum

from pydantic import BaseModel


class EOSType(dict, Enum):
    s112 = {'name': 'Система 112', 'code': "112"}
    fireDepartment = {"name": 'Пожарная Служба', "code": "01"}
    police = {"name": 'Полиция', "code": "02"}
    Ambulance = {"name": 'Скорая помощь', "code": "03"}
    GasDepartment = {"name": 'Газовая служба', "code": "04"}
    AntiTerror = {"name": 'Антитеррор', "code": "05"}
    HouseDepartment = {"name": "ЖКХ", "code": "06"}
    edds = {"name": "ЕДДС", "code": "07"}
    psycho = {"name": "Психологическая поддержка", "code": "08"}
    translators = {"name": "Переводчики", "code": "09"}
    mchs = {"name": "МЧС", "code": "10"}
    rosGuardian = {"name": "Росгвардия", "code": "11"}
    flyForestSecurity = {"name": 'ФБУ "Авиалесоохрана"', "code": "12"}
    rosAutoDor = {"name": "Росавтодор", "code": "13"}
    rosLesXoz = {"name": "Рослесхоз", "code": "14"}


class Operator(BaseModel):
    operatorId: str
    eosClassTypeId: list[EOSType] = []
