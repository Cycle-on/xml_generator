"""
Система журналирования сообщений ПИТВ
"""
import json
import os
import threading
from datetime import datetime
from typing import List, Dict, Any, Optional
from models.pitv_models import MessageLogEntry


class MessageLogger:
    """Класс для управления журналом сообщений"""
    
    def __init__(self, log_file: str = "data/message_log.json"):
        self.log_file = log_file
        self.lock = threading.Lock()
        self._ensure_log_file_exists()
        
        # Callback для уведомления о новых сообщениях
        self.callbacks = []
    
    def _ensure_log_file_exists(self):
        """Убедиться что файл журнала существует"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def add_message(self, entry: MessageLogEntry) -> bool:
        """Добавить сообщение в журнал"""
        try:
            with self.lock:
                # Читаем существующие записи
                messages = self._read_messages()
                
                # Добавляем новую запись
                messages.append(entry.to_dict())
                
                # Сохраняем обратно
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    json.dump(messages, f, ensure_ascii=False, indent=2)
                
                # Уведомляем подписчиков
                self._notify_callbacks(entry)
                
                print(f"[MessageLogger] Добавлено сообщение: {entry.message_type} (ID: {entry.id_112})")
                return True
                
        except Exception as e:
            print(f"[MessageLogger] Ошибка при добавлении сообщения: {e}")
            return False
    
    def get_messages(self, limit: int = 100, message_type: str = None, 
                    id_112: str = None) -> List[Dict[str, Any]]:
        """Получить сообщения из журнала с фильтрацией"""
        try:
            with self.lock:
                messages = self._read_messages()
                
                # Фильтрация
                if message_type:
                    messages = [m for m in messages if m.get('message_type') == message_type]
                
                if id_112:
                    messages = [m for m in messages if m.get('id_112') == id_112]
                
                # Сортировка по времени (новые первыми)
                messages.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
                
                return messages[:limit]
                
        except Exception as e:
            print(f"[MessageLogger] Ошибка при чтении сообщений: {e}")
            return []
    
    def get_recent_messages(self, minutes: int = 60) -> List[Dict[str, Any]]:
        """Получить сообщения за последние N минут"""
        from datetime import timedelta
        
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        cutoff_str = cutoff_time.isoformat()
        
        messages = self.get_messages(limit=1000)
        return [m for m in messages if m.get('timestamp', '') >= cutoff_str]
    
    def clear_messages(self) -> bool:
        """Очистить журнал сообщений"""
        try:
            with self.lock:
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                
                print("[MessageLogger] Журнал сообщений очищен")
                return True
                
        except Exception as e:
            print(f"[MessageLogger] Ошибка при очистке журнала: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получить статистику по сообщениям"""
        try:
            messages = self.get_messages(limit=10000)
            
            stats = {
                "total_messages": len(messages),
                "by_type": {},
                "by_status": {},
                "recent_24h": 0,
                "last_message_time": None
            }
            
            # Статистика за последние 24 часа
            from datetime import timedelta
            cutoff_24h = datetime.now() - timedelta(hours=24)
            cutoff_24h_str = cutoff_24h.isoformat()
            
            for msg in messages:
                # По типам
                msg_type = msg.get('message_type', 'unknown')
                stats['by_type'][msg_type] = stats['by_type'].get(msg_type, 0) + 1
                
                # По статусам
                status = msg.get('status', 'unknown')
                stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
                
                # За 24 часа
                if msg.get('timestamp', '') >= cutoff_24h_str:
                    stats['recent_24h'] += 1
            
            # Время последнего сообщения
            if messages:
                stats['last_message_time'] = messages[0].get('timestamp')
            
            return stats
            
        except Exception as e:
            print(f"[MessageLogger] Ошибка при получении статистики: {e}")
            return {"error": str(e)}
    
    def _read_messages(self) -> List[Dict[str, Any]]:
        """Прочитать сообщения из файла"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def add_callback(self, callback):
        """Добавить callback для уведомления о новых сообщениях"""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback):
        """Удалить callback"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def _notify_callbacks(self, entry: MessageLogEntry):
        """Уведомить всех подписчиков о новом сообщении"""
        for callback in self.callbacks:
            try:
                callback(entry.to_dict())
            except Exception as e:
                print(f"[MessageLogger] Ошибка в callback: {e}")


# Глобальный экземпляр логгера
message_logger = MessageLogger()