"""
Конвертер из формата ЦССИ (Ukio) в формат ЦПГ (Card + Ier)
Использует таблицы соответствия полей для корректного маппинга
"""
import uuid
import random
from typing import Optional, Tuple
from datetime import datetime

# Флаг для копирования адреса из Card в IER
USE_CARD_ADDRESS_IN_IER = True

from schemas.ukio_model import Ukio, Address as UkioAddress, Era
from schemas.string_eos import Operator as UkioOperator
from schemas.cpg_models import (
    CPGCard, CPGIer, CPGOperator, CPGCoords, CPGAddress, CPGLocation,
    CPGCommonData, CPGDdsData01, CPGDdsData02, CPGDdsData03, CPGDdsData04,
    CPGDdsDataAT, CPGDdsDataCommServ, CPGFullName, CPGSmsIer, CPGEraCallCard,
    CPGEraLocation, CPGCrashType
)


def convert_ukio_to_cpg(ukio: Ukio) -> Tuple[Optional[CPGCard], Optional[CPGIer]]:
    """
    Главная функция конвертации Ukio в Card + Ier
    
    Args:
        ukio: Объект Ukio из системы ЦССИ
        
    Returns:
        Tuple[CPGCard, CPGIer]: Карточка и обращение в формате ЦПГ
    """
    if not ukio:
        return None, None
    
    print(f"DEBUG: Флаг USE_CARD_ADDRESS_IN_IER = {USE_CARD_ADDRESS_IN_IER}")
    
    card = _create_card_from_ukio(ukio)
    ier = _create_ier_from_ukio(ukio, card)
    
    return card, ier


def _create_card_from_ukio(ukio: Ukio) -> CPGCard:
    """Создание карточки CPGCard из Ukio"""
    
    # Извлекаем первого и последнего оператора
    first_operator = None
    last_operator = None
    
    if ukio.phoneCall and len(ukio.phoneCall) > 0:
        if hasattr(ukio.phoneCall[0], 'operator'):
            first_operator = ukio.phoneCall[0].operator
        if hasattr(ukio.phoneCall[-1], 'operator'):
            last_operator = ukio.phoneCall[-1].operator
    
    # Если операторов нет, создаем дефолтного
    if not first_operator:
        first_operator = _create_default_operator()
    if not last_operator:
        last_operator = first_operator
    
    card = CPGCard(
        Id112=ukio.globalId,
        ExtId=None,  # Должно быть пустое согласно таблице маппинга!
        Location=_map_location_from_address(ukio.address),
        CommonData=_extract_common_data(ukio),
        DdsData01=_convert_card01_to_dds(ukio.card01) if ukio.card01 else None,
        DdsData02=_convert_card02_to_dds(ukio.card02) if ukio.card02 else None,
        DdsData03=_convert_card03_to_dds(ukio.card03) if ukio.card03 else None,
        DdsData04=_convert_card04_to_dds(ukio.card04) if ukio.card04 else None,
        DdsDataAT=_convert_cardAT_to_dds(ukio.cardAT) if ukio.cardAT else None,
        DdsDataCommServ=_convert_cardCommServ_to_dds(ukio.cardCommServ) if ukio.cardCommServ else None,
        EraGlonassCardId=ukio.era.eraId if ukio.era else None,
        CreateOperator=_map_operator(first_operator),
        LastChangeOperator=_map_operator(last_operator),
        IncidentState=ukio.strCardState.value if ukio.strCardState else "new",
        Created=ukio.dtCreate.isoformat() + 'Z' if ukio.dtCreate else datetime.now().isoformat() + 'Z',
        Changed=ukio.dtUpdate.isoformat() + 'Z' if ukio.dtUpdate else datetime.now().isoformat() + 'Z'
    )
    
    return card


def _create_ier_from_ukio(ukio: Ukio, card: Optional[CPGCard] = None) -> CPGIer:
    """Создание обращения CPGIer из Ukio"""
    
    # Извлекаем оператора принявшего звонок
    accept_operator = None
    ier_time = datetime.now().isoformat() + 'Z'
    
    if ukio.phoneCall and len(ukio.phoneCall) > 0:
        first_call = ukio.phoneCall[0]
        if hasattr(first_call, 'operator'):
            accept_operator = first_call.operator
        if hasattr(first_call, 'dtCall'):
            ier_time = first_call.dtCall.isoformat() + 'Z'
    
    if not accept_operator:
        accept_operator = _create_default_operator()
    
    # Извлекаем номер телефона
    cg_pn = "112"
    if ukio.callContent and hasattr(ukio.callContent, 'strCgPN'):
        cg_pn = ukio.callContent.strCgPN or "112"
    
    # Определяем адрес для IER
    ier_location = None
    if USE_CARD_ADDRESS_IN_IER and card and card.Location:
        # Используем адрес из Card
        ier_location = card.Location
        print(f"DEBUG: IER использует адрес из Card: {card.Location.Address.City if card.Location.Address else 'N/A'}")
    else:
        # Используем адрес заявителя (старое поведение)
        if ukio.callContent and hasattr(ukio.callContent, 'appResAddress'):
            ier_location = _map_location_from_string(ukio.callContent.appResAddress)
            print(f"DEBUG: IER использует адрес заявителя: {ukio.callContent.appResAddress}")
        else:
            print("DEBUG: IER создается без адреса")
    
    ier = CPGIer(
        Id=f"IER_{uuid.uuid4().hex[:8].upper()}",
        IerIsoTime=ier_time,
        CgPn=cg_pn,
        CdPn=None,  # Номер телефона диспетчера - новое поле
        FullName=_extract_fullname(ukio.callContent) if ukio.callContent else None,
        AcceptOperator=_map_operator(accept_operator),
        Text=None,  # Нет соответствия - должно быть пустым!
        Era=_map_era(ukio.era) if ukio.era else None,
        Sms=_map_sms(ukio.sms[0]) if ukio.sms and len(ukio.sms) > 0 else None,
        IerType=1,  # Обязательное поле по WSDL! Константа = 1
        HrId=None,  # Нет соответствия согласно таблице маппинга!
        Birthdate=None,  # Новое поле - дата рождения заявителя
        Location=ier_location
    )
    
    return ier


def _map_location_from_address(address: Optional[UkioAddress]) -> CPGLocation:
    """Конвертация Address ЦССИ в Location ЦПГ"""
    if not address:
        return CPGLocation()
    
    cpg_address = CPGAddress(
        City=address.strCity,
        CityCode=address.strCityKLADR,
        CityFiasId=address.strCityFIAS,
        CityShort=None,  # Новое поле
        District=address.strDistrict,
        DistrictCode=address.strDistrictKLADR,
        DistrCenterCode=None,  # Новое поле
        Street=address.strStreet,
        StreetCode=address.strStreetKLADR,
        StreetFiasId=address.strStreetFIAS,
        StreetShort=None,  # Новое поле
        HouseNumber=address.strHouse,
        HouseType=None,  # Новое поле
        HouseCode=None,  # Новое поле
        HouseFiasId=address.strHouseFIAS,
        HouseFraction=address.strCorps,
        Building=address.strBuilding,
        BuildingType=None,  # Новое поле
        Ownership=address.strHolding,
        TargetArea=address.strAddressSection,
        TargetAreaStreet=None,  # Новое поле
        Road=address.strRoad,
        Clarification=None,  # Новое поле
        Porch=int(address.strEntrance) if address.strEntrance and address.strEntrance.isdigit() else None,
        Floor=address.nFloor,
        Flat=address.strRoom,
        IsNear=address.bNear,
        DistanceInKm=address.nKm,
        DistanceInM=address.nM,
        Code=address.strEntranceCode
    )
    
    cpg_coords = None
    if address.geoLatitude and address.geoLongitude:
        cpg_coords = CPGCoords(
            Latitude=str(address.geoLatitude),
            Longitude=str(address.geoLongitude)
        )
    
    return CPGLocation(Address=cpg_address, Coords=cpg_coords)


def _map_location_from_string(address_str: Optional[str]) -> Optional[CPGLocation]:
    """Создание Location из строки адреса"""
    if not address_str:
        return None
    
    return CPGLocation(
        Address=CPGAddress(
            City=address_str  # Упрощенно - весь адрес в поле City
        )
    )


def _extract_common_data(ukio: Ukio) -> CPGCommonData:
    """Извлечение CommonData из Ukio"""
    
    # Определяем тип происшествия
    incident_type = "Происшествие"
    if ukio.strIncidentType:
        incident_type = ukio.strIncidentType
    
    # Определяем время происшествия
    time_iso = datetime.now().isoformat() + 'Z'
    if ukio.dtCall:
        time_iso = ukio.dtCall.isoformat() + 'Z'
    
    # Извлекаем описание
    description = None
    if ukio.callContent and hasattr(ukio.callContent, 'strIncidentDescription'):
        description = ukio.callContent.strIncidentDescription
    
    return CPGCommonData(
        TypeStr=incident_type,
        RegionStr="Московская область",  # Обязательное поле по WSDL
        HrId=None,  # Нет соответствия согласно таблице маппинга!
        Description=description,
        LostNumber=None,  # Нет соответствия - должно быть пустым!
        InjuredNumber=ukio.nCasualties if ukio.nCasualties else 0,
        IsDanger=bool(ukio.bHumanThreat) if ukio.bHumanThreat is not None else None,
        IsBlocking=None,  # Нет соответствия - должно быть пустым!
        TimeIsoStr=time_iso,
        Level=int(ukio.bChs) if ukio.bChs is not None else None
    )


def _convert_card01_to_dds(card01) -> Optional[CPGDdsData01]:
    """Конвертация Card01 (пожарная служба) в DdsData01"""
    if not card01:
        return None
    
    return CPGDdsData01(
        DdsTypeStr=card01.strIncidentType if hasattr(card01, 'strIncidentType') else "Пожар",
        HasGas=card01.bObjectGasified if hasattr(card01, 'bObjectGasified') else False,
        NeedRescue=card01.bNeedRescueWork if hasattr(card01, 'bNeedRescueWork') else False,
        FloorCount=int(card01.strStoreys) if hasattr(card01, 'strStoreys') and card01.strStoreys and str(card01.strStoreys).isdigit() else None,
        FireTime=int(card01.strEstimation) if hasattr(card01, 'strEstimation') and card01.strEstimation and str(card01.strEstimation).isdigit() else None,
        FireEffects=card01.strObservedConsequencesFire if hasattr(card01, 'strObservedConsequencesFire') else None,
        DrivewaysState=card01.strCharacteristicsAccessRoads if hasattr(card01, 'strCharacteristicsAccessRoads') else None,
        WorkingConditions=card01.strCharacteristicsWorkingConditions if hasattr(card01, 'strCharacteristicsWorkingConditions') else None,
        EvacuationPossibility=card01.strEvacuationPossibilitiesAssessment if hasattr(card01, 'strEvacuationPossibilitiesAssessment') else None,
        OwnersAndTenantsInfo=card01.strObjectOwnerInfo if hasattr(card01, 'strObjectOwnerInfo') else None,
        LastChangeOperator01=None  # Оператор последнего изменения
    )


def _convert_card02_to_dds(card02) -> Optional[CPGDdsData02]:
    """Конвертация Card02 (полиция) в DdsData02"""
    if not card02:
        return None
    
    # Собираем описания подозреваемых и разыскиваемых
    suspect_desc = []
    if hasattr(card02, 'suspect') and card02.suspect:
        for suspect in card02.suspect:
            desc_parts = []
            if hasattr(suspect, 'strGender') and suspect.strGender:
                desc_parts.append(f"Пол: {suspect.strGender}")
            if hasattr(suspect, 'iAge') and suspect.iAge:
                desc_parts.append(f"Возраст: {suspect.iAge}")
            if hasattr(suspect, 'strDressed') and suspect.strDressed:
                desc_parts.append(f"Одежда: {suspect.strDressed}")
            if desc_parts:
                suspect_desc.append("; ".join(desc_parts))
    
    wanted_desc = []
    if hasattr(card02, 'wantedPerson') and card02.wantedPerson:
        for wanted in card02.wantedPerson:
            desc_parts = []
            if hasattr(wanted, 'strLastName') and wanted.strLastName:
                name_parts = [wanted.strLastName]
                if hasattr(wanted, 'strName') and wanted.strName:
                    name_parts.append(wanted.strName)
                if hasattr(wanted, 'strMiddleName') and wanted.strMiddleName:
                    name_parts.append(wanted.strMiddleName)
                desc_parts.append(" ".join(name_parts))
            if hasattr(wanted, 'iAge') and wanted.iAge:
                desc_parts.append(f"Возраст: {wanted.iAge}")
            if desc_parts:
                wanted_desc.append("; ".join(desc_parts))
    
    # Собираем описания транспорта
    vehicle_desc = []
    if hasattr(card02, 'vehicle') and card02.vehicle:
        for vehicle in card02.vehicle:
            desc_parts = []
            if hasattr(vehicle, 'strVehicleType') and vehicle.strVehicleType:
                desc_parts.append(f"Тип: {vehicle.strVehicleType}")
            if hasattr(vehicle, 'strColorVehicleType') and vehicle.strColorVehicleType:
                desc_parts.append(f"Цвет: {vehicle.strColorVehicleType}")
            if hasattr(vehicle, 'strRegistrationNumber') and vehicle.strRegistrationNumber:
                desc_parts.append(f"Номер: {vehicle.strRegistrationNumber}")
            if desc_parts:
                vehicle_desc.append("; ".join(desc_parts))
    
    return CPGDdsData02(
        DdsTypeStr=card02.strIncidentType if hasattr(card02, 'strIncidentType') else "Правонарушение",
        NumberOffenders=card02.iNumberOffenders if hasattr(card02, 'iNumberOffenders') else None,
        NumberVehicles=card02.iNumberVehicle if hasattr(card02, 'iNumberVehicle') else None,
        SuspectDescription=" | ".join(suspect_desc) if suspect_desc else None,
        WantedPersons=" | ".join(wanted_desc) if wanted_desc else None,
        VehicleDescription=" | ".join(vehicle_desc) if vehicle_desc else None,
        LastChangeOperator02=None
    )


def _convert_card03_to_dds(card03) -> Optional[CPGDdsData03]:
    """Конвертация Card03 (скорая помощь) в DdsData03"""
    if not card03:
        return None
    
    # Собираем информацию о пациентах
    patients_info = []
    if hasattr(card03, 'patient') and card03.patient:
        for patient in card03.patient:
            desc_parts = []
            if hasattr(patient, 'strLastName') and patient.strLastName:
                name_parts = [patient.strLastName]
                if hasattr(patient, 'strName') and patient.strName:
                    name_parts.append(patient.strName)
                if hasattr(patient, 'strMiddleName') and patient.strMiddleName:
                    name_parts.append(patient.strMiddleName)
                desc_parts.append(" ".join(name_parts))
            if hasattr(patient, 'iAge') and patient.iAge:
                desc_parts.append(f"Возраст: {patient.iAge}")
            if hasattr(patient, 'strGender') and patient.strGender:
                desc_parts.append(f"Пол: {patient.strGender}")
            if hasattr(patient, 'strOccasion') and patient.strOccasion:
                desc_parts.append(f"Повод: {patient.strOccasion}")
            if desc_parts:
                patients_info.append("; ".join(desc_parts))
    
    return CPGDdsData03(
        DdsTypeStr=card03.strIncidentType if hasattr(card03, 'strIncidentType') else "Медицинское происшествие",
        WhoCalled=card03.strWhoCalled if hasattr(card03, 'strWhoCalled') else None,
        IsConsultation=card03.bConsultation if hasattr(card03, 'bConsultation') else None,
        PatientsInfo=" | ".join(patients_info) if patients_info else None,
        SymptomsDescription=None,  # Можно добавить из strOccasion первого пациента
        UrgencyLevel=None,  # Может быть добавлено позже
        LastChangeOperator03=None
    )


def _convert_card04_to_dds(card04) -> Optional[CPGDdsData04]:
    """Конвертация Card04 (газовая служба) в DdsData04"""
    if not card04:
        return None
    
    return CPGDdsData04(
        DdsTypeStr=card04.strIncidentType if hasattr(card04, 'strIncidentType') else "Газовое происшествие",
        Instructions=card04.strInstructions if hasattr(card04, 'strInstructions') else None,
        IsConsultation=card04.bConsultation if hasattr(card04, 'bConsultation') else None,
        GasLeakLevel=None,  # Новое поле, может быть добавлено
        AffectedArea=None,  # Новое поле
        LastChangeOperator04=None
    )


def _convert_cardAT_to_dds(cardAT) -> Optional[CPGDdsDataAT]:
    """Конвертация CardAT (антитеррор) в DdsDataAT"""
    if not cardAT:
        return None
    
    # Собираем информацию о вооружении и транспорте
    armament_str = None
    if hasattr(cardAT, 'strArmament') and cardAT.strArmament:
        if isinstance(cardAT.strArmament, list):
            armament_str = " | ".join(cardAT.strArmament)
        else:
            armament_str = str(cardAT.strArmament)
    
    vehicle_str = None
    if hasattr(cardAT, 'strVehicle') and cardAT.strVehicle:
        if isinstance(cardAT.strVehicle, list):
            vehicle_str = " | ".join(cardAT.strVehicle)
        else:
            vehicle_str = str(cardAT.strVehicle)
    
    return CPGDdsDataAT(
        DdsTypeStr=cardAT.strIncidentType if hasattr(cardAT, 'strIncidentType') else "Антитеррористическое происшествие",
        PerishedPeople=cardAT.iPerishedPeople if hasattr(cardAT, 'iPerishedPeople') else None,
        AffectedPeople=cardAT.iAffectedPeople if hasattr(cardAT, 'iAffectedPeople') else None,
        SuspectPeople=cardAT.iSuspectPeople if hasattr(cardAT, 'iSuspectPeople') else None,
        SuspectDescription=cardAT.strSuspectDescription if hasattr(cardAT, 'strSuspectDescription') else None,
        Armament=armament_str,
        VehicleInfo=vehicle_str,
        Direction=cardAT.strDirection if hasattr(cardAT, 'strDirection') else None,
        InjurySuspect=cardAT.strInjurySuspect if hasattr(cardAT, 'strInjurySuspect') else None,
        ThreatLevel=None,  # Новое поле
        LastChangeOperatorAT=None
    )


def _convert_cardCommServ_to_dds(cardCommServ) -> Optional[CPGDdsDataCommServ]:
    """Конвертация CardCommServ (коммунальные службы) в DdsDataCommServ"""
    if not cardCommServ:
        return None
    
    # Собираем информацию о затронутых услугах
    services_str = None
    if hasattr(cardCommServ, 'strServiced') and cardCommServ.strServiced:
        if isinstance(cardCommServ.strServiced, list):
            services_str = " | ".join(cardCommServ.strServiced)
        else:
            services_str = str(cardCommServ.strServiced)
    
    return CPGDdsDataCommServ(
        DdsTypeStr=cardCommServ.strIncidentType if hasattr(cardCommServ, 'strIncidentType') else "Коммунальное происшествие",
        CommServType=cardCommServ.strCommServ if hasattr(cardCommServ, 'strCommServ') else None,
        Instructions=cardCommServ.strInstructions if hasattr(cardCommServ, 'strInstructions') else None,
        IsConsultation=cardCommServ.bConsultation if hasattr(cardCommServ, 'bConsultation') else None,
        ServicesAffected=services_str,
        Appeal=cardCommServ.strAppeal if hasattr(cardCommServ, 'strAppeal') else None,
        AffectedBuildings=None,  # Новое поле
        EstimatedRepairTime=None,  # Новое поле
        LastChangeOperatorCommServ=None
    )


def _map_operator(operator) -> CPGOperator:
    """Маппинг оператора из ЦССИ в ЦПГ"""
    if not operator:
        return _create_default_operator()
    
    # Составляем полное имя
    full_name = ""
    if hasattr(operator, 'strOperatorSurname'):
        full_name += str(operator.strOperatorSurname or "")
    if hasattr(operator, 'strOperatorName'):
        full_name += f" {operator.strOperatorName}" if full_name else str(operator.strOperatorName or "")
    if hasattr(operator, 'strOperatorLastName'):
        full_name += f" {operator.strOperatorLastName}" if full_name else str(operator.strOperatorLastName or "")
    
    return CPGOperator(
        OperatorLogin=operator.operatorId if hasattr(operator, 'operatorId') else "operator",
        OperatorPost=operator.strOperatorPost if hasattr(operator, 'strOperatorPost') else "Оператор 112",
        OperatorInfo=operator.strOperatorInfo if hasattr(operator, 'strOperatorInfo') else None,
        OperatorDN=None,  # Новое поле - телефонный номер
        OperatorWorkplace=None,  # Новое поле - номер АРМ
        OperatorName=full_name.strip() if full_name else None
    )


def _create_default_operator() -> CPGOperator:
    """Создание оператора по умолчанию"""
    return CPGOperator(
        OperatorLogin="system",
        OperatorPost="Оператор 112",
        OperatorInfo="Автоматически созданный оператор",
        OperatorName="Система"
    )


def _extract_fullname(call_content) -> Optional[CPGFullName]:
    """Извлечение ФИО из CallContent"""
    if not call_content:
        return None
    
    return CPGFullName(
        LastName=call_content.strLastName if hasattr(call_content, 'strLastName') else None,
        FirstName=call_content.strName if hasattr(call_content, 'strName') else None,
        MiddleName=call_content.strMiddleName if hasattr(call_content, 'strMiddleName') else None
    )


def _map_era(era: Optional[Era]) -> Optional[CPGEraCallCard]:
    """Маппинг ЭРА-ГЛОНАСС данных"""
    if not era:
        return None
    
    # Создаем информацию о столкновении
    crash_info = None
    if any([
        hasattr(era, 'bFrontCrash'),
        hasattr(era, 'bLeftCrash'),
        hasattr(era, 'bRightCrash'),
        hasattr(era, 'bSideCrash'),
        hasattr(era, 'bRearCrash'),
        hasattr(era, 'bRollover'),
        hasattr(era, 'bOtherCrashType')
    ]):
        crash_info = CPGCrashType(
            frontCrash=bool(era.bFrontCrash) if hasattr(era, 'bFrontCrash') else False,
            leftCrash=bool(era.bLeftCrash) if hasattr(era, 'bLeftCrash') else False,
            rightCrash=bool(era.bRightCrash) if hasattr(era, 'bRightCrash') else False,
            sideCrash=bool(era.bSideCrash) if hasattr(era, 'bSideCrash') else False,
            rearCrash=bool(era.bRearCrash) if hasattr(era, 'bRearCrash') else False,
            rollover=bool(era.bRollover) if hasattr(era, 'bRollover') else False,
            otherCrashType=bool(era.bOtherCrashType) if hasattr(era, 'bOtherCrashType') else False
        )
    
    # Создаем информацию о местоположении
    vehicle_location = None
    if hasattr(era, 'geoLatitude1') and hasattr(era, 'geoLongitude1'):
        vehicle_location = CPGEraLocation(
            latitude=float(era.geoLatitude1) if era.geoLatitude1 else None,
            longitude=float(era.geoLongitude1) if era.geoLongitude1 else None,
            positionCanBeTrusted=bool(era.bDataReliability) if hasattr(era, 'bDataReliability') else None,
            timestamp=era.dtGeo1Time if hasattr(era, 'dtGeo1Time') else None
        )
    
    return CPGEraCallCard(
        CardID=era.eraId if hasattr(era, 'eraId') else None,
        cardShortId=era.strCallShortId if hasattr(era, 'strCallShortId') else None,
        esgCardId=None,  # Новое поле
        terminalPhone=None,  # Новое поле
        declarantLanguageCode="ru",  # По умолчанию русский
        voiceChannelState="active" if hasattr(era, 'bVoiceCommTransport') and era.bVoiceCommTransport else "inactive",
        injuredPersons=era.nPassengers if hasattr(era, 'nPassengers') else None,
        driverPhone=None,  # Нет прямого маппинга
        driverFullName=None,  # Нет прямого маппинга
        automaticActivation=bool(era.bTriggeringType) if hasattr(era, 'bTriggeringType') else None,
        testCall=bool(era.bCallType) if hasattr(era, 'bCallType') else None,
        vehicleType=int(era.strVehicleType) if hasattr(era, 'strVehicleType') and str(era.strVehicleType).isdigit() else None,
        vehicleIdentificationNumber=era.strVIN if hasattr(era, 'strVIN') else None,
        vehiclePropulsionStorageType=int(era.iVehiclePropulsionStorageType) if hasattr(era, 'iVehiclePropulsionStorageType') else None,
        vehicleRegistryNumber=era.strRegistryNumber if hasattr(era, 'strRegistryNumber') else None,
        vehicleBodyColor=era.strVehicleBodyColor if hasattr(era, 'strVehicleBodyColor') else None,
        vehicleModel=era.strVehicleModel if hasattr(era, 'strVehicleModel') else None,
        callTimestamp=era.dtEra.timestamp() if hasattr(era, 'dtEra') and era.dtEra else None,
        vehicleLocation=vehicle_location,
        vehicleDirection=era.iDirection if hasattr(era, 'iDirection') else None,
        numberOfPassengers=era.nPassengers if hasattr(era, 'nPassengers') else None,
        severeCrashEstimate=None,  # Новое поле
        vehicleLocationDescription=None,  # Можно заполнить из адреса
        crashInfo=crash_info
    )


def _map_sms(sms) -> Optional[CPGSmsIer]:
    """Маппинг SMS сообщения"""
    if not sms:
        return None
    
    return CPGSmsIer(
        Text=sms.strSms if hasattr(sms, 'strSms') else None
    )