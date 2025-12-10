"""
Сервер приема сообщений ПИТВ на порту 8081
"""
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from flask import Flask, request, Response, jsonify
from werkzeug.serving import make_server
import threading
import signal
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.pitv_models import (
    MessageLogEntry, UpdateCardResponse, AddReactionNotification, 
    AddReactionDeparture, CancelCard, UpdateCardRequest, 
    FinishReaction, CloseCardResponse, Operator, DdsData01,
    get_message_display_name
)
from message_logger import message_logger

app = Flask(__name__)

# Глобальные переменные для управления сервером
server_instance = None
server_thread = None
is_running = False
error_mode_enabled = False  # Режим эмуляции ошибок


def parse_soap_xml(xml_content: str) -> dict:
    """Базовый парсер SOAP/XML сообщений"""
    try:
        # Убираем BOM если есть
        if xml_content.startswith('\ufeff'):
            xml_content = xml_content[1:]
        
        root = ET.fromstring(xml_content)
        
        # Определяем namespace
        namespaces = {
            'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
            'tns': 'http://system112.ru/112/integration'
        }
        
        # Ищем тело сообщения
        body = root.find('.//soap:Body', namespaces)
        if body is not None:
            # Получаем первый элемент в Body
            message_element = body[0] if len(body) > 0 else None
            if message_element is not None:
                return {
                    'message_type': message_element.tag.split('}')[-1],  # Убираем namespace
                    'raw_xml': xml_content,
                    'parsed_data': element_to_dict(message_element)
                }
        
        return {
            'message_type': 'unknown',
            'raw_xml': xml_content,
            'parsed_data': {}
        }
        
    except ET.ParseError as e:
        return {
            'message_type': 'parse_error',
            'raw_xml': xml_content,
            'error': str(e)
        }


def element_to_dict(element):
    """Конвертировать XML элемент в словарь"""
    result = {}
    
    # Атрибуты
    if element.attrib:
        result.update(element.attrib)
    
    # Дочерние элементы
    for child in element:
        child_data = element_to_dict(child)
        tag_name = child.tag.split('}')[-1]  # Убираем namespace
        
        if tag_name in result:
            # Если уже есть элемент с таким именем, делаем список
            if not isinstance(result[tag_name], list):
                result[tag_name] = [result[tag_name]]
            result[tag_name].append(child_data)
        else:
            result[tag_name] = child_data
    
    # Текст элемента
    if element.text and element.text.strip():
        if result:
            result['_text'] = element.text.strip()
        else:
            return element.text.strip()
    
    return result


def extract_id_112(parsed_data: dict) -> str:
    """Извлечь ID карточки 112 из данных"""
    # Ищем различные варианты поля ID
    possible_fields = ['id112', 'Id112', 'id_112', 'cardId', 'Id']
    
    def search_recursive(data, fields):
        if isinstance(data, dict):
            for field in fields:
                if field in data:
                    return str(data[field])
            
            # Рекурсивный поиск
            for value in data.values():
                result = search_recursive(value, fields)
                if result:
                    return result
        
        return None
    
    return search_recursive(parsed_data, possible_fields) or "unknown"


def create_success_response(message_type: str = None) -> str:
    """Создать успешный ответ в формате SOAP"""
    if message_type and "Request" in message_type:
        # Для Request сообщений отвечаем Response
        response_type = message_type.replace("Request", "Response")
        return f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <{response_type}>
            <Code>200</Code>
            <CodeDescr>Успешно обработано</CodeDescr>
        </{response_type}>
    </soap:Body>
</soap:Envelope>"""
    
    # Стандартный ответ
    return """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <Response>
            <Code>200</Code>
            <CodeDescr>Сообщение получено и обработано</CodeDescr>
        </Response>
    </soap:Body>
</soap:Envelope>"""


@app.route('/health', methods=['GET'])
def health_check():
    """Проверка работоспособности сервера"""
    return jsonify({
        "status": "running",
        "service": "PITV Message Receiver",
        "port": 8081,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/', methods=['POST'])
def receive_pitv_message():
    """Основной эндпоинт для приема всех ПИТВ сообщений на корневой путь"""
    global error_mode_enabled
    
    try:
        # Проверяем режим ошибок
        if error_mode_enabled:
            print("[PITV Receiver] РЕЖИМ ОШИБКИ ВКЛЮЧЕН - возвращаем 500")
            error_response = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <soap:Fault>
            <faultcode>Server</faultcode>
            <faultstring>Эмуляция ошибки сервера</faultstring>
            <detail>
                <ErrorCode>500</ErrorCode>
                <ErrorDescription>Сервер временно недоступен (режим эмуляции ошибок)</ErrorDescription>
            </detail>
        </soap:Fault>
    </soap:Body>
</soap:Envelope>"""
            return Response(error_response, mimetype="text/xml", status=500)
        
        # Получаем данные
        content_type = request.content_type or "text/xml"
        xml_content = request.get_data(as_text=True)
        source_ip = request.remote_addr
        
        print(f"[PITV Receiver] Получено сообщение от {source_ip}")
        print(f"[PITV Receiver] Content-Type: {content_type}")
        print(f"[PITV Receiver] XML (первые 500 символов): {xml_content[:500]}")
        
        # Парсим XML
        parsed = parse_soap_xml(xml_content)
        message_type = parsed.get('message_type', 'unknown')
        id_112 = extract_id_112(parsed.get('parsed_data', {}))
        
        print(f"[PITV Receiver] Тип сообщения: {message_type}, ID: {id_112}")
        
        # Создаем запись в журнале
        log_entry = MessageLogEntry.create(
            message_type=message_type,
            data=parsed,
            id_112=id_112,
            status="received",
            source_ip=source_ip
        )
        
        # Сохраняем в журнал
        success = message_logger.add_message(log_entry)
        
        if success:
            print(f"[PITV Receiver] Сообщение сохранено в журнал")
            # Возвращаем успешный ответ
            response_xml = create_success_response(message_type)
            return Response(response_xml, mimetype="text/xml", status=200)
        else:
            print(f"[PITV Receiver] Ошибка сохранения в журнал")
            return Response("Ошибка сохранения", status=500)
            
    except Exception as e:
        print(f"[PITV Receiver] Ошибка обработки сообщения: {e}")
        
        # Сохраняем ошибку в журнал
        error_entry = MessageLogEntry.create(
            message_type="error",
            data={"error": str(e), "raw_content": xml_content if 'xml_content' in locals() else ""},
            status="error",
            source_ip=request.remote_addr,
            error_message=str(e)
        )
        message_logger.add_message(error_entry)
        
        return Response("Ошибка обработки сообщения", status=500)


# Дополнительные маршруты для совместимости (на случай если кто-то шлет с эндпоинтами)
@app.route('/pitv/receive', methods=['POST'])
@app.route('/pitv/update-card-response', methods=['POST'])
@app.route('/pitv/add-reaction', methods=['POST'])  
@app.route('/pitv/cancel-card', methods=['POST'])
@app.route('/pitv/update-card-request', methods=['POST'])
@app.route('/pitv/finish-reaction', methods=['POST'])
@app.route('/pitv/close-card-response', methods=['POST'])
def receive_pitv_with_endpoints():
    """Все эндпоинты ведут на основную функцию приема"""
    return receive_pitv_message()


# API для интеграции с основным приложением
@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Получить сообщения из журнала"""
    try:
        limit = int(request.args.get('limit', 100))
        message_type = request.args.get('type')
        id_112 = request.args.get('id_112')
        
        messages = message_logger.get_messages(
            limit=limit,
            message_type=message_type,
            id_112=id_112
        )
        
        return jsonify({
            "success": True,
            "messages": messages,
            "count": len(messages)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/messages/clear', methods=['POST'])
def clear_messages():
    """Очистить журнал сообщений"""
    try:
        success = message_logger.clear_messages()
        return jsonify({
            "success": success,
            "message": "Журнал очищен" if success else "Ошибка очистки"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Получить статистику сообщений"""
    try:
        stats = message_logger.get_statistics()
        return jsonify({
            "success": True,
            "statistics": stats
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/error-mode', methods=['GET'])
def get_error_mode():
    """Получить текущий режим ошибок"""
    global error_mode_enabled
    return jsonify({
        "success": True,
        "error_mode_enabled": error_mode_enabled
    })


@app.route('/api/error-mode', methods=['POST'])
def set_error_mode():
    """Установить режим ошибок"""
    global error_mode_enabled
    try:
        data = request.get_json()
        error_mode_enabled = data.get('enabled', False)
        
        print(f"[PITV Receiver] Режим ошибок: {'ВКЛЮЧЕН' if error_mode_enabled else 'ВЫКЛЮЧЕН'}")
        
        return jsonify({
            "success": True,
            "error_mode_enabled": error_mode_enabled
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def start_message_receiver_server():
    """Запустить сервер приема сообщений"""
    global server_instance, server_thread, is_running
    
    if is_running:
        print("[PITV Receiver] Сервер уже запущен")
        return True
    
    try:
        # Создаем сервер
        server_instance = make_server('0.0.0.0', 8081, app, threaded=True)
        
        def run_server():
            global is_running
            is_running = True
            print("[PITV Receiver] Сервер запущен на порту 8081")
            print("[PITV Receiver] СЛУШАЕТ ПРОСТО ПОРТ - НИКАКИХ ЭНДПОИНТОВ НЕ НУЖНО!")
            print("  ✅ POST http://localhost:8081/ - ОСНОВНОЙ ПРИЕМ СООБЩЕНИЙ")
            print("  ✅ GET  http://localhost:8081/health - проверка работоспособности")
            print("  📝 Дополнительные эндпоинты тоже работают для совместимости")
            print("  🔥 ПРОСТО ШЛИТЕ XML НА ПОРТ 8081 БЕЗ ВСЯКИХ ПУТЕЙ!")
            
            server_instance.serve_forever()
        
        # Запускаем в отдельном потоке
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        return True
        
    except Exception as e:
        print(f"[PITV Receiver] Ошибка запуска сервера: {e}")
        return False


def stop_message_receiver_server():
    """Остановить сервер приема сообщений"""
    global server_instance, is_running
    
    if server_instance and is_running:
        print("[PITV Receiver] Остановка сервера...")
        server_instance.shutdown()
        is_running = False
        print("[PITV Receiver] Сервер остановлен")


def signal_handler(sig, frame):
    """Обработчик сигналов для корректного завершения"""
    print('\n[PITV Receiver] Получен сигнал завершения')
    stop_message_receiver_server()
    sys.exit(0)


if __name__ == "__main__":
    # Регистрируем обработчик сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Запускаем сервер
    if start_message_receiver_server():
        print("[PITV Receiver] Сервер работает. Нажмите Ctrl+C для остановки.")
        
        # Ждем завершения
        try:
            while is_running:
                threading.Event().wait(1)
        except KeyboardInterrupt:
            signal_handler(signal.SIGINT, None)
    else:
        print("[PITV Receiver] Не удалось запустить сервер")
        sys.exit(1)