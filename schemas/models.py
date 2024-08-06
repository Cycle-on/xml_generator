import datetime
from typing import ClassVar

from schemas.string_schemas import CallSource, IncidentType, CardStates
from pydantic import BaseModel, Field

from schemas.Phone import Phone
from schemas import Operator, EOSType


class SensorMessage(BaseModel):
    operator: Operator = None
    dtSensorMessage: datetime.datetime


class Sms(BaseModel):
    dtSms: datetime.datetime


class OtherMessage(BaseModel):
    operator: Operator = None
    dtOtherMessage: datetime.datetime


class Era(BaseModel):
    operator: Operator
    dtEra: datetime.datetime = None
    callType: bool


class TransferItem(BaseModel):
    eosClassTypeId: EOSType
    dtTransfer: datetime.datetime
    success: bool


class ReceptionItem(BaseModel):
    eosClassTypeId: EOSType
    dtConfirmMessage: datetime.datetime
    bSuccess: bool


class FireDepartment(BaseModel):
    dtCreate: datetime.datetime
    strIncidentType: IncidentType
    strObject: str
    bObjectGasified: bool


class Police(BaseModel):
    dtCreate: datetime.datetime


class Ambulance(BaseModel):
    dtCreate: datetime.datetime


class GasDepartment(BaseModel):
    dtCreate: datetime.datetime


class HouseDepartment(BaseModel):
    dtCreate: datetime.datetime


class AntiTerror(BaseModel):
    dtCreate: datetime.datetime
    strInjurySuspect: str = None


class Consult(BaseModel):
    consultId: str = Field(default_factory=lambda: Consult.__get_next_id())
    operator: Operator
    dtConsultStart: datetime.datetime
    dtConsultEnd: datetime.datetime

    __id_counter: ClassVar[int] = 0

    @classmethod
    def __get_next_id(cls):
        cls.__id_counter += 1
        return str(cls.__id_counter)


class Psycho(BaseModel):
    psychoId: str = Field(default_factory=lambda: Psycho.__get_next_id())
    operator: Operator
    bPsychoInHouse: bool
    dtPsychoStart: datetime.datetime
    dtPsychoEnd: datetime.datetime

    __id_counter: ClassVar[int] = 0

    @classmethod
    def __get_next_id(cls):
        cls.__id_counter += 1
        return str(cls.__id_counter)


class Card(BaseModel):
    globalId: str = Field(default_factory=lambda: Card.__get_next_id())
    cardState: CardStates = None
    incidentType: IncidentType = None
    dtSend_: datetime.datetime = datetime.datetime.now()
    dtCreate: datetime.datetime = datetime.datetime.now()
    dtUpdate: datetime.datetime = datetime.datetime.now()
    casualties: int = 0
    humanThreat: bool = False
    chs: bool = False  # Чрезвычайная ситуация или нет
    callSource: CallSource = None
    phoneCalls: list[Phone] = None
    era: Era = None
    sensorMessages: list[SensorMessage] = None
    sms: list[Sms] = None
    otherMessages: list[OtherMessage] = None
    transferItem: list[TransferItem] = None
    receptionItems: list[ReceptionItem] = None
    card01: FireDepartment = None
    card02: Police = None
    card03: Ambulance = None
    card04: GasDepartment = None
    cardCommServ: HouseDepartment = None
    cardAT: AntiTerror = None
    wrong: bool
    childPlay: bool
    consult: Consult = None
    psycho: Psycho = None

    __id_counter: ClassVar[int] = 0

    @classmethod
    def __get_next_id(cls):
        cls.__id_counter += 1
        return str(cls.__id_counter)


if __name__ == '__main__':
    print(isinstance(Police(dtCreate=datetime.datetime.now()), BaseModel))
