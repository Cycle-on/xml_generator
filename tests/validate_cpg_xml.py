"""
Валидация XML файлов по WSDL схеме ЦПГ
"""
import sys
import os
import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple

# Добавляем родительскую директорию в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def validate_cpg_xml(xml_file_path: str) -> Tuple[bool, List[str]]:
    """
    Валидация XML файла по структуре WSDL ЦПГ
    
    Args:
        xml_file_path: Путь к XML файлу
        
    Returns:
        Tuple[bool, List[str]]: (Валидный ли файл, Список ошибок/предупреждений)
    """
    errors = []
    warnings = []
    
    try:
        # Парсим XML
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        # Проверяем namespace
        expected_namespace = "http://tspg.service/"
        if not root.tag.startswith("{" + expected_namespace + "}"):
            errors.append(f"Неверный namespace. Ожидается: {expected_namespace}")
        
        # Проверяем корневой элемент
        valid_roots = [
            "UpdateCardRequest",
            "CancelCardRequest",
            "AddReactionRequest",
            "FinishReactionRequest",
            "CloseCardRequest"
        ]
        
        root_name = root.tag.split("}")[-1] if "}" in root.tag else root.tag
        if root_name not in valid_roots:
            errors.append(f"Неверный корневой элемент: {root_name}. Ожидается один из: {valid_roots}")
        
        # Проверяем обязательные поля для UpdateCardRequest
        if root_name == "UpdateCardRequest":
            errors.extend(_validate_update_card_request(root, expected_namespace))
        
    except ET.ParseError as e:
        errors.append(f"Ошибка парсинга XML: {e}")
    except Exception as e:
        errors.append(f"Неожиданная ошибка: {e}")
    
    is_valid = len(errors) == 0
    return is_valid, errors + warnings


def _validate_update_card_request(root: ET.Element, namespace: str) -> List[str]:
    """
    Валидация UpdateCardRequest
    
    Args:
        root: Корневой элемент
        namespace: Ожидаемый namespace
        
    Returns:
        List[str]: Список ошибок
    """
    errors = []
    ns = {"tns": namespace}
    
    # Проверяем SysCode
    sys_code = root.find("tns:SysCode", ns)
    if sys_code is None:
        errors.append("Отсутствует обязательное поле SysCode")
    elif not sys_code.text:
        errors.append("Поле SysCode пустое")
    
    # Проверяем Card или Ier (хотя бы один должен быть)
    card = root.find("tns:Card", ns)
    ier = root.find("tns:Ier", ns)
    
    if card is None and ier is None:
        errors.append("Должен быть указан хотя бы Card или Ier")
    
    # Проверяем структуру Card
    if card is not None:
        errors.extend(_validate_card(card, ns))
    
    # Проверяем структуру Ier
    if ier is not None:
        errors.extend(_validate_ier(ier, ns))
    
    return errors


def _validate_card(card: ET.Element, ns: Dict[str, str]) -> List[str]:
    """
    Валидация структуры Card
    
    Args:
        card: Элемент Card
        ns: Namespaces
        
    Returns:
        List[str]: Список ошибок
    """
    errors = []
    
    # Обязательные поля Card
    required_fields = [
        "Location",
        "CommonData",
        "CreateOperator",
        "LastChangeOperator",
        "IncidentState",
        "Created",
        "Changed"
    ]
    
    for field in required_fields:
        element = card.find(f"tns:{field}", ns)
        if element is None:
            errors.append(f"В Card отсутствует обязательное поле {field}")
    
    # Проверяем CommonData
    common_data = card.find("tns:CommonData", ns)
    if common_data is not None:
        # Обязательные поля CommonData
        type_str = common_data.find("tns:TypeStr", ns)
        region_str = common_data.find("tns:RegionStr", ns)
        time_iso_str = common_data.find("tns:TimeIsoStr", ns)
        
        if type_str is None:
            errors.append("В CommonData отсутствует обязательное поле TypeStr")
        if region_str is None:
            errors.append("В CommonData отсутствует обязательное поле RegionStr")
        if time_iso_str is None:
            errors.append("В CommonData отсутствует обязательное поле TimeIsoStr")
    
    return errors


def _validate_ier(ier: ET.Element, ns: Dict[str, str]) -> List[str]:
    """
    Валидация структуры Ier
    
    Args:
        ier: Элемент Ier
        ns: Namespaces
        
    Returns:
        List[str]: Список ошибок
    """
    errors = []
    
    # Обязательные поля Ier
    required_fields = [
        "IerIsoTime",
        "CgPn",
        "AcceptOperator",
        "IerType",
        "Location"
    ]
    
    for field in required_fields:
        element = ier.find(f"tns:{field}", ns)
        if element is None:
            errors.append(f"В Ier отсутствует обязательное поле {field}")
    
    return errors


def validate_directory(directory_path: str) -> Dict[str, Tuple[bool, List[str]]]:
    """
    Валидация всех XML файлов в директории
    
    Args:
        directory_path: Путь к директории
        
    Returns:
        Dict: Словарь {имя_файла: (валидный, список_ошибок)}
    """
    results = {}
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                is_valid, errors = validate_cpg_xml(file_path)
                results[file_path] = (is_valid, errors)
    
    return results


def main():
    """
    Главная функция для запуска из командной строки
    """
    if len(sys.argv) < 2:
        print("Использование: python validate_cpg_xml.py <путь_к_xml_или_директории>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if os.path.isfile(path):
        # Валидация одного файла
        is_valid, errors = validate_cpg_xml(path)
        
        if is_valid:
            print(f"✅ Файл {path} валидный")
        else:
            print(f"❌ Файл {path} содержит ошибки:")
            for error in errors:
                print(f"   - {error}")
    
    elif os.path.isdir(path):
        # Валидация директории
        results = validate_directory(path)
        
        valid_count = sum(1 for _, (is_valid, _) in results.items() if is_valid)
        total_count = len(results)
        
        print(f"\n=== Результаты валидации ===")
        print(f"Всего файлов: {total_count}")
        print(f"Валидных: {valid_count}")
        print(f"С ошибками: {total_count - valid_count}")
        
        # Выводим ошибки
        for file_path, (is_valid, errors) in results.items():
            if not is_valid:
                print(f"\n❌ {file_path}:")
                for error in errors:
                    print(f"   - {error}")
    
    else:
        print(f"Путь {path} не существует")
        sys.exit(1)


if __name__ == "__main__":
    main()