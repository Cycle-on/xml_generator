"""
Модели данных для сообщений ПИТВ (Протокол информационно-технологического взаимодействия)
"""
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime
import json


@dataclass
class Operator:
    """Структура оператора"""
    operator_login: Optional[str] = None
    operator_post: Optional[str] = None  
    operator_info: Optional[str] = None
    operator_dn: Optional[str] = None
    operator_workplace: Optional[str] = None
    operator_name: Optional[str] = None


@dataclass
class UpdateCardResponse:
    """1.0 Создание новой карточки - UpdateCardResponse"""
    id_112: str
    code: str  # HTTP код, 200 для успеха
    
    def __post_init__(self):
        self.message_type = "UpdateCardResponse"


@dataclass 
class AddReactionNotification:
    """1.1 Просмотр карточки - AddReaction (Notification)"""
    sys_code: str = "tspg"
    id_112: str = ""
    unit_name: Optional[str] = None
    unit_membership: Optional[str] = None
    action_type: str = "Notification"
    remark: Optional[str] = None
    react_operator: Optional[Operator] = None
    action_time_iso_str: Optional[str] = None
    dds_type: str = "FireFighter"
    ext_id: Optional[str] = None
    
    def __post_init__(self):
        self.message_type = "AddReaction_Notification"


@dataclass
class AddReactionDeparture:
    """1.3 Начало реагирования - AddReaction (Departure)"""
    sys_code: str = "tspg"
    id_112: str = ""
    unit_name: str = ""  # Наименование подразделения
    unit_membership: Optional[str] = None  # Состав сил и средств
    action_type: str = "Departure"
    remark: Optional[str] = None
    react_operator: Optional[Operator] = None
    action_time_iso_str: Optional[str] = None  # Время выезда
    dds_type: str = "FireFighter"
    ext_id: Optional[str] = None
    
    def __post_init__(self):
        self.message_type = "AddReaction_Departure"


@dataclass
class CancelCard:
    """1.2 Отмена вызова - CancelCard"""
    sys_code: str = "tspg"
    id_112: str = ""
    reason: str = "Ошибочный"
    cancel_operator: Optional[Operator] = None
    ext_id: Optional[str] = None
    
    def __post_init__(self):
        self.message_type = "CancelCard"


@dataclass
class DdsData01:
    """Структура DdsData01 для обновления карточки"""
    dds_type_str: Optional[str] = None  # Вид происшествия
    has_gas: Optional[bool] = None  # Объект газифицирован
    need_rescue: Optional[bool] = None  # Необходимость спасательных работ
    floor_count: Optional[int] = None  # Этажность
    fire_time: Optional[int] = None  # Время развития пожара
    fire_effects: Optional[str] = None  # Последствия пожара
    driveways_state: Optional[str] = None  # Подъездные пути
    working_conditions: Optional[str] = None  # Условия работы
    evacuation_possibility: Optional[str] = None  # Возможность эвакуации
    owners_and_tenants_info: Optional[str] = None  # Информация о собственниках
    last_change_operator_01: Optional[Operator] = None


@dataclass
class UpdateCardRequest:
    """1.4 Обновление карточки - UpdateCardRequest"""
    sys_code: str = "tspg"
    card: Optional[Dict[str, Any]] = None  # Структура УКИО
    ier: Optional[Dict[str, Any]] = None   # Структура вызов
    dds_data_01: Optional[DdsData01] = None
    
    def __post_init__(self):
        self.message_type = "UpdateCardRequest"


@dataclass
class FinishReaction:
    """1.5 Завершение мероприятий - FinishReaction"""
    sys_code: str = "tspg"
    id_112: str = ""
    finish_operator: Optional[Operator] = None
    dds_type: str = "FireFighter"
    ext_id: Optional[str] = None
    
    def __post_init__(self):
        self.message_type = "FinishReaction"


@dataclass
class CloseCardResponse:
    """1.6 Закрытие карточки - CloseCardResponse"""
    code: str  # HTTP код, 200 для успеха
    code_descr: Optional[str] = None
    
    def __post_init__(self):
        self.message_type = "CloseCardResponse"


@dataclass
class MessageLogEntry:
    """Запись в журнале сообщений"""
    timestamp: str
    message_type: str
    id_112: Optional[str] = None
    status: str = "received"  # received, processed, error
    source_ip: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    
    @classmethod
    def create(cls, message_type: str, data: Any, id_112: str = None, 
               status: str = "received", source_ip: str = None, error_message: str = None):
        """Создать запись в журнале"""
        return cls(
            timestamp=datetime.now().isoformat(),
            message_type=message_type,
            id_112=id_112,
            status=status,
            source_ip=source_ip,
            data=asdict(data) if hasattr(data, '__dataclass_fields__') else data,
            error_message=error_message
        )
    
    def to_dict(self):
        """Конвертировать в словарь"""
        return asdict(self)


def parse_message_from_xml(xml_content: str, content_type: str = None) -> Optional[Any]:
    """
    Парсинг сообщения из XML/SOAP
    В реальной реализации здесь будет парсинг XML
    """
    # Пока заглушка - в реальности нужно парсить XML
    return {"raw_xml": xml_content, "parsed": False}


def get_message_display_name(message_type: str) -> str:
    """Получить читаемое название типа сообщения"""
    display_names = {
        "UpdateCardResponse": "Создание карточки",
        "AddReaction_Notification": "Просмотр карточки", 
        "AddReaction_Departure": "Начало реагирования",
        "CancelCard": "Отмена вызова",
        "UpdateCardRequest": "Обновление карточки",
        "FinishReaction": "Завершение мероприятий",
        "CloseCardResponse": "Закрытие карточки"
    }
    return display_names.get(message_type, message_type)