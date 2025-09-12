#!/usr/bin/env python3
"""
Тестирование валидации ЦПГ XML файлов по cpg_wsdl_1.wsdl
"""
import xml.etree.ElementTree as ET
from pprint import pprint
import os
import sys

def get_types_from_cpg_wsdl(wsdl_path: str) -> dict:
    """Извлекает типы и их поля из ЦПГ WSDL"""
    types = {}
    tree = ET.parse(wsdl_path)
    root = tree.getroot()
    
    # Namespace для XSD
    ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    
    # Найдем все complexType элементы в WSDL
    for complex_type in root.findall(".//xs:complexType", ns):
        type_name = complex_type.get('name')
        if type_name:
            types[type_name] = set()
            
            # Извлечем все элементы (поля) из этого типа
            for element in complex_type.findall(".//xs:element", ns):
                field_name = element.get('name')
                if field_name:
                    types[type_name].add(field_name)
    
    return types


def parse_cpg_xml(xml_path: str) -> dict:
    """Парсит ЦПГ XML и извлекает структуру"""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Namespace для ЦПГ
    ns = {'tns': 'http://tspg.service/'}
    
    structure = {}
    
    # UpdateCardRequest
    structure['UpdateCardRequest'] = set()
    for child in root:
        # Убираем namespace из имени тега
        tag = child.tag.replace('{http://tspg.service/}', '')
        structure['UpdateCardRequest'].add(tag)
    
    # Card
    card = root.find('tns:Card', ns)
    if card:
        structure['Card'] = set()
        for child in card:
            tag = child.tag.replace('{http://tspg.service/}', '')
            structure['Card'].add(tag)
            
            # Для вложенных структур тоже собираем поля
            if tag in ['Location', 'CommonData', 'DdsData01', 'DdsData02', 'DdsData03', 
                      'DdsData04', 'DdsDataAT', 'DdsDataCommServ', 'CreateOperator', 'LastChangeOperator']:
                structure[tag] = set()
                for nested_child in child:
                    nested_tag = nested_child.tag.replace('{http://tspg.service/}', '')
                    structure[tag].add(nested_tag)
    
    # Ier
    ier = root.find('tns:Ier', ns)
    if ier:
        structure['Ier'] = set()
        for child in ier:
            tag = child.tag.replace('{http://tspg.service/}', '')
            structure['Ier'].add(tag)
            
            # Для вложенных структур
            if tag in ['FullName', 'AcceptOperator', 'Location']:
                structure[f'Ier_{tag}'] = set()
                for nested_child in child:
                    nested_tag = nested_child.tag.replace('{http://tspg.service/}', '')
                    structure[f'Ier_{tag}'].add(nested_tag)
    
    return structure


def validate_cpg_file(xml_path: str, wsdl_path: str):
    """Валидирует ЦПГ XML файл против WSDL схемы"""
    print(f"\n{'='*80}")
    print(f"Валидация файла: {os.path.basename(xml_path)}")
    print(f"WSDL схема: {os.path.basename(wsdl_path)}")
    print('='*80)
    
    # Получаем типы из WSDL
    wsdl_types = get_types_from_cpg_wsdl(wsdl_path)
    
    # Парсим XML
    xml_structure = parse_cpg_xml(xml_path)
    
    # Проверяем обязательные элементы
    print("\n📋 Проверка обязательных элементов:")
    
    required_in_card = {
        'Location', 'CommonData', 'CreateOperator', 
        'LastChangeOperator', 'IncidentState', 'Created', 'Changed'
    }
    
    if 'Card' in xml_structure:
        missing = required_in_card - xml_structure['Card']
        if missing:
            print(f"   ❌ В Card отсутствуют обязательные поля: {missing}")
        else:
            print(f"   ✅ Все обязательные поля Card присутствуют")
    else:
        print(f"   ❌ Card не найден в XML!")
    
    # Проверяем наличие DdsData (опционально - службы генерируются по вероятности)
    dds_services = ['DdsData01', 'DdsData02', 'DdsData03', 'DdsData04', 'DdsDataAT', 'DdsDataCommServ']
    found_services = []
    
    for service in dds_services:
        if service in xml_structure.get('Card', set()):
            found_services.append(service)
    
    if found_services:
        print(f"\n📋 Службы экстренного реагирования: найдено {len(found_services)} из 6")
        for service in found_services:
            print(f"   ✅ {service}")
    
    # Проверяем Ier
    print("\n📋 Проверка Ier (обращение):")
    required_in_ier = {'IerIsoTime', 'CgPn', 'AcceptOperator', 'IerType'}
    
    if 'Ier' in xml_structure:
        missing = required_in_ier - xml_structure['Ier']
        if missing:
            print(f"   ❌ В Ier отсутствуют обязательные поля: {missing}")
        else:
            print(f"   ✅ Все обязательные поля Ier присутствуют")
    else:
        print(f"   ❌ Ier не найден в XML!")
    
    # Итоговая оценка
    print(f"\n{'='*80}")
    print("📊 ИТОГ ВАЛИДАЦИИ:")
    
    is_valid = True
    
    # Проверка основной структуры
    if 'Card' in xml_structure and 'Ier' in xml_structure:
        print("   ✅ Основная структура корректна (Card + Ier)")
    else:
        print("   ❌ Основная структура некорректна")
        is_valid = False
    
    # Проверка обязательных полей
    if 'Card' in xml_structure:
        if not (required_in_card - xml_structure['Card']):
            print("   ✅ Обязательные поля Card присутствуют")
        else:
            print("   ❌ Отсутствуют обязательные поля Card")
            is_valid = False
    
    if 'Ier' in xml_structure:
        if not (required_in_ier - xml_structure['Ier']):
            print("   ✅ Обязательные поля Ier присутствуют")
        else:
            print("   ❌ Отсутствуют обязательные поля Ier")
            is_valid = False
    
    if is_valid:
        print("\n🎉 ФАЙЛ ВАЛИДЕН ПО СХЕМЕ cpg_wsdl_1.wsdl")
    else:
        print("\n❌ ФАЙЛ НЕ ПРОШЕЛ ВАЛИДАЦИЮ")
    
    print('='*80)
    
    return is_valid


def test_all_cpg_files():
    """Тестирует все сгенерированные ЦПГ файлы"""
    cpg_dir = "../files/TEST_cpg"
    wsdl_path = "../cpg_wsdl_1.wsdl"
    
    # Найдем все XML файлы
    xml_files = []
    for root, dirs, files in os.walk(cpg_dir):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))
    
    print(f"\n🔍 Найдено {len(xml_files)} XML файлов для проверки")
    
    valid_count = 0
    invalid_count = 0
    
    # Проверяем первые несколько файлов
    for xml_file in xml_files[:5]:  # Проверим первые 5 файлов
        try:
            is_valid = validate_cpg_file(xml_file, wsdl_path)
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
        except Exception as e:
            print(f"❌ Ошибка при проверке {xml_file}: {e}")
            invalid_count += 1
    
    print(f"\n\n{'='*80}")
    print("📊 ОБЩАЯ СТАТИСТИКА:")
    print(f"   ✅ Валидных файлов: {valid_count}")
    print(f"   ❌ Невалидных файлов: {invalid_count}")
    print(f"   📈 Процент валидности: {valid_count/(valid_count+invalid_count)*100:.1f}%")
    print('='*80)


if __name__ == "__main__":
    # Сначала проверим наш тестовый файл со всеми службами
    test_file = "../files/TEST_cpg/test_multi_services/UpdateCard/test_all_services.xml"
    wsdl_file = "../cpg_wsdl_1.wsdl"
    
    if os.path.exists(test_file):
        print("\n🧪 ТЕСТ ФАЙЛА СО ВСЕМИ СЛУЖБАМИ:")
        validate_cpg_file(test_file, wsdl_file)
    
    # Затем проверим несколько реальных сгенерированных файлов
    print("\n\n🔬 ТЕСТ РЕАЛЬНЫХ СГЕНЕРИРОВАННЫХ ФАЙЛОВ:")
    test_all_cpg_files()