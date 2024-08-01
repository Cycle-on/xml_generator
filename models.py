import datetime

from string_schemas import CallSource, IncidentType
from pydantic import BaseModel

from schemas.Phone import Phone
from schemas import Operator, EOSType


class SensorMessage(BaseModel):
    operator: Operator = ''
    dtSensorMessage: datetime.datetime


class Sms(BaseModel):
    dtSms: datetime.datetime


class OtherMessage(BaseModel):
    operator: Operator = ''
    dtOtherMessage: datetime.datetime


class Era(BaseModel):
    operator: Operator
    dtEra: datetime.datetime = ''
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
    strInjurySuspect: str = ''


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
    cardState: str = ''
    incidentType: str = ''
    dtSend_: datetime.datetime = datetime.datetime.now()
    dtCreate: datetime.datetime = datetime.datetime.now()
    dtUpdate: datetime.datetime = datetime.datetime.now()
    casualties: int = 0
    humanThreat: bool = False
    chs: bool = False  # Чрезвычайная ситуация или нет
    callSource: CallSource = ''
    phoneCalls: list[Phone] = []
    era: Era = ''
    sensorMessages: list[SensorMessage] = []
    sms: list[Sms] = []
    otherMessages: list[OtherMessage] = []
    transferItem: list[TransferItem] = []
    receptionItems: list[ReceptionItem] = []
    card01: FireDepartment = ''
    card02: Police = ''
    card03: Ambulance = ''
    card04: GasDepartment = ''
    cardCommServ: HouseDepartment = ''
    cardAT: AntiTerror = ''
    wrong: bool
    childPlay: bool
    consult: Consult = ''
    psycho: Psycho = ''


if __name__ == '__main__':
    Card(
        globalId='1',
        wrong=True,
        childPlay=True
    )
