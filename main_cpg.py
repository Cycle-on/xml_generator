"""
Главный модуль для генерации файлов в формате ЦПГ
Параллельная реализация, не затрагивающая функционал ЦССИ
"""
import datetime
from datetime import timedelta as td

from constants import fill_constants

# Заполняем константы
fill_constants()

from config import load_config, ukios_info, missed_info
from config.dirs import clear_dir, create_dirs
from constants import ALL_PROJ_CONSTANTS
from constants.constants_remaker import get_next_constants
from csv_parser.parse_addresses import fill_addresses
from csv_parser.parse_incident_types import fill_incident_type_lists
from generators.operators_and_arms import (
    ARM_WORK,
    OPERATOR_WORK,
    create_arms_and_operators,
)
from generators.cpg_generator import generate_cpg_card_data
from file_creator_cpg import create_cpg_xml_file

config = load_config()


def generate_cpg_region_files(
    date_zero=None, 
    region_name: str = "rsc-region-05"
):
    """
    Генерация файлов для региона в формате ЦПГ
    Аналог generate_region_files из main.py, но для ЦПГ
    
    Args:
        date_zero: Начальная дата генерации
        region_name: Название региона
    """
    global ALL_PROJ_CONSTANTS
    
    # Очищаем списки операторов
    ARM_WORK.clear()
    OPERATOR_WORK.clear()
    ukios_info.clear()
    
    # Выводим информацию о параметрах генерации
    print("\n=== Генерация в режиме ЦПГ ===")
    print(f"Регион: {region_name}")
    print(f"Количество файлов: {ALL_PROJ_CONSTANTS.get('files_count', 1)}")
    print(f"XML на файл: {ALL_PROJ_CONSTANTS.get('xml_count_per_file', 10)}")
    print("\nЗначения переменных для создания карточек:")
    print(f"CARD_CREATE_LOW: {ALL_PROJ_CONSTANTS['CARD_CREATE_LOW']}")
    print(f"CARD_CREATE_HIGH: {ALL_PROJ_CONSTANTS['CARD_CREATE_HIGH']}")
    print(f"EOS_CARD_CREATE_LOW: {ALL_PROJ_CONSTANTS['EOS_CARD_CREATE_LOW']}")
    print(f"EOS_CARD_CREATE_HIGH: {ALL_PROJ_CONSTANTS['EOS_CARD_CREATE_HIGH']}")
    print(f"AVG_EOS_CARD_CREATE_TIME: {ALL_PROJ_CONSTANTS['AVG_EOS_CARD_CREATE_TIME']}")
    print("----------------------------------------\n")
    
    # Создаем директории
    create_dirs()
    
    # Создаем операторов и АРМы
    create_arms_and_operators()
    
    # Устанавливаем начальную дату
    if date_zero is None:
        date_zero = datetime.datetime.now() - td(hours=3)
    
    dt_start = datetime.datetime.now()
    
    # Заполняем типы инцидентов
    fill_incident_type_lists(region_name)
    print("Загружены типы инцидентов")
    
    # Загружаем адреса
    addresses = fill_addresses(region_name)
    if not addresses:
        print(f"Не найдены адреса в таблице для региона: {region_name}")
        return
    
    print(f"Загружено адресов: {len(addresses)}")
    
    # Счетчики для статистики
    generated_count = 0
    failed_count = 0
    
    # Генерируем файлы (по одной карточке на файл)
    total_cards = ALL_PROJ_CONSTANTS.get("files_count", 1) * ALL_PROJ_CONSTANTS.get("xml_count_per_file", 10)
    print(f"Будет сгенерировано {total_cards} отдельных файлов")
    
    file_counter = 0
    for i in range(ALL_PROJ_CONSTANTS.get("files_count", 1)):
        for j in range(ALL_PROJ_CONSTANTS.get("xml_count_per_file", 10)):
            # Генерируем карточку и обращение ЦПГ
            card, ier = generate_cpg_card_data(date_zero)
            
            # Сдвигаем время для следующего вызова
            date_zero += td(seconds=ALL_PROJ_CONSTANTS["AVG_DELAY_BETWEEN_CALLS_TIME"])
            
            if card and ier:
                # Сохраняем каждую карточку в отдельный файл
                try:
                    from file_creator_cpg import create_cpg_xml_file
                    
                    filename = f"card_{file_counter}"
                    file_path = create_cpg_xml_file(
                        card=card,
                        ier=ier,
                        filename=filename,
                        region_name=region_name,
                        operation="UpdateCard"
                    )
                    
                    if file_path:
                        ukios_info.append({
                            "filename": filename + ".xml",
                            "dt_send": card.Created,
                            "mode": "CPG"
                        })
                        generated_count += 1
                        if generated_count % 10 == 0:
                            print(f"Сгенерировано {generated_count}/{total_cards} файлов")
                except Exception as e:
                    print(f"Ошибка при создании XML файла {filename}: {e}")
                    failed_count += 1
            else:
                failed_count += 1
            
            file_counter += 1
    
    # Выводим статистику
    print(f"\n=== Статистика генерации ЦПГ ===")
    print(f"Успешно сгенерировано: {generated_count}")
    print(f"Неудачных попыток: {failed_count}")
    print(f"Время генерации: {datetime.datetime.now() - dt_start}")
    print("==============================\n")
    
    # Очистка
    if ALL_PROJ_CONSTANTS["TAKE_CONSTANTS_FROM_FILE"]:
        ALL_PROJ_CONSTANTS = {}
    ARM_WORK.clear()
    OPERATOR_WORK.clear()
    ukios_info.clear()


def main_cpg():
    """
    Главная функция для генерации файлов ЦПГ
    """
    print("\n" + "="*50)
    print("ЗАПУСК ГЕНЕРАТОРА В РЕЖИМЕ ЦПГ")
    print("="*50 + "\n")
    
    config.date_zero = datetime.datetime.now() - td(hours=3)
    
    # НЕ очищаем директории ЦССИ, создаем отдельные для ЦПГ
    # clear_dir() - не вызываем!
    
    if ALL_PROJ_CONSTANTS["TAKE_CONSTANTS_FROM_FILE"]:
        # Генерация с константами из файла
        generate_cpg_region_files(region_name="rsc-region-05")
    else:
        # Генерация с константами из таблиц
        for constants_dict in get_next_constants():
            ukios_info.clear()
            missed_info.clear()
            
            ALL_PROJ_CONSTANTS.update(constants_dict)
            
            # Преобразуем строки в списки если нужно
            for k, v in ALL_PROJ_CONSTANTS.items():
                if isinstance(v, str) and "[" in v:
                    ALL_PROJ_CONSTANTS[k] = eval(v)
            
            generate_cpg_region_files(
                region_name=constants_dict.get("region_name/constant name", "rsc-region-05")
            )
    
    print("\n" + "="*50)
    print("ГЕНЕРАЦИЯ ЦПГ ЗАВЕРШЕНА")
    print("="*50 + "\n")


if __name__ == "__main__":
    # Если запускаем напрямую этот файл
    main_cpg()