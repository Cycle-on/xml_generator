from enum import Enum


class CallSource(str, Enum):
    mobile_phone = 'Мобильный телефон'
    s112 = 'Служба 112'
    sms = 'SMS'
    sensor = 'Датчик'


class CardStates(str, Enum):
    status1 = 'status1'
    status2 = 'status2'
    status3 = 'status3'


class IncidentType(str, Enum):
    type1 = "type1"
    type2 = "type2"
    type3 = "type3"
