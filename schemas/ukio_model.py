from constants import files_prefix
from schemas.string_eos import StringEosType, Operator, Consult, Psycho

from schemas.eos_for_ukio_models import *
from schemas.string_schemas import CallSource, IncidentTypes, CardStates, EosResourceUnitNames
from schemas.phonecall import PhoneCall

from pydantic import Field, BaseModel
from schemas import BaseModelWithId
from decimal import Decimal


class TransferItem(BaseModelWithId):
    transferItemId: str = Field(default_factory=lambda: TransferItem._BaseModelWithId__get_next_id())
    eosClassTypeId: str
    dtTransfer: datetime.datetime
    bSuccess: bool


class ReceptionItem(BaseModelWithId):
    receptionItemId: str = Field(default_factory=lambda: ReceptionItem._BaseModelWithId__get_next_id())
    eosClassTypeId: StringEosType
    dtConfirmMessage: datetime.datetime
    bSuccess: bool


class SensorMessage(BaseModelWithId):
    sensorMessageId: str = Field(default_factory=lambda: SensorMessage._BaseModelWithId__get_next_id())
    operator: Operator = None
    operatorId: str = None
    strSensorMessage: str = None
    strSensorInfo: str = None
    dtSensorMessage: datetime.datetime


class Sms(BaseModelWithId):
    smsId: str = Field(default_factory=lambda: Sms._BaseModelWithId__get_next_id())
    dtSms: datetime.datetime
    strSms: str = None
    strPhoneNumber: str = None
    smsLatitude: Decimal = None
    smsLongitude: Decimal = None
    smsCoordAccuracy: int = None


class OtherMessage(BaseModelWithId):
    otherMessageId: str = Field(default_factory=lambda: OtherMessage._BaseModelWithId__get_next_id())
    strMessageType: str = None
    Operator: Operator = None
    dtOtherMessage: datetime.datetime
    strMessageContent: str = None


class Era(BaseModelWithId):
    eraId: str = Field(default_factory=lambda: Era._BaseModelWithId__get_next_id())
    Operator: Operator = None
    operatorId: str = None
    dtEra: datetime.datetime = None
    bCallType: bool = None
    bTriggeringType: bool = None
    bPresenceCasualties: bool = None
    bVoiceCommTransport: bool = None
    strVehicleType: str = None
    strVIN: str = None
    strEngineType: str = None
    iVehiclePropulsionStorageType: str = None
    strRegistryNumber: str = None
    strVehicleBodyColor: str = None
    strVehicleModel: str = None
    iDirection: int = None
    geoLatitude1: Decimal = None
    geoLongitude1: Decimal = None
    geoLatitude2: Decimal = None
    geoLongitude2: Decimal = None
    bDataReliability: bool = None
    dtGeo1Time: datetime.datetime = None
    dtGeo2Time: datetime.datetime = None
    nPassengers: int = None
    strCallShortId: str = None
    strCallId: str = None
    bFrontCrash: bool = None
    bLeftCrash: bool = None
    bRightCrash: bool = None
    bSideCrash: bool = None
    bRearCrash: bool = None
    bRollover: bool = None
    bOtherCrashType: bool = None
    phoneCallId: str = None


class DispatchService(BaseModelWithId):
    dispatchServiceId: str = Field(default_factory=lambda: DispatchService._BaseModelWithId__get_next_id())
    eosClassTypeId: int = None
    strDispatchServiceName: str = None


class CallContent(BaseModelWithId):
    callContentId: str = Field(default_factory=lambda: CallContent._BaseModelWithId__get_next_id())
    strLastName: str = None
    strName: str = None
    strMiddleName: str = None
    strCallerContactPhone: str = None
    strCgPN: str = None
    strAddressDevice: str = None
    appResAddress: str = None
    strLanguage: str = None
    strIncidentDescription: str
    appLatitude: Decimal = None
    appLongitude: Decimal = None
    appCoordAccuracy: int = None
    appLocAddress: str
    appLocAddressKLADR: str = None
    appLocAddressFIAS: str = None


class EosResource(BaseModelWithId):
    eosResourceId: str = Field(default_factory=lambda: EosResource._BaseModelWithId__get_next_id())
    eosClassTypeId: int = None
    strResourceUnitName: str = None
    strMembership: str = None


class EosItem(BaseModelWithId):
    assignId: str = Field(default_factory=lambda: EosItem._BaseModelWithId__get_next_id())
    operator: Operator = None
    operatorId: str = None
    dtDepart: datetime.datetime = None
    dtConfirmDepart: datetime.datetime | None = None
    dtArrival: datetime.datetime | None = None
    dtComplete: datetime.datetime | None = None
    dtCancel: datetime.datetime | None = None
    dispatchService: DispatchService
    eosResource: list[EosResource] | None = None


class Address(BaseModelWithId):
    addressId: str = Field(default_factory=lambda: Address._BaseModelWithId__get_next_id())
    strAddress: str
    geoLatitude: Decimal = None
    geoLongitude: Decimal = None
    strDistrict: str
    strCity: str
    strStreet: str = None
    strHouse: str = None
    strHouseSlash: str = None
    strCorps: str = None
    strBuilding: str = None
    strHolding: str = None
    strEntrance: str = None
    nFloor: int = None
    strRoom: str = None
    strEntranceCode: str = None
    strRoad: str = None
    nKm: int = None
    nM: int = None
    strAddressSection: str = None
    bNear: bool = None
    strPlace: str = None
    OKATO: str = None
    OKTMO: str = None
    strDistrictKLADR: str = None
    strCityKLADR: str = None  # require
    strStreetKLADR: str = None
    strDistrictFIAS: str = None
    strCityFIAS: str = None  # require
    strStreetFIAS: str = None
    strHouseFIAS: str = None
    orgOKPO: str = None


class Ukio(BaseModelWithId):
    globalId: str = Field(default_factory=lambda: f"{files_prefix}_{Ukio._BaseModelWithId__get_next_id()}")
    parentGlobalId: str = None
    strCardState: CardStates = None
    strIncidentType: IncidentTypes = None
    dtSend: datetime.datetime
    dtCreate: datetime.datetime = None
    dtUpdate: datetime.datetime = None
    dtCall: datetime.datetime = None
    dtCallEnd: datetime.datetime = None
    aCallEnded: bool = None
    nCasualties: int = None
    bHumanThreat: bool = False
    bChs: bool = False
    strCallSource: CallSource = None
    bWrong: bool
    bChildPlay: bool
    phoneCall: list[PhoneCall] = None
    PhoneCallID: list[str] = None
    bRelocated: bool = None
    strRegionTransfer: str = None
    callContent: CallContent = None
    address: Address = None
    era: Era = None
    sensorMessages: list[SensorMessage] = None
    sms: list[Sms] = None
    otherMessages: list[OtherMessage] = None
    psycho: Psycho = None
    consult: Consult = None
    transferItem: list[TransferItem] = None
    receptionItems: list[ReceptionItem] = None
    eosItem: list[EosItem] = None
    card01: Card01 = None
    card02: Card02 = None
    card03: Card03 = None
    card04: Card04 = None
    cardAT: CardAT = None
    cardCommServ: CardCommServ = None


class Ukios(BaseModel):
    Ukios: list[Ukio]
