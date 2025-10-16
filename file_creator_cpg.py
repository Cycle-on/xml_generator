"""
XML генератор для системы ЦПГ
Создает XML файлы согласно cpg_wsdl_1.wsdl
"""
import os
import gc
import datetime
import xml.etree.ElementTree as ET
from typing import Optional
from pydantic import BaseModel

from schemas.cpg_models import CPGCard, CPGIer, UpdateCardRequest
from config import load_config

config = load_config()

# Namespace для ЦПГ
CPG_NAMESPACE = "http://tspg.service/"
NAMESPACES = {
    'tns': CPG_NAMESPACE,
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}


def create_cpg_xml_file(
    card: Optional[CPGCard], 
    ier: Optional[CPGIer], 
    filename: str,
    region_name: str = "rsc-region-05",
    operation: str = "UpdateCard"
) -> str:
    """
    Создает XML файл в формате ЦПГ
    
    Args:
        card: Карточка в формате ЦПГ
        ier: Обращение в формате ЦПГ
        filename: Имя файла (без расширения)
        region_name: Название региона для директории
        operation: Тип операции (UpdateCard, CancelCard, etc.)
        
    Returns:
        str: Путь к созданному файлу
    """
    # Создаем UpdateCardRequest
    request = UpdateCardRequest(
        SysCode="XML_GEN_112",
        Card=card,
        Ier=ier
    )
    
    # Генерируем XML
    xml_element = _generate_xml_from_cpg_model(request, operation)
    
    # Сохраняем в файл
    file_path = _save_xml_to_file(xml_element, filename, region_name, operation)
    
    return file_path


def _generate_xml_from_cpg_model(model: BaseModel, operation: str = "UpdateCard") -> ET.Element:
    """
    Генерирует XML из Pydantic модели для ЦПГ
    
    Args:
        model: Pydantic модель
        operation: Тип операции
        
    Returns:
        ET.Element: Корневой элемент XML
    """
    # Регистрируем namespaces
    for prefix, uri in NAMESPACES.items():
        ET.register_namespace(prefix, uri)
    
    # Создаем корневой элемент с namespace
    root_tag = f"{{{CPG_NAMESPACE}}}{operation}Request"
    root = ET.Element(root_tag)
    
    # Конвертируем модель в словарь
    model_dict = model.model_dump(exclude_none=True)
    
    # Рекурсивно добавляем элементы
    _add_elements_to_xml(root, model_dict, CPG_NAMESPACE)
    
    return root


def _add_elements_to_xml(parent: ET.Element, data: dict, namespace: str):
    """
    Рекурсивно добавляет элементы в XML дерево
    
    Args:
        parent: Родительский элемент
        data: Данные для добавления
        namespace: Namespace для элементов
    """
    for key, value in data.items():
        if value is None:
            continue
            
        # Создаем элемент с namespace
        element_tag = f"{{{namespace}}}{key}"
        
        if isinstance(value, dict):
            # Вложенный объект
            sub_element = ET.SubElement(parent, element_tag)
            _add_elements_to_xml(sub_element, value, namespace)
        elif isinstance(value, list):
            # Список элементов
            for item in value:
                if isinstance(item, dict):
                    sub_element = ET.SubElement(parent, element_tag)
                    _add_elements_to_xml(sub_element, item, namespace)
                else:
                    sub_element = ET.SubElement(parent, element_tag)
                    sub_element.text = _format_value(item, key)
        else:
            # Простое значение
            element = ET.SubElement(parent, element_tag)
            element.text = _format_value(value, key)


def _format_value(value, field_name: str = "") -> str:
    """
    Форматирует значение для XML
    
    Args:
        value: Значение для форматирования
        field_name: Имя поля для определения типа времени
        
    Returns:
        str: Отформатированное значение
    """
    if isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, datetime.datetime):
        formatted_value = value.isoformat()
        # Добавляем Z для полей времени (аналогично ЦССИ)
        if "time" in field_name.lower() or "created" in field_name.lower() or "changed" in field_name.lower():
            formatted_value += "Z"
        return formatted_value
    elif value is None:
        return ""
    else:
        return str(value)


def _save_xml_to_file(xml_element: ET.Element, filename: str, region_name: str, operation: str) -> str:
    """
    Сохраняет XML элемент в файл
    
    Args:
        xml_element: XML элемент для сохранения
        filename: Имя файла (без расширения)
        region_name: Название региона
        operation: Тип операции
        
    Returns:
        str: Путь к сохраненному файлу
    """
    # Создаем директорию для ЦПГ файлов
    dir_path = os.path.join(
        config.output_directory_name + "_cpg",  # Отдельная директория для ЦПГ
        str(region_name),
        operation
    )
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    # Полный путь к файлу
    file_path = os.path.join(dir_path, f"{filename}.xml")
    
    # Создаем дерево и сохраняем
    tree = ET.ElementTree(xml_element)
    
    # Добавляем XML декларацию и форматируем
    with open(file_path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True, method="xml")
    
    # Читаем файл обратно для форматирования (добавление отступов)
    _format_xml_file(file_path)
    
    # Очистка памяти
    del tree
    gc.collect()
    
    return file_path


def _format_xml_file(file_path: str):
    """
    Форматирует XML файл для читаемости (добавляет отступы)
    
    Args:
        file_path: Путь к файлу
    """
    try:
        # Читаем файл
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Добавляем отступы
        _indent_xml(root)
        
        # Сохраняем обратно
        tree.write(file_path, encoding="utf-8", xml_declaration=True, method="xml")
    except Exception as e:
        print(f"Не удалось отформатировать XML: {e}")


def _indent_xml(elem, level=0):
    """
    Рекурсивно добавляет отступы в XML элемент
    
    Args:
        elem: XML элемент
        level: Уровень вложенности
    """
    indent = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for child in elem:
            _indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent


def create_cpg_xml_from_ukio(ukio, filename: str, region_name: str = "rsc-region-05") -> Optional[str]:
    """
    Удобная функция для создания XML из Ukio через конвертацию
    
    Args:
        ukio: Объект Ukio
        filename: Имя файла
        region_name: Название региона
        
    Returns:
        str: Путь к созданному файлу или None
    """
    from converters.ukio_to_cpg import convert_ukio_to_cpg
    
    # Конвертируем Ukio в Card + Ier
    card, ier = convert_ukio_to_cpg(ukio)
    
    if not card and not ier:
        print(f"Не удалось конвертировать Ukio в CPG для файла {filename}")
        return None
    
    # Создаем XML файл
    return create_cpg_xml_file(card, ier, filename, region_name)


def modify_cpg_xml_file_to_send(file_path: str, prefix: str = "", postfix: str = ""):
    """
    Модифицирует XML файл для отправки (добавляет SOAP envelope если нужно)
    Аналог modify_xml_file_to_send для ЦПГ
    
    Args:
        file_path: Путь к файлу
        prefix: Префикс для добавления
        postfix: Постфикс для добавления
    """
    if not prefix and not postfix:
        return  # Ничего не делаем если нет обертки
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Добавляем обертку
    wrapped_content = prefix + content + postfix
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(wrapped_content)