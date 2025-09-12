"""
Генерация примеров XML файлов для ЦССИ и ЦПГ с валидацией
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import fill_constants
fill_constants()

from datetime import datetime
import xml.etree.ElementTree as ET

def generate_cssi_example():
    """
    Генерация примера ЦССИ XML
    """
    print("\n=== ГЕНЕРАЦИЯ ПРИМЕРА ЦССИ ===")
    
    from schemas.ukio_model import Ukio, Address, CallContent, Ukios
    from schemas.phonecall import PhoneCall
    from schemas.string_eos import Operator
    from schemas.string_schemas import CardStates
    from schemas.eos_for_ukio_models import Card01
    from file_creator import create_file_from_model
    
    # Создаем оператора
    operator = Operator(
        operatorId="cssi_op_001",
        strOperatorSurname="Иванов",
        strOperatorName="Иван",
        strOperatorPost="Старший оператор 112"
    )
    
    # Создаем телефонный звонок
    phone_call = PhoneCall(
        phoneCallId="call_001",
        dtSend=datetime.now(),
        dtCall=datetime.now(),
        dtConnect=datetime.now(),
        dtEndCall=datetime.now(),
        operator=operator,
        bOperatorIniciatied=False,
        aCallEnded=True,
        strCallerAddress="г. Москва, ул. Тверская, д. 1"
    )
    
    # Создаем адрес
    address = Address(
        addressId="addr_001",
        strAddress="г. Москва, Красная площадь, д. 1",
        strCity="Москва",
        strCityKLADR="7700000000000",
        strCityFIAS="0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
        strDistrict="Центральный административный округ",
        strStreet="Красная площадь",
        strHouse="1",
        geoLatitude=55.753544,
        geoLongitude=37.620211
    )
    
    # Создаем контент звонка
    call_content = CallContent(
        callContentId="content_001",
        strLastName="Петров",
        strName="Петр",
        strMiddleName="Петрович",
        strCallerContactPhone="+79161234567",
        strCgPN="+79161234567",
        appResAddress="г. Москва, ул. Арбат, д. 10",
        strLanguage="ru",
        strIncidentDescription="Пожар на третьем этаже жилого дома",
        appLocAddress="г. Москва, Красная площадь, д. 1"
    )
    
    # Создаем Card01 (пожарная служба)
    card01 = Card01(
        card01Id="card01_001",
        dtCreate=datetime.now(),
        strIncidentType="Пожар в жилом доме",
        bObjectGasified=True,
        bNeedRescueWork=True,
        strStoreys="9",
        strEstimation="15",
        strObservedConsequencesFire="Сильное задымление, видно пламя",
        strCharacteristicsAccessRoads="Подъезд свободен",
        strCharacteristicsWorkingConditions="Сильное задымление",
        strEvacuationPossibilitiesAssessment="Эвакуация по лестничным клеткам",
        strObjectOwnerInfo="Многоквартирный жилой дом"
    )
    
    # Создаем Ukio
    ukio = Ukio(
        globalId="CSSI_EXAMPLE_001",
        strCardState=CardStates.status1,
        strIncidentType="Пожар",
        dtSend=datetime.now(),
        dtCreate=datetime.now(),
        dtUpdate=datetime.now(),
        dtCall=datetime.now(),
        dtCallEnd=datetime.now(),
        aCallEnded=True,
        nCasualties=2,
        bHumanThreat=1,
        bChs=0,
        strCallSource="Мобильный телефон",
        bWrong=False,
        bChildPlay=False,
        phoneCall=[phone_call],
        address=address,
        callContent=call_content,
        card01=card01
    )
    
    # Создаем файл
    ukios = Ukios(Ukios=[ukio])
    file_path = create_file_from_model(
        ukios,
        filename="example_cssi",
        basename="Ukios",
        region_name="examples"
    )
    
    print(f"✅ Файл создан: {file_path}")
    
    # Валидация структуры
    validate_cssi_structure(file_path)
    
    return file_path


def generate_cpg_example():
    """
    Генерация примера ЦПГ XML
    """
    print("\n=== ГЕНЕРАЦИЯ ПРИМЕРА ЦПГ ===")
    
    from schemas.cpg_models import (
        CPGCard, CPGIer, CPGOperator, CPGLocation, CPGAddress,
        CPGCoords, CPGCommonData, CPGDdsData01, CPGFullName
    )
    from file_creator_cpg import create_cpg_xml_file
    
    # Создаем оператора
    operator = CPGOperator(
        OperatorLogin="cpg_op_001",
        OperatorPost="Старший оператор",
        OperatorInfo="Опытный специалист",
        OperatorName="Иванов Иван Иванович"
    )
    
    # Создаем адрес
    address = CPGAddress(
        City="Москва",
        CityCode="7700000000000",
        CityFiasId="0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
        District="Центральный административный округ",
        Street="Красная площадь",
        HouseNumber="1",
        Floor=3,
        IsNear=False
    )
    
    # Создаем координаты
    coords = CPGCoords(
        Latitude="55.753544",
        Longitude="37.620211"
    )
    
    # Создаем локацию
    location = CPGLocation(
        Address=address,
        Coords=coords
    )
    
    # Создаем CommonData
    common_data = CPGCommonData(
        TypeStr="Пожар",
        RegionStr="г. Москва",
        HrId="INC-12345",
        Description="Пожар на третьем этаже жилого дома",
        LostNumber=0,
        InjuredNumber=2,
        IsDanger=True,
        IsBlocking=False,
        TimeIsoStr=datetime.now().isoformat(),
        Level=0
    )
    
    # Создаем DdsData01
    dds_data = CPGDdsData01(
        DdsTypeStr="Пожар в жилом доме",
        HasGas=True,
        NeedRescue=True,
        FloorCount=9,
        FireTime=15,
        FireEffects="Сильное задымление, видно пламя",
        DrivewaysState="Подъезд свободен",
        WorkingConditions="Сильное задымление",
        EvacuationPossibility="Эвакуация по лестничным клеткам",
        OwnersAndTenantsInfo="Многоквартирный жилой дом"
    )
    
    # Создаем Card
    card = CPGCard(
        Id112="CPG_EXAMPLE_001",
        ExtId="EXT_ABCD1234",
        Location=location,
        CommonData=common_data,
        DdsData01=dds_data,
        CreateOperator=operator,
        LastChangeOperator=operator,
        IncidentState="new",
        Created=datetime.now().isoformat(),
        Changed=datetime.now().isoformat()
    )
    
    # Создаем FullName
    full_name = CPGFullName(
        LastName="Петров",
        FirstName="Петр",
        MiddleName="Петрович"
    )
    
    # Создаем Ier
    ier = CPGIer(
        Id="IER_EXAMPLE_001",
        IerIsoTime=datetime.now().isoformat(),
        CgPn="+79161234567",
        FullName=full_name,
        AcceptOperator=operator,
        Text="Срочно! Пожар на третьем этаже, есть пострадавшие",
        IerType=1,
        HrId="IER-12345",
        Location=CPGLocation(
            Address=CPGAddress(
                City="Москва",
                Street="Арбат",
                HouseNumber="10"
            )
        )
    )
    
    # Создаем файл
    file_path = create_cpg_xml_file(
        card=card,
        ier=ier,
        filename="example_cpg",
        region_name="examples"
    )
    
    print(f"✅ Файл создан: {file_path}")
    
    # Валидация структуры
    validate_cpg_structure(file_path)
    
    return file_path


def validate_cssi_structure(file_path):
    """
    Валидация структуры ЦССИ XML
    """
    print("\n📋 Валидация ЦССИ структуры:")
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Проверка namespace
        if "s112" in root.tag:
            print("  ✅ Namespace s112 присутствует")
        else:
            print(f"  ❌ Неверный namespace: {root.tag}")
        
        # Проверка обязательных полей
        checks = {
            ".//globalId": "globalId (идентификатор)",
            ".//strCallSource": "strCallSource (источник вызова)",
            ".//bWrong": "bWrong (ложный вызов)",
            ".//bChildPlay": "bChildPlay (детская шалость)",
            ".//phoneCall": "phoneCall (телефонный звонок)",
            ".//address": "address (адрес)",
            ".//card01": "card01 (карточка пожарной службы)"
        }
        
        for xpath, description in checks.items():
            element = root.find(xpath)
            if element is not None:
                value = element.text if element.text else "(объект)"
                print(f"  ✅ {description}: найден")
            else:
                print(f"  ❌ {description}: отсутствует")
                
    except Exception as e:
        print(f"  ❌ Ошибка валидации: {e}")


def validate_cpg_structure(file_path):
    """
    Валидация структуры ЦПГ XML
    """
    print("\n📋 Валидация ЦПГ структуры:")
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        ns = {"tns": "http://tspg.service/"}
        
        # Проверка namespace и корневого элемента
        if "UpdateCardRequest" in root.tag:
            print("  ✅ Корневой элемент UpdateCardRequest")
        else:
            print(f"  ❌ Неверный корневой элемент: {root.tag}")
        
        # Проверка обязательных элементов
        checks = {
            "tns:SysCode": "SysCode (идентификатор системы)",
            "tns:Card": "Card (карточка)",
            "tns:Ier": "Ier (обращение)",
            ".//tns:Id112": "Id112 (идентификатор)",
            ".//tns:Location": "Location (местоположение)",
            ".//tns:CommonData": "CommonData (общие данные)",
            ".//tns:DdsData01": "DdsData01 (данные службы 01)",
            ".//tns:IerIsoTime": "IerIsoTime (время обращения)",
            ".//tns:CgPn": "CgPn (номер звонящего)"
        }
        
        for xpath, description in checks.items():
            element = root.find(xpath, ns)
            if element is not None:
                print(f"  ✅ {description}: найден")
            else:
                print(f"  ❌ {description}: отсутствует")
                
    except Exception as e:
        print(f"  ❌ Ошибка валидации: {e}")


def compare_files(cssi_path, cpg_path):
    """
    Сравнение размеров и структуры файлов
    """
    print("\n=== СРАВНЕНИЕ ФАЙЛОВ ===")
    
    # Размеры файлов
    cssi_size = os.path.getsize(cssi_path)
    cpg_size = os.path.getsize(cpg_path)
    
    print(f"\n📊 Размеры файлов:")
    print(f"  ЦССИ: {cssi_size} байт")
    print(f"  ЦПГ: {cpg_size} байт")
    print(f"  Разница: {abs(cssi_size - cpg_size)} байт ({round(abs(cssi_size - cpg_size) / cssi_size * 100, 1)}%)")
    
    # Количество элементов
    cssi_tree = ET.parse(cssi_path)
    cpg_tree = ET.parse(cpg_path)
    
    cssi_elements = len(cssi_tree.getroot().findall(".//*"))
    cpg_elements = len(cpg_tree.getroot().findall(".//*"))
    
    print(f"\n📊 Количество элементов:")
    print(f"  ЦССИ: {cssi_elements} элементов")
    print(f"  ЦПГ: {cpg_elements} элементов")
    
    # Читаем первые строки для визуального сравнения
    print("\n📄 Первые строки ЦССИ:")
    with open(cssi_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < 5:
                print(f"  {line.rstrip()}")
            else:
                break
    
    print("\n📄 Первые строки ЦПГ:")
    with open(cpg_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < 5:
                print(f"  {line.rstrip()}")
            else:
                break


if __name__ == "__main__":
    print("\n" + "="*80)
    print("ГЕНЕРАЦИЯ И ВАЛИДАЦИЯ ПРИМЕРОВ XML")
    print("="*80)
    
    # Генерация примеров
    cssi_file = generate_cssi_example()
    cpg_file = generate_cpg_example()
    
    # Сравнение файлов
    if cssi_file and cpg_file:
        compare_files(cssi_file, cpg_file)
    
    print("\n" + "="*80)
    print("ГЕНЕРАЦИЯ ЗАВЕРШЕНА")
    print("="*80)
    
    print(f"\n📁 Файлы сохранены в:")
    print(f"  ЦССИ: {cssi_file}")
    print(f"  ЦПГ: {cpg_file}")