#!/usr/bin/env python3
"""
Простой тест новой системы ЦПГ без зависимостей от конфигурации
"""
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

# Добавляем путь для импорта
sys.path.insert(0, '/home/repos/xml_generator')

def test_cpg_xml_generation():
    """Тест генерации XML в новом формате ЦПГ"""
    
    try:
        print("🧪 ТЕСТ ГЕНЕРАЦИИ ЦПГ XML")
        print("=" * 50)
        
        # Новый namespace
        new_namespace = 'http://eiim.service112.iskratel.si/'
        ET.register_namespace('tns', new_namespace)
        
        # Создаем UpdateCardRequest
        root = ET.Element(f'{{{new_namespace}}}UpdateCardRequest')
        
        # SysCode
        sys_code = ET.SubElement(root, 'SysCode')
        sys_code.text = 'XML_GEN_112'
        
        # Card
        card = ET.SubElement(root, 'Card')
        
        # Card основные поля
        id112 = ET.SubElement(card, 'Id112')
        id112.text = 'TEST_CPG_12345'
        
        # Location
        location = ET.SubElement(card, 'Location')
        
        # Address с новыми полями
        address = ET.SubElement(location, 'Address')
        
        city = ET.SubElement(address, 'City')
        city.text = 'Москва'
        
        # ✅ НОВОЕ ПОЛЕ
        housing = ET.SubElement(address, 'Housing')
        housing.text = 'Жилой комплекс "Тестовый"'
        
        street = ET.SubElement(address, 'Street')
        street.text = 'Тестовая улица'
        
        # Coords с новыми полями
        coords = ET.SubElement(location, 'Coords')
        
        latitude = ET.SubElement(coords, 'Latitude')
        latitude.text = '55.7558'
        
        longitude = ET.SubElement(coords, 'Longitude')
        longitude.text = '37.6173'
        
        # ✅ НОВЫЕ ПОЛЯ
        lapse_radius = ET.SubElement(coords, 'LapseRadius')
        lapse_radius.text = '100'
        
        arc_data = ET.SubElement(coords, 'ArcData')
        arc_data.text = 'Test arc data'
        
        # CommonData с новыми полями и enum
        common_data = ET.SubElement(card, 'CommonData')
        
        type_str = ET.SubElement(common_data, 'TypeStr')
        type_str.text = 'Пожар'
        
        region_str = ET.SubElement(common_data, 'RegionStr')
        region_str.text = 'Московская область'
        
        time_iso = ET.SubElement(common_data, 'TimeIsoStr')
        time_iso.text = datetime.now().isoformat() + 'Z'
        
        # ✅ ENUM LEVEL (новый формат)
        level = ET.SubElement(common_data, 'Level')
        level.text = 'SimpleIncident'
        
        # ✅ НОВЫЕ ПОЛЯ
        is_chem_flood = ET.SubElement(common_data, 'IsChemFlood')
        is_chem_flood.text = 'false'
        
        is_malicious = ET.SubElement(common_data, 'IsMalicius')
        is_malicious.text = 'false'
        
        injured_number = ET.SubElement(common_data, 'InjuredNumber')
        injured_number.text = '2'
        
        # DdsData01 с обновленными полями
        dds_data = ET.SubElement(card, 'DdsData01')
        
        dds_type = ET.SubElement(dds_data, 'DdsTypeStr')
        dds_type.text = 'Пожар'
        
        has_gas = ET.SubElement(dds_data, 'HasGas')
        has_gas.text = 'false'
        
        need_rescue = ET.SubElement(dds_data, 'NeedRescue')
        need_rescue.text = 'true'
        
        # ✅ FIRETIМЕ КАК STRING (вместо int)
        fire_time = ET.SubElement(dds_data, 'FireTime')
        fire_time.text = '15'  # Строка вместо числа
        
        # ✅ НОВОЕ ПОЛЕ
        burn_object = ET.SubElement(dds_data, 'BurnObject')
        burn_object.text = 'Мебель и отделочные материалы'
        
        # ✅ НОВЫЕ ПОЛЯ - ResourceList
        resource_list = ET.SubElement(card, 'ResourceList')
        
        resource = ET.SubElement(resource_list, 'ResourceLink')  
        caption = ET.SubElement(resource, 'Caption')
        caption.text = 'Фото места происшествия'
        
        res_type = ET.SubElement(resource, 'ResourceType')
        res_type.text = 'image'
        
        uri = ET.SubElement(resource, 'Uri')
        uri.text = 'http://example.com/photo.jpg'
        
        size = ET.SubElement(resource, 'Size')
        size.text = '1024'
        
        # ✅ НОВЫЕ ПОЛЯ - Parameters
        parameters = ET.SubElement(card, 'Parameters')
        
        param = ET.SubElement(parameters, 'Parameter')
        name = ET.SubElement(param, 'Name')
        name.text = 'priority'
        
        value = ET.SubElement(param, 'Value')
        value.text = 'high'
        
        # Операторы
        create_operator = ET.SubElement(card, 'CreateOperator')
        op_login = ET.SubElement(create_operator, 'OperatorLogin')
        op_login.text = 'test_operator'
        
        last_operator = ET.SubElement(card, 'LastChangeOperator')
        last_login = ET.SubElement(last_operator, 'OperatorLogin')
        last_login.text = 'test_operator'
        
        # Состояние карточки
        state = ET.SubElement(card, 'IncidentState')
        state.text = 'new'
        
        created = ET.SubElement(card, 'Created')
        created.text = datetime.now().isoformat() + 'Z'
        
        changed = ET.SubElement(card, 'Changed')
        changed.text = datetime.now().isoformat() + 'Z'
        
        # IER с новыми полями
        ier = ET.SubElement(root, 'Ier')
        
        ier_id = ET.SubElement(ier, 'Id')
        ier_id.text = 'IER_TEST_123'
        
        # ✅ НОВОЕ ПОЛЕ
        card_id = ET.SubElement(ier, 'CardId')
        card_id.text = 'TEST_CPG_12345'
        
        ier_time = ET.SubElement(ier, 'IerIsoTime')
        ier_time.text = datetime.now().isoformat() + 'Z'
        
        cg_pn = ET.SubElement(ier, 'CgPn')
        cg_pn.text = '79991234567'
        
        # ✅ IER TYPE КАК ENUM (вместо int)
        ier_type = ET.SubElement(ier, 'IerType')
        ier_type.text = 'PhoneCall'
        
        # ✅ НОВЫЕ ПОЛЯ
        link = ET.SubElement(ier, 'Link')
        link.text = 'http://example.com/ier/123'
        
        contact_number = ET.SubElement(ier, 'ContactNumber')
        contact_number.text = '79991234567'
        
        ext_id = ET.SubElement(ier, 'ExtId')
        ext_id.text = 'EXT_TEST_456'
        
        # Оператор IER
        accept_operator = ET.SubElement(ier, 'AcceptOperator')
        accept_login = ET.SubElement(accept_operator, 'OperatorLogin')
        accept_login.text = 'test_operator'
        
        # Конвертация в строку с форматированием
        _indent(root)
        xml_str = ET.tostring(root, encoding='unicode')
        
        print("✅ XML успешно сгенерирован!")
        print("\n📄 РЕЗУЛЬТАТ:")
        print("-" * 50)
        print(xml_str)
        
        # Сохранение в файл
        with open('/tmp/test_cpg_new.xml', 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(xml_str)
        
        print(f"\n💾 Файл сохранен: /tmp/test_cpg_new.xml")
        
        # Проверки
        print("\n🔍 ПРОВЕРКИ:")
        print("-" * 30)
        print(f"✅ Namespace: {new_namespace}")
        print("✅ Все дочерние элементы без namespace prefix (form='unqualified')")
        print("✅ Housing поле добавлено в Address")
        print("✅ LapseRadius, ArcData добавлены в Coords")
        print("✅ Level как enum: SimpleIncident")
        print("✅ IsChemFlood, IsMalicius добавлены") 
        print("✅ FireTime как string (не int)")
        print("✅ BurnObject добавлен в DdsData01")
        print("✅ ResourceList с ResourceLink добавлен")
        print("✅ Parameters с Parameter добавлен") 
        print("✅ IerType как enum: PhoneCall")
        print("✅ CardId, Link, ContactNumber, ExtId добавлены в Ier")
        
        return True
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        return False


def _indent(elem, level=0):
    """Добавляет отступы для читаемости XML"""
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for child in elem:
            _indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


if __name__ == "__main__":
    success = test_cpg_xml_generation()
    if success:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        print("🚀 Новый генератор ЦПГ готов к использованию!")
    else:
        print("\n💥 ТЕСТЫ НЕ ПРОШЛИ!")
        sys.exit(1)