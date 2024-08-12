from schemas import EOSType, Operator, Consult, Psycho
from schemas.eos_models import *
from schemas.string_schemas import CallSource, IncidentType, CardStates
from schemas.phone import Phone

from pydantic import BaseModel, Field


class TransferItem(BaseModel):
    eosClassTypeId: EOSType
    dtTransfer: datetime.datetime
    success: bool


class ReceptionItem(BaseModel):
    eosClassTypeId: EOSType
    dtConfirmMessage: datetime.datetime
    bSuccess: bool


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


class Card(BaseModel):
    globalId: str = Field(default_factory=lambda: Card.__get_next_id())
    cardState: CardStates = None
    incidentType: IncidentType = None
    dtSend_: datetime.datetime = datetime.datetime.now()
    dtCreate: datetime.datetime = datetime.datetime.now()
    dtUpdate: datetime.datetime = datetime.datetime.now()
    casualties: int = None
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

# if __name__ == '__main__':
#     print(isinstance(Police(dtCreate=datetime.datetime.now()), BaseModel))
