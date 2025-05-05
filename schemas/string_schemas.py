from enum import Enum


class CallSource(str, Enum):
    mobile_phone = "Мобильный телефон"
    s112 = "Служба 112"
    sms = "SMS"
    sensor = "Датчик"


class CardStates(str, Enum):
    status1 = "status1"
    status2 = "status2"
    status3 = "status3"


class IncidentTypes(str, Enum):
    type1 = "type1"
    type2 = "type2"
    type3 = "type3"


class EosResourceUnitNames(str, Enum):
    name1 = "Бригада 1"
    name2 = "Бригада 2"
    name3 = "Бригада 3"
