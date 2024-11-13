import datetime

from pydantic import Field
from schemas import BaseModelWithId


class Card01(BaseModelWithId):
    card01Id: str = Field(default_factory=lambda: Card01._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime = None
    strIncidentType: str = None
    strObject: str = None
    strStoreys: str = None
    bObjectGasified: bool = None
    strEstimation: str = None
    strObservedConsequencesFire: str = None
    strCharacteristicsAccessRoads: str = None
    strCharacteristicsWorkingConditions: str = None
    bNeedRescueWork: bool = None
    strEvacuationPossibilitiesAssessment: str = None
    strObjectOwnerInfo: str = None


class WantedPerson(BaseModelWithId):
    wantedId: str = Field(default_factory=lambda: WantedPerson._BaseModelWithId__get_next_id())
    strGender: str = None
    iAge: int = None
    strHeightType: str = None
    strBodyType: str = None
    strDressed: str = None
    strSpecialSigns: str = None
    strLastName: str = None
    strName: str = None
    strMiddleName: str = None
    dtDateBirth: datetime.datetime = None


class Suspect(BaseModelWithId):
    suspectId: str = Field(default_factory=lambda: Suspect._BaseModelWithId__get_next_id())
    strGender: str = None
    iAge: int = None
    strHeightType: str = None
    strBodyType: str = None
    strDressed: str = None
    strSpecialSigns: str = None


class Vehicle(BaseModelWithId):
    vehicleId: str = Field(default_factory=lambda: Vehicle._BaseModelWithId__get_next_id())
    strVehicleType: str = None
    strColorVehicleType: str = None
    strRegistrationNumber: str = None
    strRegion: str = None
    bHidden: bool = None


class Card02(BaseModelWithId):
    card02Id: str = Field(default_factory=lambda: Card02._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime = None
    strIncidentType: str = None
    iNumberOffenders: int = None
    iNumberVehicle: int = None
    suspect: list[Suspect] = None
    wantedPerson: list[WantedPerson] = None
    vehicle: list[Vehicle] = None


class Patient(BaseModelWithId):
    patientId: str = Field(default_factory=lambda: Patient._BaseModelWithId__get_next_id())
    strLastName: str = None
    strName: str = None
    strMiddleName: str = None
    dtDateBirth: datetime.datetime = None
    iAge: int = None
    strGender: str = None
    strOccasion: str = None
    strAbilityMoveIndependently: str = None


class Card03(BaseModelWithId):
    card03Id: str = Field(default_factory=lambda: Card03._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime = None
    strIncidentType: str = None
    strWhoCalled: str = None
    bConsultation: bool = None
    patient: list[Patient] = None


class Card04(BaseModelWithId):
    card04Id: str = Field(default_factory=lambda: Card04._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime = None
    strIncidentType: str = None
    strInstructions: str = None
    bConsultation: bool = None


class CardCommServ(BaseModelWithId):
    cardCommServId: str = Field(default_factory=lambda: CardCommServ._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime = None
    strIncidentType: str = None
    strCommServ: str = None
    strInstructions: str = None
    bConsultation: bool = None
    strServiced: list[str] = None
    strAppeal: str = None


class CardAT(BaseModelWithId):
    cardATId: str = Field(default_factory=lambda: CardAT._BaseModelWithId__get_next_id())
    dtCreate: datetime.datetime = None
    strIncidentType: str = None
    iPerishedPeople: int = None
    iAffectedPeople: int = None
    iSuspectPeople: int = None
    strSuspectDescription: str = None
    strArmament: list[str] = None
    strVehicles: list[str] = None
    strDirection: str = None
    strInjurySuspect: str = None
