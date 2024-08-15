import datetime

from schemas.string_eos import EOSType, Operator, Consult, Psycho

from schemas.eos_for_ukio_models import *
from schemas.string_schemas import CallSource, IncidentType, CardStates
from schemas.phone import Phone

from pydantic import Field
from schemas import BaseModelWithId

class TransferItem(BaseModelWithId):
    receptionItemId: str = Field(default_factory=lambda: TransferItem._BaseModelWithId__get_next_id())

    eosClassTypeId: EOSType
    dtTransfer: datetime.datetime
    success: bool


class ReceptionItem(BaseModelWithId):
    receptionItemId: str = Field(default_factory=lambda: ReceptionItem._BaseModelWithId__get_next_id())
    eosClassTypeId: EOSType
    dtConfirmMessage: datetime.datetime
    bSuccess: bool


class SensorMessage(BaseModelWithId):
    operator: Operator = None
    dtSensorMessage: datetime.datetime


class Sms(BaseModelWithId):
    dtSms: datetime.datetime


class OtherMessage(BaseModelWithId):
    operator: Operator = None
    dtOtherMessage: datetime.datetime


class Era(BaseModelWithId):
    operator: Operator
    dtEra: datetime.datetime = None
    callType: bool


class Card(BaseModelWithId):
    globalId: str = Field(default_factory=lambda: Card._BaseModelWithId__get_next_id())
    cardState: CardStates = None
    incidentType: IncidentType = None
    dtSend_: datetime.datetime = datetime.datetime.now()
    dtCreate: datetime.datetime = datetime.datetime.now()
    dtUpdate: datetime.datetime = datetime.datetime.now()
    casualties: int = None
    humanThreat: bool = False
    chs: bool = False
    callSource: CallSource = None
    phoneCalls: list[Phone] = None
    era: Era = None
    sensorMessages: list[SensorMessage] = None
    sms: list[Sms] = None
    otherMessages: list[OtherMessage] = None
    transferItem: list[TransferItem] = None
    receptionItems: list[ReceptionItem] = None
    card01: Card01 = None
    card02: Card02 = None
    card03: Card03 = None
    card04: Card04 = None
    cardCommServ: CardCommServ = None
    cardAT: CardAT = None
    wrong: bool
    bChildPlay: bool
    consult: Consult = None
    psycho: Psycho = None
