"""
Модели данных для системы ЦПГ (Центр Правительственной Связи)
Основано на cpg_wsdl_1.wsdl
"""
import random
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field


# ============== Базовые структуры ==============

class CPGOperator(BaseModel):
    """Оператор в системе ЦПГ"""
    OperatorLogin: str
    OperatorPost: Optional[str] = "Оператор 112"
    OperatorInfo: Optional[str] = None
    OperatorDN: Optional[str] = None
    OperatorWorkplace: Optional[str] = None
    OperatorName: Optional[str] = None


class CPGCoords(BaseModel):
    """Координаты"""
    Latitude: Optional[str] = None
    Longitude: Optional[str] = None


class CPGAddress(BaseModel):
    """Адрес в системе ЦПГ"""
    City: Optional[str] = None
    CityCode: Optional[str] = None
    CityFiasId: Optional[str] = None
    CityShort: Optional[str] = None
    District: Optional[str] = None
    DistrictCode: Optional[str] = None
    DistrCenterCode: Optional[str] = None
    Street: Optional[str] = None
    StreetCode: Optional[str] = None
    StreetFiasId: Optional[str] = None
    StreetShort: Optional[str] = None
    HouseNumber: Optional[str] = None
    HouseType: Optional[str] = None
    HouseCode: Optional[str] = None
    HouseFiasId: Optional[str] = None
    HouseFraction: Optional[str] = None
    Building: Optional[str] = None
    BuildingType: Optional[str] = None
    Ownership: Optional[str] = None
    TargetArea: Optional[str] = None
    TargetAreaStreet: Optional[str] = None
    Road: Optional[str] = None
    Clarification: Optional[str] = None
    Porch: Optional[int] = None
    Floor: Optional[int] = None
    Flat: Optional[str] = None
    IsNear: Optional[bool] = None
    DistanceInKm: Optional[int] = None
    DistanceInM: Optional[int] = None
    Code: Optional[str] = None


class CPGLocation(BaseModel):
    """Местоположение (адрес + координаты)"""
    Address: Optional[CPGAddress] = None
    Coords: Optional[CPGCoords] = None


# ============== Структуры карточки ==============

class CPGCommonData(BaseModel):
    """Общие данные карточки"""
    TypeStr: str  # Тип происшествия
    RegionStr: str = "Московская область"  # Обязательное поле по WSDL
    HrId: Optional[str] = None  # Нет соответствия - должно быть пустым!
    Description: Optional[str] = None
    LostNumber: Optional[int] = None  # Нет соответствия - должно быть пустым!
    InjuredNumber: Optional[int] = None  # Число пострадавших
    IsDanger: Optional[bool] = None  # Угроза людям
    IsBlocking: Optional[bool] = None  # Нет соответствия - должно быть пустым!
    TimeIsoStr: str  # Дата и время происшествия
    Level: Optional[int] = None  # Признак ЧС


class CPGDdsData01(BaseModel):
    """Данные службы 01 (пожарная)"""
    DdsTypeStr: str = "Пожар"  # Вид происшествия
    HasGas: bool = False  # Объект газифицирован
    NeedRescue: bool = False  # Необходимость спасательных работ
    FloorCount: Optional[int] = None  # Этажность
    FireTime: Optional[int] = None  # Оценка времени развития пожара
    FireEffects: Optional[str] = None  # Наблюдаемые последствия
    DrivewaysState: Optional[str] = None  # Характеристика подъездных путей
    WorkingConditions: Optional[str] = None  # Условия работы
    EvacuationPossibility: Optional[str] = None  # Оценка возможности эвакуации
    OwnersAndTenantsInfo: Optional[str] = None  # Информация о собственниках
    LastChangeOperator01: Optional[CPGOperator] = None


class CPGDdsData02(BaseModel):
    """Данные службы 02 (полиция)"""
    DdsTypeStr: str = "Правонарушение"  # Вид происшествия
    NumberOffenders: Optional[int] = None  # Количество правонарушителей
    NumberVehicles: Optional[int] = None  # Количество транспортных средств
    SuspectDescription: Optional[str] = None  # Описание подозреваемых
    WantedPersons: Optional[str] = None  # Информация о разыскиваемых
    VehicleDescription: Optional[str] = None  # Описание транспортных средств
    LastChangeOperator02: Optional[CPGOperator] = None


class CPGDdsData03(BaseModel):
    """Данные службы 03 (скорая помощь)"""
    DdsTypeStr: str = "Медицинское происшествие"  # Вид происшествия
    WhoCalled: Optional[str] = None  # Кто вызвал
    IsConsultation: Optional[bool] = None  # Консультация
    PatientsInfo: Optional[str] = None  # Информация о пациентах
    SymptomsDescription: Optional[str] = None  # Описание симптомов
    UrgencyLevel: Optional[str] = None  # Уровень срочности
    LastChangeOperator03: Optional[CPGOperator] = None


class CPGDdsData04(BaseModel):
    """Данные службы 04 (газовая служба)"""
    DdsTypeStr: str = "Газовое происшествие"  # Вид происшествия
    Instructions: Optional[str] = None  # Инструкции
    IsConsultation: Optional[bool] = None  # Консультация
    GasLeakLevel: Optional[str] = None  # Уровень утечки газа
    AffectedArea: Optional[str] = None  # Пострадавшая зона
    LastChangeOperator04: Optional[CPGOperator] = None


class CPGDdsDataAT(BaseModel):
    """Данные антитеррористической службы"""
    DdsTypeStr: str = "Антитеррористическое происшествие"  # Вид происшествия
    PerishedPeople: Optional[int] = None  # Количество погибших
    AffectedPeople: Optional[int] = None  # Количество пострадавших
    SuspectPeople: Optional[int] = None  # Количество подозреваемых
    SuspectDescription: Optional[str] = None  # Описание подозреваемых
    Armament: Optional[str] = None  # Вооружение
    VehicleInfo: Optional[str] = None  # Информация о транспорте
    Direction: Optional[str] = None  # Направление движения
    InjurySuspect: Optional[str] = None  # Ранения подозреваемых
    ThreatLevel: Optional[str] = None  # Уровень угрозы
    LastChangeOperatorAT: Optional[CPGOperator] = None


class CPGDdsDataCommServ(BaseModel):
    """Данные коммунальных служб"""
    DdsTypeStr: str = "Коммунальное происшествие"  # Вид происшествия
    CommServType: Optional[str] = None  # Тип коммунальной службы
    Instructions: Optional[str] = None  # Инструкции
    IsConsultation: Optional[bool] = None  # Консультация
    ServicesAffected: Optional[str] = None  # Затронутые услуги
    Appeal: Optional[str] = None  # Обращение
    AffectedBuildings: Optional[str] = None  # Пострадавшие здания
    EstimatedRepairTime: Optional[str] = None  # Ориентировочное время ремонта
    LastChangeOperatorCommServ: Optional[CPGOperator] = None


class CPGCard(BaseModel):
    """Основная карточка происшествия"""
    Id112: Optional[str] = None  # Идентификатор в системе 112
    ExtId: Optional[str] = None  # Пустое согласно таблице маппинга!
    Location: CPGLocation
    CommonData: CPGCommonData
    DdsData01: Optional[CPGDdsData01] = None  # Пожарная служба
    DdsData02: Optional[CPGDdsData02] = None  # Полиция  
    DdsData03: Optional[CPGDdsData03] = None  # Скорая помощь
    DdsData04: Optional[CPGDdsData04] = None  # Газовая служба
    DdsDataAT: Optional[CPGDdsDataAT] = None  # Антитеррор
    DdsDataCommServ: Optional[CPGDdsDataCommServ] = None  # Коммунальные службы
    EraGlonassCardId: Optional[str] = None
    CreateOperator: CPGOperator
    LastChangeOperator: CPGOperator
    IncidentState: str  # Состояние карточки
    Created: str  # Дата создания в ISO формате
    Changed: str  # Дата изменения в ISO формате


# ============== Структуры обращения (Ier) ==============

class CPGFullName(BaseModel):
    """ФИО заявителя"""
    LastName: Optional[str] = None
    FirstName: Optional[str] = None
    MiddleName: Optional[str] = None


class CPGSmsIer(BaseModel):
    """SMS сообщение"""
    Text: Optional[str] = None


class CPGCrashType(BaseModel):
    """Тип столкновения для ЭРА-ГЛОНАСС"""
    frontCrash: bool = False
    leftCrash: bool = False
    rightCrash: bool = False
    sideCrash: bool = False
    rearCrash: bool = False
    rollover: bool = False
    otherCrashType: bool = False


class CPGEraLocation(BaseModel):
    """Местоположение для ЭРА-ГЛОНАСС"""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    positionCanBeTrusted: Optional[bool] = None
    timestamp: Optional[datetime] = None
    timestampMillis: Optional[int] = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    latitudeMillis: Optional[int] = None
    longitudeMillis: Optional[int] = None


class CPGEraCallCard(BaseModel):
    """Карточка вызова ЭРА-ГЛОНАСС"""
    CardID: Optional[str] = None
    cardShortId: Optional[str] = None
    esgCardId: Optional[str] = None
    terminalPhone: Optional[str] = None
    declarantLanguageCode: Optional[str] = None
    voiceChannelState: Optional[str] = None
    injuredPersons: Optional[int] = None
    driverPhone: Optional[str] = None
    driverFullName: Optional[str] = None
    automaticActivation: Optional[bool] = None
    testCall: Optional[bool] = None
    vehicleType: Optional[int] = None
    vehicleIdentificationNumber: Optional[str] = None
    vehiclePropulsionStorageType: Optional[int] = None
    vehicleRegistryNumber: Optional[str] = None
    vehicleBodyColor: Optional[str] = None
    vehicleModel: Optional[str] = None
    callTimestamp: Optional[float] = None
    vehicleLocation: Optional[CPGEraLocation] = None
    vehicleDirection: Optional[int] = None
    numberOfPassengers: Optional[int] = None
    severeCrashEstimate: Optional[int] = None
    vehicleLocationDescription: Optional[str] = None
    crashInfo: Optional[CPGCrashType] = None
    callTimestampMillis: Optional[int] = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))


class CPGIer(BaseModel):
    """Информация об обращении"""
    Id: Optional[str] = Field(default_factory=lambda: f"IER_{uuid.uuid4().hex[:8].upper()}")
    IerIsoTime: str  # Дата и время приема обращения
    CgPn: str  # Номер абонентского устройства
    CdPn: Optional[str] = None  # Номер телефона диспетчера
    FullName: Optional[CPGFullName] = None
    AcceptOperator: CPGOperator
    Text: Optional[str] = None  # Дополнительная информация
    Era: Optional[CPGEraCallCard] = None
    Sms: Optional[CPGSmsIer] = None
    IerType: int = 1  # Обязательное поле по WSDL! Константа
    HrId: Optional[str] = None  # Нет соответствия - должно быть пустым!
    Birthdate: Optional[str] = None  # Дата рождения заявителя
    Location: Optional[CPGLocation] = None  # Адрес заявителя


# ============== Сообщения (операции) ==============

class UpdateCardRequest(BaseModel):
    """Запрос на создание/обновление карточки"""
    SysCode: str = "XML_GEN_112"  # Идентификатор системы-отправителя
    Card: Optional[CPGCard] = None
    Ier: Optional[CPGIer] = None


class UpdateCardResponse(BaseModel):
    """Ответ на запрос создания/обновления карточки"""
    Id112: str
    Code: str


class CancelCardRequest(BaseModel):
    """Запрос на отмену карточки"""
    SysCode: str = "XML_GEN_112"
    Id112: str
    Reason: str
    CancelOperator: CPGOperator
    ExtId: Optional[str] = None


class CancelCardResponse(BaseModel):
    """Ответ на запрос отмены карточки"""
    Code: str
    CodeDescr: Optional[str] = None


class AddReactionRequest(BaseModel):
    """Запрос на добавление реагирования"""
    SysCode: str = "XML_GEN_112"
    Id112: str
    UnitName: str  # Наименование единицы реагирования
    UnitMembership: Optional[str] = None  # Состав бригады
    ActionType: str  # Тип этапа реагирования
    Remark: Optional[str] = None  # Дополнительные данные
    ReactOperator: CPGOperator
    ActionTimeIsoStr: str  # Дата и время начала этапа
    DdsType: str  # Тип ДДС
    ExtId: Optional[str] = None


class AddReactionResponse(BaseModel):
    """Ответ на запрос добавления реагирования"""
    Code: str
    CodeDescr: Optional[str] = None


class FinishReactionRequest(BaseModel):
    """Запрос на завершение реагирования"""
    SysCode: str = "XML_GEN_112"
    Id112: str
    FinishOperator: CPGOperator
    DdsType: str
    ExtId: Optional[str] = None


class FinishReactionResponse(BaseModel):
    """Ответ на запрос завершения реагирования"""
    Code: str
    CodeDescr: Optional[str] = None


class CloseCardRequest(BaseModel):
    """Запрос на закрытие карточки"""
    SysCode: str = "XML_GEN_112"
    Id112: str
    CloseOperator: CPGOperator
    Reason: Optional[str] = None
    ExtId: Optional[str] = None


class CloseCardResponse(BaseModel):
    """Ответ на запрос закрытия карточки"""
    Code: str
    CodeDescr: Optional[str] = None