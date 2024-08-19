from schemas.string_eos import EOSType, Operator, consult, psycho

from schemas.eos_for_ukio_models import *
from schemas.string_schemas import CallSource, IncidentType, CardStates
from schemas.phonecall import PhoneCall

from pydantic import Field, BaseModel
from schemas import BaseModelWithId


class TransferItem(BaseModelWithId):
    transferItemId: str = Field(default_factory=lambda: TransferItem._BaseModelWithId__get_next_id())
    eosClassTypeId: EOSType
    dtTransfer: datetime.datetime
    bSuccess: bool


class ReceptionItem(BaseModelWithId):
    receptionItemId: str = Field(default_factory=lambda: ReceptionItem._BaseModelWithId__get_next_id())
    eosClassTypeId: EOSType
    dtConfirmMessage: datetime.datetime
    bSuccess: bool


class SensorMessage(BaseModelWithId):
    operator: Operator = None
    dtSensorMessage: datetime.datetime


class Sms(BaseModelWithId):
    smsId: str = Field(default_factory=lambda: Sms._BaseModelWithId__get_next_id())
    dtSms: datetime.datetime


class OtherMessage(BaseModelWithId):
    otherMessageId: str = Field(default_factory=lambda: OtherMessage._BaseModelWithId__get_next_id())
    dtOtherMessage: datetime.datetime


class Era(BaseModelWithId):
    eraId: str = Field(default_factory=lambda: Era._BaseModelWithId__get_next_id())
    dtEra: datetime.datetime = None


class CallContent:
    pass


class EosItem:
    pass


class Address:
    pass


class Ukio(BaseModelWithId):
    globalId: str = Field(default_factory=lambda: Ukio._BaseModelWithId__get_next_id())
    parentGlobalId: str = None
    strCardState: CardStates = None
    strIncidentType: IncidentType = None
    dtSend: datetime.datetime = datetime.datetime.now()
    dtCreate: datetime.datetime = datetime.datetime.now()
    dtUpdate: datetime.datetime = datetime.datetime.now()
    nCasualties: int = None
    bHumanThreat: bool = False
    bChs: bool = False
    strCallSource: CallSource = None
    bWrong: bool = None
    bChildPlay: bool
    phoneCall: list[PhoneCall] = None
    PhoneCallID: list[str] = None
    bRelocated: bool = None
    strRegionTransfer: str = None
    CallContent: CallContent = None
    Address: Address = None
    era: Era = None
    sensorMessages: list[SensorMessage] = None
    sms: list[Sms] = None
    otherMessages: list[OtherMessage] = None
    Psycho: psycho = None
    Consult: consult = None
    TransferItem: list[TransferItem] = None
    ReceptionItems: list[ReceptionItem] = None
    EosItem: EosItem = None
    Card01: card01 = None
    Card02: card02 = None
    Card03: card03 = None
    Card04: card04 = None
    CardAT: cardAT = None
    CardCommServ: cardCommServ = None


class Ukios(BaseModel):
    Ukios: list[Ukio]
