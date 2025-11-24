"""
Тесты для конвертера Ukio -> CPG
"""
import sys
import os
from datetime import datetime

# Добавляем родительскую директорию в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Инициализируем константы перед импортом моделей
from constants import fill_constants
fill_constants()

from schemas.ukio_model import Ukio, Address, CallContent
from schemas.string_schemas import CardStates
from schemas.phonecall import PhoneCall
from schemas.string_eos import Operator
from converters.ukio_to_cpg import convert_ukio_to_cpg
from schemas.cpg_models import CPGCard, CPGIer


def create_test_ukio() -> Ukio:
    """
    Создает тестовый объект Ukio с минимальными данными
    
    Returns:
        Ukio: Тестовый объект
    """
    # Создаем оператора
    operator = Operator(
        operatorId="test_operator_1",
        strOperatorSurname="Иванов",
        strOperatorName="Иван",
        strOperatorLastName="Иванович",
        strOperatorPost="Оператор 112",
        strOperatorInfo="Тестовый оператор"
    )
    
    # Создаем телефонный звонок
    phone_call = PhoneCall(
        dtSend=datetime.now(),
        dtCall=datetime.now(),
        dtConnect=datetime.now(),
        dtEndCall=datetime.now(),
        operator=operator,
        bOperatorIniciatied=False,
        aCallEnded=True
    )
    
    # Создаем адрес
    address = Address(
        strAddress="г. Москва, ул. Тверская, д. 1",
        strCity="Москва",
        strDistrict="Центральный",
        strStreet="Тверская",
        strHouse="1",
        geoLatitude=55.7558,
        geoLongitude=37.6173
    )
    
    # Создаем контент звонка
    call_content = CallContent(
        strLastName="Петров",
        strName="Петр",
        strMiddleName="Петрович",
        strCallerContactPhone="+79001234567",
        strCgPN="112",
        appResAddress="г. Москва, ул. Арбат, д. 10",
        strLanguage="ru",
        strIncidentDescription="Пожар в квартире",
        appLocAddress="г. Москва, ул. Тверская, д. 1"
    )
    
    # Создаем Ukio
    ukio = Ukio(
        globalId="TEST_UKIO_001",
        strCardState=CardStates.NEW,
        strIncidentType="Пожар",
        dtSend=datetime.now(),
        dtCreate=datetime.now(),
        dtUpdate=datetime.now(),
        dtCall=datetime.now(),
        dtCallEnd=datetime.now(),
        aCallEnded=True,
        nCasualties=0,
        bHumanThreat=False,
        bChs=False,
        strCallSource="Мобильный телефон",
        bWrong=False,
        bChildPlay=False,
        phoneCall=[phone_call],
        address=address,
        callContent=call_content
    )
    
    return ukio


def test_basic_conversion():
    """
    Тест базовой конвертации Ukio в Card + Ier
    """
    print("\n=== Тест базовой конвертации ===")
    
    # Создаем тестовый Ukio
    ukio = create_test_ukio()
    print(f"Создан тестовый Ukio с ID: {ukio.globalId}")
    
    # Конвертируем
    card, ier = convert_ukio_to_cpg(ukio)
    
    # Проверяем что получили оба объекта
    assert card is not None, "Card не должен быть None"
    assert ier is not None, "Ier не должен быть None"
    print("✅ Card и Ier успешно созданы")
    
    # Проверяем что это правильные типы
    assert isinstance(card, CPGCard), "Card должен быть типа CPGCard"
    assert isinstance(ier, CPGIer), "Ier должен быть типа CPGIer"
    print("✅ Типы объектов корректны")
    
    # Проверяем маппинг основных полей
    assert card.Id112 == ukio.globalId, "Id112 должен совпадать с globalId"
    print(f"✅ Id112 корректно замаплен: {card.Id112}")
    
    # IncidentState теперь выбирается случайно из допустимых значений
    incident_state_values = ["New", "Created", "InWork", "Finished", "Closed", "Assigned", "NotSet"]
    assert card.IncidentState in incident_state_values, f"IncidentState должен быть из допустимых значений: {incident_state_values}"
    print(f"✅ IncidentState корректно выбран из допустимых значений: {card.IncidentState}")
    
    # Проверяем CommonData
    assert card.CommonData is not None, "CommonData не должна быть None"
    assert card.CommonData.TypeStr == ukio.strIncidentType, "TypeStr должен совпадать с strIncidentType"
    print(f"✅ CommonData.TypeStr корректно замаплен: {card.CommonData.TypeStr}")
    
    # Проверяем Location
    assert card.Location is not None, "Location не должен быть None"
    assert card.Location.Address is not None, "Location.Address не должен быть None"
    assert card.Location.Address.City == ukio.address.strCity, "City должен совпадать"
    print(f"✅ Location.Address.City корректно замаплен: {card.Location.Address.City}")
    
    # Проверяем Ier
    assert ier.CgPn == ukio.callContent.strCgPN, "CgPn должен совпадать"
    print(f"✅ Ier.CgPn корректно замаплен: {ier.CgPn}")
    
    assert ier.FullName is not None, "FullName не должен быть None"
    assert ier.FullName.LastName == ukio.callContent.strLastName, "LastName должен совпадать"
    print(f"✅ Ier.FullName корректно замаплен: {ier.FullName.LastName}")
    
    print("\n✅ Все проверки базовой конвертации пройдены успешно!")
    return True


def test_conversion_with_none_values():
    """
    Тест конвертации с пустыми значениями
    """
    print("\n=== Тест конвертации с пустыми значениями ===")
    
    # Создаем минимальный Ukio
    ukio = Ukio(
        globalId="TEST_MINIMAL_001",
        strCardState=None,
        strIncidentType=None,
        dtSend=datetime.now(),
        dtCreate=None,
        dtUpdate=None,
        bWrong=False,
        bChildPlay=False,
        phoneCall=None,
        address=None,
        callContent=None
    )
    
    print(f"Создан минимальный Ukio с ID: {ukio.globalId}")
    
    # Конвертируем
    card, ier = convert_ukio_to_cpg(ukio)
    
    # Проверяем что получили оба объекта даже с минимальными данными
    assert card is not None, "Card не должен быть None даже с минимальными данными"
    assert ier is not None, "Ier не должен быть None даже с минимальными данными"
    print("✅ Card и Ier созданы даже с минимальными данными")
    
    # Проверяем дефолтные значения
    assert card.Id112 == ukio.globalId, "Id112 должен быть установлен"
    assert card.ExtId is not None and card.ExtId.startswith("EXT_"), "ExtId должен быть сгенерирован"
    print(f"✅ Сгенерирован ExtId: {card.ExtId}")
    
    # IncidentState теперь выбирается случайно из допустимых значений
    incident_state_values = ["New", "Created", "InWork", "Finished", "Closed", "Assigned", "NotSet"]
    assert card.IncidentState in incident_state_values, f"IncidentState должен быть из допустимых значений: {incident_state_values}"
    print(f"✅ IncidentState выбран из допустимых значений: {card.IncidentState}")
    
    # IerType теперь строка из допустимых значений
    ier_type_values = ["NotSet", "PhoneCall", "Sms", "Fax", "EraGlonass", "Manual"]
    assert ier.IerType in ier_type_values, f"IerType должен быть из допустимых значений: {ier_type_values}"
    print(f"✅ IerType имеет корректное значение: {ier.IerType}")
    
    print("\n✅ Все проверки конвертации с пустыми значениями пройдены успешно!")
    return True


def test_operator_mapping():
    """
    Тест маппинга операторов
    """
    print("\n=== Тест маппинга операторов ===")
    
    # Создаем Ukio с операторами
    operator1 = Operator(
        operatorId="operator_1",
        strOperatorSurname="Сидоров",
        strOperatorName="Сидор",
        strOperatorLastName="Сидорович",
        strOperatorPost="Старший оператор",
        strOperatorInfo="Опытный оператор"
    )
    
    operator2 = Operator(
        operatorId="operator_2",
        strOperatorSurname="Козлов",
        strOperatorName="Козел",
        strOperatorLastName="Козлович",
        strOperatorPost="Младший оператор",
        strOperatorInfo="Новый оператор"
    )
    
    phone_call1 = PhoneCall(
        dtCall=datetime.now(),
        operator=operator1
    )
    
    phone_call2 = PhoneCall(
        dtCall=datetime.now(),
        operator=operator2
    )
    
    ukio = Ukio(
        globalId="TEST_OPERATORS_001",
        bWrong=False,
        bChildPlay=False,
        phoneCall=[phone_call1, phone_call2],
        dtSend=datetime.now()
    )
    
    # Конвертируем
    card, ier = convert_ukio_to_cpg(ukio)
    
    # Проверяем операторов в Card
    assert card.CreateOperator.OperatorLogin == "operator_1", "CreateOperator должен быть первый оператор"
    assert card.LastChangeOperator.OperatorLogin == "operator_2", "LastChangeOperator должен быть последний оператор"
    print(f"✅ CreateOperator: {card.CreateOperator.OperatorLogin}")
    print(f"✅ LastChangeOperator: {card.LastChangeOperator.OperatorLogin}")
    
    # Проверяем полное имя
    expected_name = "Сидоров Сидор Сидорович"
    assert card.CreateOperator.OperatorName == expected_name, f"Имя должно быть {expected_name}"
    print(f"✅ Полное имя оператора: {card.CreateOperator.OperatorName}")
    
    # Проверяем оператора в Ier
    assert ier.AcceptOperator.OperatorLogin == "operator_1", "AcceptOperator должен быть первый оператор"
    print(f"✅ AcceptOperator: {ier.AcceptOperator.OperatorLogin}")
    
    print("\n✅ Все проверки маппинга операторов пройдены успешно!")
    return True


def run_all_tests():
    """
    Запуск всех тестов
    """
    print("="*50)
    print("ЗАПУСК ТЕСТОВ КОНВЕРТЕРА UKIO -> CPG")
    print("="*50)
    
    tests = [
        ("Базовая конвертация", test_basic_conversion),
        ("Конвертация с пустыми значениями", test_conversion_with_none_values),
        ("Маппинг операторов", test_operator_mapping)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"\n❌ Тест '{test_name}' провален: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ Тест '{test_name}' завершился с ошибкой: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print(f"Пройдено: {passed}")
    print(f"Провалено: {failed}")
    print(f"Всего: {passed + failed}")
    print("="*50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)