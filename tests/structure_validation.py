"""
Валидация структур данных ЦССИ и ЦПГ
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import fill_constants
fill_constants()

def validate_wsdl_structures():
    """
    Проверка соответствия моделей WSDL схемам
    """
    print("\n" + "="*80)
    print("ВАЛИДАЦИЯ СТРУКТУР ДАННЫХ ПО WSDL")
    print("="*80)
    
    # Анализ wsdl_5.wsdl для ЦССИ
    from wsdl_parser.wsdl_tester import get_types_from_wsdl
    
    print("\n1. Анализ wsdl_5.wsdl (ЦССИ)...")
    try:
        cssi_types = get_types_from_wsdl("wsdl_5.wsdl")
        print(f"   ✅ Найдено типов: {len(cssi_types)}")
        
        # Основные типы ЦССИ
        main_types = ["Ukio", "PhoneCall", "Address", "CallContent", 
                      "Card01", "Card02", "Card03", "Card04", "CardAT", "CardCommServ"]
        
        for type_name in main_types:
            if type_name in cssi_types:
                fields_count = len(cssi_types[type_name])
                print(f"   ✅ {type_name}: {fields_count} полей")
            else:
                print(f"   ❌ {type_name}: не найден в WSDL")
                
    except Exception as e:
        print(f"   ❌ Ошибка анализа WSDL: {e}")
    
    # Анализ cpg_wsdl_1.wsdl для ЦПГ
    print("\n2. Анализ cpg_wsdl_1.wsdl (ЦПГ)...")
    import xml.etree.ElementTree as ET
    
    try:
        tree = ET.parse("cpg_wsdl_1.wsdl")
        root = tree.getroot()
        
        # Считаем complexType элементы
        ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
        complex_types = root.findall(".//xs:complexType", ns)
        
        print(f"   ✅ Найдено типов: {len(complex_types)}")
        
        # Основные типы ЦПГ
        cpg_types = {}
        for ct in complex_types:
            name = ct.get("name")
            if name:
                elements = ct.findall(".//xs:element", ns)
                cpg_types[name] = len(elements)
        
        main_cpg_types = ["Card", "Ier", "CommonData", "DdsData01", 
                          "Location", "Address", "Operator"]
        
        for type_name in main_cpg_types:
            if type_name in cpg_types:
                print(f"   ✅ {type_name}: {cpg_types[type_name]} полей")
            else:
                print(f"   ❌ {type_name}: не найден в WSDL")
                
    except Exception as e:
        print(f"   ❌ Ошибка анализа WSDL: {e}")
    
    return cssi_types, cpg_types


def validate_models():
    """
    Проверка Pydantic моделей
    """
    print("\n3. Проверка Pydantic моделей...")
    
    # Проверка моделей ЦССИ
    print("\n   Модели ЦССИ:")
    try:
        from schemas.ukio_model import Ukio, Address, CallContent
        from schemas.phonecall import PhoneCall
        print("   ✅ Ukio - загружен")
        print("   ✅ Address - загружен")
        print("   ✅ CallContent - загружен")
        print("   ✅ PhoneCall - загружен")
    except ImportError as e:
        print(f"   ❌ Ошибка импорта: {e}")
    
    # Проверка моделей ЦПГ
    print("\n   Модели ЦПГ:")
    try:
        from schemas.cpg_models import (
            CPGCard, CPGIer, CPGCommonData, CPGDdsData01,
            CPGLocation, CPGAddress, CPGOperator,
            UpdateCardRequest
        )
        print("   ✅ CPGCard - загружен")
        print("   ✅ CPGIer - загружен")
        print("   ✅ CPGCommonData - загружен")
        print("   ✅ CPGDdsData01 - загружен")
        print("   ✅ CPGLocation - загружен")
        print("   ✅ CPGAddress - загружен")
        print("   ✅ CPGOperator - загружен")
        print("   ✅ UpdateCardRequest - загружен")
    except ImportError as e:
        print(f"   ❌ Ошибка импорта: {e}")


def check_converter():
    """
    Проверка работы конвертера
    """
    print("\n4. Проверка конвертера UKIO → CPG...")
    
    from datetime import datetime
    from schemas.ukio_model import Ukio
    from converters.ukio_to_cpg import convert_ukio_to_cpg
    
    # Создаем минимальный UKIO
    test_data = {
        "globalId": "CONV_TEST_001",
        "strIncidentType": "Тестовое происшествие",
        "dtSend": datetime.now(),
        "dtCreate": datetime.now(),
        "dtUpdate": datetime.now(),
        "nCasualties": 3,
        "bHumanThreat": 1,
        "bChs": 0,
        "bWrong": False,
        "bChildPlay": False
    }
    
    try:
        ukio = Ukio(**test_data)
        print("   ✅ Тестовый UKIO создан")
        
        # Конвертируем
        card, ier = convert_ukio_to_cpg(ukio)
        
        if card and ier:
            print("   ✅ Конвертация успешна")
            print(f"      - Card.Id112 = {card.Id112}")
            print(f"      - Card.ExtId = {card.ExtId}")
            print(f"      - Card.CommonData.TypeStr = {card.CommonData.TypeStr}")
            print(f"      - Ier.Id = {ier.Id}")
            print(f"      - Ier.IerType = {ier.IerType}")
        else:
            print("   ❌ Конвертация не удалась")
            
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")


def check_xml_generation():
    """
    Проверка генерации XML
    """
    print("\n5. Проверка генерации XML...")
    
    from datetime import datetime
    from schemas.ukio_model import Ukio
    from schemas.cpg_models import CPGCard, CPGIer, CPGCommonData, CPGLocation, CPGOperator
    import xml.etree.ElementTree as ET
    
    # Создаем минимальную Card
    try:
        card = CPGCard(
            Id112="XML_TEST_001",
            ExtId="EXT_TEST",
            Location=CPGLocation(),
            CommonData=CPGCommonData(
                TypeStr="Тест",
                RegionStr="Тестовый регион",
                TimeIsoStr=datetime.now().isoformat()
            ),
            CreateOperator=CPGOperator(OperatorLogin="test_op"),
            LastChangeOperator=CPGOperator(OperatorLogin="test_op"),
            IncidentState="New",
            Created=datetime.now().isoformat(),
            Changed=datetime.now().isoformat()
        )
        print("   ✅ CPGCard создан")
        
        # Создаем минимальный Ier
        ier = CPGIer(
            IerIsoTime=datetime.now().isoformat(),
            CgPn="112",
            AcceptOperator=CPGOperator(OperatorLogin="test_op"),
            IerType=1
        )
        print("   ✅ CPGIer создан")
        
        # Проверка сериализации
        card_dict = card.model_dump(exclude_none=True)
        ier_dict = ier.model_dump(exclude_none=True)
        
        print(f"   ✅ Сериализация Card: {len(card_dict)} полей")
        print(f"   ✅ Сериализация Ier: {len(ier_dict)} полей")
        
    except Exception as e:
        print(f"   ❌ Ошибка создания моделей: {e}")


def analyze_differences():
    """
    Анализ ключевых различий
    """
    print("\n" + "="*80)
    print("АНАЛИЗ КЛЮЧЕВЫХ РАЗЛИЧИЙ")
    print("="*80)
    
    differences = {
        "✅ КОРРЕКТНО РЕАЛИЗОВАНО": [
            "• Маппинг основных полей (globalId → Id112)",
            "• Маппинг типов инцидентов (strIncidentType → TypeStr)",
            "• Маппинг пострадавших (nCasualties → InjuredNumber)",
            "• Маппинг угрозы людям (bHumanThreat → IsDanger)",
            "• Маппинг ЧС (bChs → Level)",
            "• Генерация новых идентификаторов (ExtId, HrId)",
            "• Разделение Ukio на Card + Ier",
            "• Новый namespace (http://tspg.service/)",
            "• Структура UpdateCardRequest"
        ],
        
        "⚠️ ЧАСТИЧНО РЕАЛИЗОВАНО": [
            "• Конвертация только Card01 → DdsData01 (другие EOS карточки игнорируются)",
            "• Упрощенный маппинг адресов (не все поля заполняются)",
            "• ЭРА-ГЛОНАСС маппинг (базовые поля)",
            "• Операторы (создаются дефолтные при отсутствии)"
        ],
        
        "❌ НЕ РЕАЛИЗОВАНО": [
            "• Операции CancelCard, AddReaction, FinishReaction, CloseCard",
            "• Пропущенные вызовы (MissedCall) в ЦПГ",
            "• Логика генерации новых полей (используются заглушки)",
            "• Card02, Card03, Card04, CardAT, CardCommServ в ЦПГ",
            "• Полный маппинг всех полей Address",
            "• Валидация по XSD схеме"
        ],
        
        "🔄 РАЗЛИЧИЯ В СТРУКТУРЕ": [
            "• ЦССИ: Монолитный Ukio содержит все данные",
            "• ЦПГ: Разделение на Card (карточка) и Ier (обращение)",
            "• ЦССИ: PhoneCall содержит оператора",
            "• ЦПГ: Операторы вынесены в Card (CreateOperator, LastChangeOperator)",
            "• ЦССИ: Множество типов EOS карточек",
            "• ЦПГ: Упрощенная DdsData01 только для службы 01",
            "• ЦССИ: globalId как единственный идентификатор",
            "• ЦПГ: Три идентификатора (Id112, ExtId, HrId)"
        ]
    }
    
    for category, items in differences.items():
        print(f"\n{category}")
        for item in items:
            print(item)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("КОМПЛЕКСНАЯ ВАЛИДАЦИЯ СТРУКТУР ЦССИ И ЦПГ")
    print("="*80)
    
    # Валидация WSDL
    cssi_types, cpg_types = validate_wsdl_structures()
    
    # Проверка моделей
    validate_models()
    
    # Проверка конвертера
    check_converter()
    
    # Проверка генерации XML
    check_xml_generation()
    
    # Анализ различий
    analyze_differences()
    
    print("\n" + "="*80)
    print("ВАЛИДАЦИЯ ЗАВЕРШЕНА")
    print("="*80)