#!/usr/bin/env python3
"""
Тест всех служб экстренного реагирования в ЦПГ
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import fill_constants
fill_constants()

from datetime import datetime
from schemas.ukio_model import Ukio
from schemas.eos_for_ukio_models import Card01, Card02, Card03, Card04, CardAT, CardCommServ, Patient, Suspect, Vehicle, WantedPerson
from schemas.string_schemas import CardStates
from converters.ukio_to_cpg import convert_ukio_to_cpg

def create_test_ukio_with_all_services():
    """
    Создаем тестовый UKIO со всеми службами экстренного реагирования
    """
    # Card01 - Пожарная служба
    card01 = Card01(
        card01Id="test_card01",
        dtCreate=datetime.now(),
        strIncidentType="Пожар в жилом доме",
        strStoreys="9",
        bObjectGasified=True,
        strEstimation="15",
        strObservedConsequencesFire="Сильное задымление",
        strCharacteristicsAccessRoads="Подъезд свободен",
        strCharacteristicsWorkingConditions="Задымление",
        bNeedRescueWork=True,
        strEvacuationPossibilitiesAssessment="Эвакуация возможна",
        strObjectOwnerInfo="Многоквартирный дом"
    )
    
    # Card02 - Полиция
    suspect = Suspect(
        suspectId="suspect1",
        strGender="М",
        iAge=25,
        strHeightType="средний",
        strBodyType="средний",
        strDressed="темная куртка",
        strSpecialSigns="шрам на лице"
    )
    
    wanted_person = WantedPerson(
        wantedId="wanted1",
        strLastName="Иванов",
        strName="Иван",
        strMiddleName="Иванович",
        strGender="М",
        iAge=30
    )
    
    vehicle = Vehicle(
        vehicleId="vehicle1",
        strVehicleType="легковой автомобиль",
        strColorVehicleType="синий",
        strRegistrationNumber="А123БВ777",
        strRegion="Москва"
    )
    
    card02 = Card02(
        card02Id="test_card02",
        dtCreate=datetime.now(),
        strIncidentType="Кража",
        iNumberOffenders=2,
        iNumberVehicle=1,
        suspect=[suspect],
        wantedPerson=[wanted_person],
        vehicle=[vehicle]
    )
    
    # Card03 - Скорая помощь  
    patient = Patient(
        patientId="patient1",
        strLastName="Петров",
        strName="Петр",
        strMiddleName="Петрович",
        iAge=45,
        strGender="М",
        strOccasion="Боль в груди",
        strAbilityMoveIndependently="не может"
    )
    
    card03 = Card03(
        card03Id="test_card03",
        dtCreate=datetime.now(),
        strIncidentType="Сердечный приступ",
        strWhoCalled="жена пациента",
        bConsultation=False,
        patient=[patient]
    )
    
    # Card04 - Газовая служба
    card04 = Card04(
        card04Id="test_card04",
        dtCreate=datetime.now(),
        strIncidentType="Утечка газа",
        strInstructions="Перекрыть газ, проветрить помещение",
        bConsultation=True
    )
    
    # CardAT - Антитеррор
    cardAT = CardAT(
        cardATId="test_cardAT",
        dtCreate=datetime.now(),
        strIncidentType="Подозрительный предмет",
        iPerishedPeople=0,
        iAffectedPeople=0,
        iSuspectPeople=1,
        strSuspectDescription="неизвестный в маске",
        strArmament=["нож"],
        strVehicle=["черная машина"],
        strDirection="в сторону центра",
        strInjurySuspect="без ранений"
    )
    
    # CardCommServ - Коммунальные службы
    cardCommServ = CardCommServ(
        cardCommServId="test_cardCommServ",
        dtCreate=datetime.now(),
        strIncidentType="Отключение электричества",
        strCommServ="энергетики",
        strInstructions="проверить трансформатор",
        bConsultation=False,
        strServiced=["электричество", "лифт"],
        strAppeal="жители дома жалуются на отключение"
    )
    
    # Основной UKIO
    ukio = Ukio(
        globalId="TEST_ALL_SERVICES_001",
        strCardState=CardStates.status1,
        strIncidentType="Комплексное происшествие",
        dtSend=datetime.now(),
        dtCreate=datetime.now(),
        dtUpdate=datetime.now(),
        dtCall=datetime.now(),
        dtCallEnd=datetime.now(),
        aCallEnded=True,
        nCasualties=1,
        bHumanThreat=1,
        bChs=0,
        strCallSource="Телефон",
        bWrong=False,
        bChildPlay=False,
        card01=card01,
        card02=card02,
        card03=card03,
        card04=card04,
        cardAT=cardAT,
        cardCommServ=cardCommServ
    )
    
    return ukio

def test_conversion():
    """
    Тестирование конвертации всех служб
    """
    print("=" * 80)
    print("ТЕСТ КОНВЕРТАЦИИ ВСЕХ СЛУЖБ ЭКСТРЕННОГО РЕАГИРОВАНИЯ")
    print("=" * 80)
    
    # Создаем тестовые данные
    print("\n1. Создание тестового UKIO...")
    ukio = create_test_ukio_with_all_services()
    print(f"   ✅ UKIO создан с ID: {ukio.globalId}")
    
    # Конвертируем
    print("\n2. Конвертация UKIO → CPG...")
    try:
        card, ier = convert_ukio_to_cpg(ukio)
        print(f"   ✅ Конвертация успешна")
        print(f"      - Card.Id112 = {card.Id112}")
        print(f"      - Card.ExtId = {card.ExtId}")
        
    except Exception as e:
        print(f"   ❌ Ошибка конвертации: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Проверяем все службы
    print("\n3. Проверка конвертации служб:")
    
    services = [
        ("DdsData01 (Пожарная)", card.DdsData01),
        ("DdsData02 (Полиция)", card.DdsData02), 
        ("DdsData03 (Скорая)", card.DdsData03),
        ("DdsData04 (Газовая)", card.DdsData04),
        ("DdsDataAT (Антитеррор)", card.DdsDataAT),
        ("DdsDataCommServ (Коммунальные)", card.DdsDataCommServ)
    ]
    
    for service_name, service_data in services:
        if service_data:
            print(f"   ✅ {service_name}:")
            print(f"      - Тип: {service_data.DdsTypeStr}")
            
            # Специфичные проверки по службам
            if hasattr(service_data, 'HasGas'):  # DdsData01
                print(f"      - Газифицирован: {service_data.HasGas}")
                print(f"      - Этажность: {service_data.FloorCount}")
            
            elif hasattr(service_data, 'NumberOffenders'):  # DdsData02
                print(f"      - Количество правонарушителей: {service_data.NumberOffenders}")
                print(f"      - Описание подозреваемых: {service_data.SuspectDescription}")
            
            elif hasattr(service_data, 'WhoCalled'):  # DdsData03
                print(f"      - Кто вызвал: {service_data.WhoCalled}")
                print(f"      - Информация о пациентах: {service_data.PatientsInfo}")
            
            elif hasattr(service_data, 'Instructions') and hasattr(service_data, 'GasLeakLevel'):  # DdsData04
                print(f"      - Инструкции: {service_data.Instructions}")
                print(f"      - Консультация: {service_data.IsConsultation}")
            
            elif hasattr(service_data, 'PerishedPeople'):  # DdsDataAT
                print(f"      - Пострадавшие: {service_data.AffectedPeople}")
                print(f"      - Подозреваемые: {service_data.SuspectPeople}")
                print(f"      - Вооружение: {service_data.Armament}")
            
            elif hasattr(service_data, 'CommServType'):  # DdsDataCommServ
                print(f"      - Тип службы: {service_data.CommServType}")
                print(f"      - Затронутые услуги: {service_data.ServicesAffected}")
                print(f"      - Обращение: {service_data.Appeal}")
        else:
            print(f"   ❌ {service_name}: не конвертирован")
    
    # Проверка Ier
    print(f"\n4. Информация об обращении (Ier):")
    print(f"   ✅ Ier.Id = {ier.Id}")
    print(f"   ✅ Ier.IerType = {ier.IerType}")
    print(f"   ✅ Ier.HrId = {ier.HrId}")
    
    print("\n" + "=" * 80)
    print("ТЕСТ ЗАВЕРШЕН УСПЕШНО")
    print("=" * 80)
    
    return True

def test_xml_generation():
    """
    Тест генерации XML с всеми службами
    """
    print("\n5. Тест генерации XML...")
    
    try:
        from file_creator_cpg import create_cpg_xml_file
        
        ukio = create_test_ukio_with_all_services()
        card, ier = convert_ukio_to_cpg(ukio)
        
        file_path = create_cpg_xml_file(
            card=card,
            ier=ier,
            filename="test_all_services",
            region_name="test_multi_services"
        )
        
        print(f"   ✅ XML файл создан: {file_path}")
        
        # Проверяем содержимое
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        # Подсчитываем службы в XML
        services_in_xml = []
        if "<tns:DdsData01>" in xml_content:
            services_in_xml.append("DdsData01")
        if "<tns:DdsData02>" in xml_content:
            services_in_xml.append("DdsData02") 
        if "<tns:DdsData03>" in xml_content:
            services_in_xml.append("DdsData03")
        if "<tns:DdsData04>" in xml_content:
            services_in_xml.append("DdsData04")
        if "<tns:DdsDataAT>" in xml_content:
            services_in_xml.append("DdsDataAT")
        if "<tns:DdsDataCommServ>" in xml_content:
            services_in_xml.append("DdsDataCommServ")
        
        print(f"   ✅ Службы в XML: {', '.join(services_in_xml)} ({len(services_in_xml)} из 6)")
        
        if len(services_in_xml) == 6:
            print("   🎉 ВСЕ 6 СЛУЖБ УСПЕШНО ДОБАВЛЕНЫ В XML!")
        else:
            print(f"   ⚠️ Не все службы попали в XML")
        
        return file_path
        
    except Exception as e:
        print(f"   ❌ Ошибка генерации XML: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    success = test_conversion()
    if success:
        test_xml_generation()