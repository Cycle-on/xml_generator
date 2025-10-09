"""
Тестовый скрипт для генерации одной карточки ЦПГ
Позволяет быстро проверить работоспособность всей цепочки
"""
import sys
import os
from datetime import datetime

# Добавляем родительскую директорию в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Инициализируем константы
from constants import fill_constants
fill_constants()

from config import load_config
from generators.ukio_generator import generate_ukio_phone_call_data
from converters.ukio_to_cpg import convert_ukio_to_cpg
from file_creator_cpg import create_cpg_xml_file
from generators.operators_and_arms import create_arms_and_operators, ARM_WORK, OPERATOR_WORK
from csv_parser.parse_addresses import fill_addresses
from csv_parser.parse_incident_types import fill_incident_type_lists

config = load_config()


def test_generate_single_cpg_card():
    """
    Генерирует одну карточку ЦПГ для тестирования
    """
    print("\n" + "="*60)
    print("ТЕСТОВАЯ ГЕНЕРАЦИЯ ОДНОЙ КАРТОЧКИ ЦПГ")
    print("="*60 + "\n")
    
    # Подготовка
    print("1. Подготовка окружения...")
    
    # Очищаем списки
    ARM_WORK.clear()
    OPERATOR_WORK.clear()
    
    # Создаем операторов и АРМы
    create_arms_and_operators()
    print(f"   ✅ Создано операторов: {len(OPERATOR_WORK)}")
    
    # Загружаем адреса и типы инцидентов
    region_name = "rsc-region-05"
    fill_incident_type_lists(region_name)
    addresses = fill_addresses(region_name)
    
    if addresses:
        print(f"   ✅ Загружено адресов: {len(addresses)}")
    else:
        print("   ⚠️  Адреса не загружены, будут использоваться дефолтные")
    
    # Генерация UKIO
    print("\n2. Генерация UKIO через существующий генератор...")
    call_date = datetime.now()
    ukio = generate_ukio_phone_call_data(call_date)
    
    if ukio is None:
        print("   ❌ Не удалось сгенерировать UKIO")
        return False
    
    print(f"   ✅ UKIO сгенерирован: {ukio.globalId}")
    print(f"      - Тип инцидента: {ukio.strIncidentType}")
    print(f"      - Состояние карточки: {ukio.strCardState}")
    print(f"      - Количество звонков: {len(ukio.phoneCall) if ukio.phoneCall else 0}")
    
    # Конвертация в ЦПГ
    print("\n3. Конвертация UKIO → CPG...")
    card, ier = convert_ukio_to_cpg(ukio)
    
    if not card or not ier:
        print("   ❌ Не удалось конвертировать в формат ЦПГ")
        return False
    
    print(f"   ✅ Конвертация успешна")
    print(f"      - Card.Id112: {card.Id112}")
    print(f"      - Card.ExtId: {card.ExtId}")
    print(f"      - Card.IncidentState: {card.IncidentState}")
    print(f"      - Ier.Id: {ier.Id}")
    print(f"      - Ier.HrId: {ier.HrId}")
    print(f"      - Ier.CgPn: {ier.CgPn}")
    
    # Генерация XML
    print("\n4. Генерация XML файла...")
    filename = f"test_cpg_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        file_path = create_cpg_xml_file(
            card=card,
            ier=ier,
            filename=filename,
            region_name=region_name,
            operation="UpdateCard"
        )
        
        print(f"   ✅ XML файл создан: {file_path}")
        
        # Проверяем размер файла
        file_size = os.path.getsize(file_path)
        print(f"      - Размер файла: {file_size} байт")
        
        # Читаем первые строки для проверки
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
            print("      - Первые строки файла:")
            for line in lines:
                print(f"        {line.rstrip()}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка при создании XML: {e}")
        return False


def test_validate_generated_xml():
    """
    Валидация сгенерированного XML
    """
    print("\n5. Валидация сгенерированного XML...")
    
    # Ищем последний сгенерированный файл
    cpg_dir = config.output_directory_name + "_cpg"
    
    if not os.path.exists(cpg_dir):
        print("   ⚠️  Директория с ЦПГ файлами не найдена")
        return False
    
    # Находим XML файлы
    xml_files = []
    for root, dirs, files in os.walk(cpg_dir):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))
    
    if not xml_files:
        print("   ⚠️  XML файлы не найдены")
        return False
    
    # Берем последний файл
    latest_file = max(xml_files, key=os.path.getctime)
    print(f"   Проверяем файл: {latest_file}")
    
    # Импортируем валидатор
    from validate_cpg_xml import validate_cpg_xml
    
    is_valid, errors = validate_cpg_xml(latest_file)
    
    if is_valid:
        print("   ✅ XML файл валидный")
        return True
    else:
        print("   ❌ XML файл содержит ошибки:")
        for error in errors:
            print(f"      - {error}")
        return False


def main():
    """
    Главная функция
    """
    success = test_generate_single_cpg_card()
    
    if success:
        # Опционально валидируем
        test_validate_generated_xml()
        
        print("\n" + "="*60)
        print("✅ ТЕСТОВАЯ ГЕНЕРАЦИЯ ЗАВЕРШЕНА УСПЕШНО")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("❌ ТЕСТОВАЯ ГЕНЕРАЦИЯ ЗАВЕРШЕНА С ОШИБКАМИ")
        print("="*60 + "\n")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)