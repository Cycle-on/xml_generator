"""
Генератор карточек для системы ЦПГ
Использует существующую логику генерации ЦССИ с конвертацией в формат ЦПГ
"""
from typing import Tuple, Optional
from datetime import datetime

from generators.ukio_generator import generate_ukio_phone_call_data
from converters.ukio_to_cpg import convert_ukio_to_cpg
from schemas.cpg_models import CPGCard, CPGIer
from schemas.phonecall import MissedCall


def generate_cpg_card_data(call_date: datetime) -> Tuple[Optional[CPGCard], Optional[CPGIer]]:
    """
    Генерирует данные карточки ЦПГ используя логику ЦССИ
    
    Args:
        call_date: Дата и время вызова
        
    Returns:
        Tuple[CPGCard, CPGIer]: Карточка и обращение в формате ЦПГ
    """
    # Используем существующий генератор ЦССИ
    ukio_or_missed = generate_ukio_phone_call_data(call_date)
    
    # Проверяем что получили
    if ukio_or_missed is None:
        print("Не удалось сгенерировать данные (нет свободных операторов)")
        return None, None
    
    # Если это пропущенный вызов, пока пропускаем
    # TODO: В будущем можно добавить поддержку пропущенных вызовов в ЦПГ
    if isinstance(ukio_or_missed, MissedCall):
        print("Пропущенный вызов - пропускаем для ЦПГ")
        return None, None
    
    # Конвертируем Ukio в формат ЦПГ
    card, ier = convert_ukio_to_cpg(ukio_or_missed)
    
    if not card:
        print("Не удалось конвертировать Ukio в Card")
        return None, None
    
    if not ier:
        print("Не удалось конвертировать Ukio в Ier")
        return None, None
    
    return card, ier


def generate_cpg_card_data_batch(start_date: datetime, count: int) -> list[Tuple[CPGCard, CPGIer]]:
    """
    Генерирует пакет карточек ЦПГ
    
    Args:
        start_date: Начальная дата генерации
        count: Количество карточек для генерации
        
    Returns:
        list: Список кортежей (Card, Ier)
    """
    from datetime import timedelta
    from constants import ALL_PROJ_CONSTANTS
    
    results = []
    current_date = start_date
    
    for i in range(count):
        # Генерируем карточку
        card, ier = generate_cpg_card_data(current_date)
        
        if card and ier:
            results.append((card, ier))
        
        # Сдвигаем время для следующей карточки
        delay_seconds = ALL_PROJ_CONSTANTS.get("AVG_DELAY_BETWEEN_CALLS_TIME", 180)
        current_date += timedelta(seconds=delay_seconds)
    
    return results