import datetime

from schemas.string_schemas import CallSource, IncidentType
from pydantic import BaseModel

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
    consultId: str
    operator: Operator
    dtConsultStart: datetime.datetime
    dtConsultEnd: datetime.datetime


class Psycho(BaseModel):
    psychoId: str
    operator: Operator
    bPsychoInHouse: bool
    dtPsychoStart: datetime.datetime
    dtPsychoEnd: datetime.datetime


class Card(BaseModel):
    globalId: str
    cardState: str = None
    incidentType: str = None
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


if __name__ == '__main__':
    print(isinstance(Police(dtCreate=datetime.datetime.now()), BaseModel))
