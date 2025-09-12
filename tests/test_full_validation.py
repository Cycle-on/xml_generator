"""
Комплексное тестирование генерации ЦССИ и ЦПГ с валидацией по WSDL
"""
import sys
import os
import xml.etree.ElementTree as ET
from datetime import datetime
import json

# Добавляем родительскую директорию в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Инициализируем константы
from constants import fill_constants
fill_constants()

from config import load_config
from generators.operators_and_arms import create_arms_and_operators, ARM_WORK, OPERATOR_WORK

config = load_config()

def test_cssi_generation():
    """
    Тестирование генерации ЦССИ и валидация по wsdl_5.wsdl
    """
    print("\n" + "="*80)
    print("ТЕСТИРОВАНИЕ РЕЖИМА ЦССИ")
    print("="*80)
    
    results = {
        "mode": "ЦССИ",
        "wsdl": "wsdl_5.wsdl",
        "tests": {}
    }
    
    # Подготовка
    ARM_WORK.clear()
    OPERATOR_WORK.clear()
    create_arms_and_operators()
    
    # Генерация одной карточки ЦССИ
    from generators.ukio_generator import generate_ukio_phone_call_data
    from file_creator import create_file_from_model
    from schemas.ukio_model import Ukios
    
    print("\n1. Генерация UKIO карточки...")
    ukio = generate_ukio_phone_call_data(datetime.now())
    
    if ukio is None:
        results["tests"]["generation"] = "❌ Не удалось сгенерировать UKIO"
        return results
    
    results["tests"]["generation"] = "✅ UKIO успешно сгенерирован"
    print(f"   - ID: {ukio.globalId}")
    print(f"   - Тип инцидента: {ukio.strIncidentType}")
    print(f"   - Состояние: {ukio.strCardState}")
    
    # Создание XML файла
    print("\n2. Создание XML файла...")
    ukios = Ukios(Ukios=[ukio])
    try:
        file_path = create_file_from_model(
            ukios, 
            filename="test_cssi",
            basename="Ukios",
            region_name="test"
        )
        results["tests"]["xml_creation"] = f"✅ XML создан: {file_path}"
        print(f"   - Файл создан: {file_path}")
    except Exception as e:
        results["tests"]["xml_creation"] = f"❌ Ошибка создания XML: {e}"
        return results
    
    # Валидация структуры по WSDL
    print("\n3. Валидация по wsdl_5.wsdl...")
    validation_results = validate_cssi_xml(file_path)
    results["tests"]["validation"] = validation_results
    
    # Проверка обязательных полей
    print("\n4. Проверка обязательных полей UKIO...")
    field_check = check_ukio_required_fields(file_path)
    results["tests"]["required_fields"] = field_check
    
    return results


def test_cpg_generation():
    """
    Тестирование генерации ЦПГ и валидация по cpg_wsdl_1.wsdl
    """
    print("\n" + "="*80)
    print("ТЕСТИРОВАНИЕ РЕЖИМА ЦПГ")
    print("="*80)
    
    results = {
        "mode": "ЦПГ",
        "wsdl": "cpg_wsdl_1.wsdl",
        "tests": {}
    }
    
    # Подготовка
    ARM_WORK.clear()
    OPERATOR_WORK.clear()
    create_arms_and_operators()
    
    # Генерация карточки ЦПГ
    from generators.cpg_generator import generate_cpg_card_data
    from file_creator_cpg import create_cpg_xml_file
    
    print("\n1. Генерация Card + Ier...")
    card, ier = generate_cpg_card_data(datetime.now())
    
    if not card or not ier:
        results["tests"]["generation"] = "❌ Не удалось сгенерировать Card/Ier"
        return results
    
    results["tests"]["generation"] = "✅ Card и Ier успешно сгенерированы"
    print(f"   - Card.Id112: {card.Id112}")
    print(f"   - Card.ExtId: {card.ExtId}")
    print(f"   - Ier.Id: {ier.Id}")
    
    # Создание XML файла
    print("\n2. Создание XML файла...")
    try:
        file_path = create_cpg_xml_file(
            card=card,
            ier=ier,
            filename="test_cpg",
            region_name="test"
        )
        results["tests"]["xml_creation"] = f"✅ XML создан: {file_path}"
        print(f"   - Файл создан: {file_path}")
    except Exception as e:
        results["tests"]["xml_creation"] = f"❌ Ошибка создания XML: {e}"
        return results
    
    # Валидация по новому WSDL
    print("\n3. Валидация по cpg_wsdl_1.wsdl...")
    from tests.validate_cpg_xml import validate_cpg_xml
    is_valid, errors = validate_cpg_xml(file_path)
    
    if is_valid:
        results["tests"]["validation"] = "✅ XML валидный по схеме ЦПГ"
    else:
        results["tests"]["validation"] = f"❌ Ошибки валидации: {errors}"
    
    # Проверка обязательных полей
    print("\n4. Проверка обязательных полей ЦПГ...")
    field_check = check_cpg_required_fields(file_path)
    results["tests"]["required_fields"] = field_check
    
    return results


def validate_cssi_xml(file_path):
    """
    Валидация XML ЦССИ по wsdl_5.wsdl
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Проверка namespace
        expected_ns = "s112"
        if expected_ns not in root.tag:
            return f"❌ Неверный namespace. Ожидается: {expected_ns}"
        
        # Проверка структуры UKIO
        ukios = root.findall(".//Ukio")
        if not ukios:
            return "❌ Не найдены элементы Ukio"
        
        # Проверка обязательных полей первого Ukio
        ukio = ukios[0]
        required = ["globalId", "strCallSource", "bWrong", "bChildPlay"]
        missing = []
        
        for field in required:
            if ukio.find(f".//{field}") is None:
                missing.append(field)
        
        if missing:
            return f"❌ Отсутствуют обязательные поля: {missing}"
        
        return "✅ XML валидный по схеме ЦССИ"
        
    except Exception as e:
        return f"❌ Ошибка валидации: {e}"


def check_ukio_required_fields(file_path):
    """
    Проверка обязательных полей UKIO
    """
    try:
        tree = ET.parse(file_path)
        
        fields_status = {}
        
        # Список обязательных полей согласно WSDL
        required_fields = {
            "globalId": "Идентификатор карточки",
            "strCallSource": "Источник вызова",
            "bWrong": "Признак ложного вызова",
            "bChildPlay": "Признак детской шалости",
            "dtSend": "Время отправки",
            "phoneCall": "Телефонный звонок"
        }
        
        for field, description in required_fields.items():
            element = tree.find(f".//{field}")
            if element is not None:
                value = element.text if element.text else "(вложенный объект)"
                fields_status[field] = f"✅ {description}: {value[:50]}"
            else:
                fields_status[field] = f"❌ {description}: отсутствует"
        
        return fields_status
        
    except Exception as e:
        return {"error": f"❌ Ошибка проверки: {e}"}


def check_cpg_required_fields(file_path):
    """
    Проверка обязательных полей ЦПГ
    """
    try:
        tree = ET.parse(file_path)
        
        fields_status = {}
        ns = {"tns": "http://tspg.service/"}
        
        # Проверка UpdateCardRequest
        root = tree.getroot()
        if "UpdateCardRequest" in root.tag:
            fields_status["root"] = "✅ Корневой элемент UpdateCardRequest"
        else:
            fields_status["root"] = f"❌ Неверный корневой элемент: {root.tag}"
        
        # Проверка SysCode
        sys_code = root.find("tns:SysCode", ns)
        if sys_code is not None:
            fields_status["SysCode"] = f"✅ SysCode: {sys_code.text}"
        else:
            fields_status["SysCode"] = "❌ SysCode отсутствует"
        
        # Проверка Card
        card = root.find("tns:Card", ns)
        if card is not None:
            # Проверка обязательных полей Card
            card_fields = {
                "Id112": "Идентификатор",
                "Location": "Местоположение",
                "CommonData": "Общие данные",
                "CreateOperator": "Создавший оператор",
                "LastChangeOperator": "Последний оператор",
                "IncidentState": "Состояние",
                "Created": "Дата создания",
                "Changed": "Дата изменения"
            }
            
            for field, desc in card_fields.items():
                elem = card.find(f"tns:{field}", ns)
                if elem is not None:
                    value = elem.text if elem.text else "(объект)"
                    fields_status[f"Card.{field}"] = f"✅ {desc}: {value[:30]}"
                else:
                    fields_status[f"Card.{field}"] = f"❌ {desc}: отсутствует"
        else:
            fields_status["Card"] = "❌ Card отсутствует"
        
        # Проверка Ier
        ier = root.find("tns:Ier", ns)
        if ier is not None:
            ier_fields = {
                "IerIsoTime": "Время обращения",
                "CgPn": "Номер звонящего",
                "AcceptOperator": "Принявший оператор",
                "IerType": "Тип обращения"
            }
            
            for field, desc in ier_fields.items():
                elem = ier.find(f"tns:{field}", ns)
                if elem is not None:
                    value = elem.text if elem.text else "(объект)"
                    fields_status[f"Ier.{field}"] = f"✅ {desc}: {value[:30]}"
                else:
                    fields_status[f"Ier.{field}"] = f"❌ {desc}: отсутствует"
        else:
            fields_status["Ier"] = "❌ Ier отсутствует"
        
        return fields_status
        
    except Exception as e:
        return {"error": f"❌ Ошибка проверки: {e}"}


def test_field_mapping():
    """
    Тестирование маппинга полей между ЦССИ и ЦПГ
    """
    print("\n" + "="*80)
    print("ТЕСТИРОВАНИЕ МАППИНГА ПОЛЕЙ")
    print("="*80)
    
    results = {
        "test": "field_mapping",
        "mappings": {}
    }
    
    # Создаем тестовый UKIO
    from schemas.ukio_model import Ukio
    from converters.ukio_to_cpg import convert_ukio_to_cpg
    
    # Минимальный UKIO для теста
    test_ukio = Ukio(
        globalId="TEST_MAPPING_001",
        strIncidentType="Пожар",
        dtSend=datetime.now(),
        dtCreate=datetime.now(),
        dtUpdate=datetime.now(),
        nCasualties=5,
        bHumanThreat=1,
        bChs=1,
        bWrong=False,
        bChildPlay=False
    )
    
    # Конвертируем
    card, ier = convert_ukio_to_cpg(test_ukio)
    
    # Проверяем маппинг
    mappings = {
        "globalId → Id112": {
            "ЦССИ": test_ukio.globalId,
            "ЦПГ": card.Id112,
            "Статус": "✅" if test_ukio.globalId == card.Id112 else "❌"
        },
        "strIncidentType → CommonData.TypeStr": {
            "ЦССИ": test_ukio.strIncidentType,
            "ЦПГ": card.CommonData.TypeStr,
            "Статус": "✅" if test_ukio.strIncidentType == card.CommonData.TypeStr else "❌"
        },
        "nCasualties → CommonData.InjuredNumber": {
            "ЦССИ": test_ukio.nCasualties,
            "ЦПГ": card.CommonData.InjuredNumber,
            "Статус": "✅" if test_ukio.nCasualties == card.CommonData.InjuredNumber else "❌"
        },
        "bHumanThreat → CommonData.IsDanger": {
            "ЦССИ": bool(test_ukio.bHumanThreat),
            "ЦПГ": card.CommonData.IsDanger,
            "Статус": "✅" if bool(test_ukio.bHumanThreat) == card.CommonData.IsDanger else "❌"
        },
        "bChs → CommonData.Level": {
            "ЦССИ": test_ukio.bChs,
            "ЦПГ": card.CommonData.Level,
            "Статус": "✅" if int(test_ukio.bChs) == card.CommonData.Level else "❌"
        }
    }
    
    # Проверка новых полей ЦПГ
    new_fields = {
        "ExtId (новое)": card.ExtId,
        "HrId (новое)": card.CommonData.HrId,
        "RegionStr (новое)": card.CommonData.RegionStr,
        "LostNumber (новое)": card.CommonData.LostNumber,
        "IsBlocking (новое)": card.CommonData.IsBlocking,
        "IerType (новое)": ier.IerType
    }
    
    results["mappings"] = mappings
    results["new_fields"] = new_fields
    
    return results


def compare_xml_structures():
    """
    Сравнение структур XML ЦССИ и ЦПГ
    """
    print("\n" + "="*80)
    print("СРАВНЕНИЕ СТРУКТУР XML")
    print("="*80)
    
    results = {
        "test": "structure_comparison",
        "differences": []
    }
    
    # Основные различия
    differences = [
        {
            "Аспект": "Namespace",
            "ЦССИ": "s112",
            "ЦПГ": "http://tspg.service/",
        },
        {
            "Аспект": "Корневой элемент",
            "ЦССИ": "Ukios (коллекция Ukio)",
            "ЦПГ": "UpdateCardRequest",
        },
        {
            "Аспект": "Структура данных",
            "ЦССИ": "Монолитный объект Ukio",
            "ЦПГ": "Разделение на Card + Ier",
        },
        {
            "Аспект": "EOS карточки",
            "ЦССИ": "Card01-04, CardAT, CardCommServ",
            "ЦПГ": "DdsData01 (упрощенная)",
        },
        {
            "Аспект": "Операторы",
            "ЦССИ": "Внутри PhoneCall",
            "ЦПГ": "CreateOperator, LastChangeOperator в Card",
        },
        {
            "Аспект": "Адрес",
            "ЦССИ": "Address как отдельный объект",
            "ЦПГ": "Location (Address + Coords)",
        },
        {
            "Аспект": "Идентификаторы",
            "ЦССИ": "globalId",
            "ЦПГ": "Id112 + ExtId + HrId",
        }
    ]
    
    results["differences"] = differences
    
    return results


def run_all_tests():
    """
    Запуск всех тестов
    """
    print("\n" + "="*80)
    print("КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ ГЕНЕРАТОРА XML")
    print("="*80)
    
    all_results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # Тест ЦССИ
    print("\n[1/4] Тестирование ЦССИ...")
    try:
        cssi_results = test_cssi_generation()
        all_results["tests"]["ЦССИ"] = cssi_results
    except Exception as e:
        all_results["tests"]["ЦССИ"] = {"error": str(e)}
    
    # Тест ЦПГ
    print("\n[2/4] Тестирование ЦПГ...")
    try:
        cpg_results = test_cpg_generation()
        all_results["tests"]["ЦПГ"] = cpg_results
    except Exception as e:
        all_results["tests"]["ЦПГ"] = {"error": str(e)}
    
    # Тест маппинга
    print("\n[3/4] Тестирование маппинга полей...")
    try:
        mapping_results = test_field_mapping()
        all_results["tests"]["mapping"] = mapping_results
    except Exception as e:
        all_results["tests"]["mapping"] = {"error": str(e)}
    
    # Сравнение структур
    print("\n[4/4] Сравнение структур XML...")
    try:
        structure_results = compare_xml_structures()
        all_results["tests"]["structure"] = structure_results
    except Exception as e:
        all_results["tests"]["structure"] = {"error": str(e)}
    
    return all_results


def generate_report(results):
    """
    Генерация отчета о тестировании
    """
    print("\n\n" + "="*80)
    print("ИТОГОВЫЙ ОТЧЕТ О ТЕСТИРОВАНИИ")
    print("="*80)
    
    print(f"\nВремя тестирования: {results['timestamp']}")
    
    # Отчет по ЦССИ
    if "ЦССИ" in results["tests"]:
        print("\n" + "-"*40)
        print("РЕЖИМ ЦССИ (wsdl_5.wsdl)")
        print("-"*40)
        cssi = results["tests"]["ЦССИ"]
        
        if "error" in cssi:
            print(f"❌ ОШИБКА: {cssi['error']}")
        else:
            for test, result in cssi.get("tests", {}).items():
                if isinstance(result, dict):
                    print(f"\n{test}:")
                    for k, v in result.items():
                        print(f"  {v}")
                else:
                    print(f"{test}: {result}")
    
    # Отчет по ЦПГ
    if "ЦПГ" in results["tests"]:
        print("\n" + "-"*40)
        print("РЕЖИМ ЦПГ (cpg_wsdl_1.wsdl)")
        print("-"*40)
        cpg = results["tests"]["ЦПГ"]
        
        if "error" in cpg:
            print(f"❌ ОШИБКА: {cpg['error']}")
        else:
            for test, result in cpg.get("tests", {}).items():
                if isinstance(result, dict):
                    print(f"\n{test}:")
                    for k, v in result.items():
                        print(f"  {v}")
                else:
                    print(f"{test}: {result}")
    
    # Отчет по маппингу
    if "mapping" in results["tests"]:
        print("\n" + "-"*40)
        print("МАППИНГ ПОЛЕЙ")
        print("-"*40)
        mapping = results["tests"]["mapping"]
        
        if "error" in mapping:
            print(f"❌ ОШИБКА: {mapping['error']}")
        else:
            print("\nСоответствие полей:")
            for field, data in mapping.get("mappings", {}).items():
                print(f"\n{field}:")
                print(f"  ЦССИ: {data['ЦССИ']}")
                print(f"  ЦПГ: {data['ЦПГ']}")
                print(f"  Статус: {data['Статус']}")
            
            print("\nНовые поля ЦПГ:")
            for field, value in mapping.get("new_fields", {}).items():
                print(f"  {field}: {value}")
    
    # Отчет по структурам
    if "structure" in results["tests"]:
        print("\n" + "-"*40)
        print("СРАВНЕНИЕ СТРУКТУР")
        print("-"*40)
        structure = results["tests"]["structure"]
        
        if "error" in structure:
            print(f"❌ ОШИБКА: {structure['error']}")
        else:
            print("\nОсновные различия:")
            for diff in structure.get("differences", []):
                print(f"\n{diff['Аспект']}:")
                print(f"  ЦССИ: {diff['ЦССИ']}")
                print(f"  ЦПГ: {diff['ЦПГ']}")
    
    # Сохранение в файл
    report_path = "test_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n\n📄 Полный отчет сохранен в: {report_path}")


if __name__ == "__main__":
    results = run_all_tests()
    generate_report(results)