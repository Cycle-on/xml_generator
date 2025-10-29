"""
Тестовый скрипт для отправки ПИТВ сообщений на сервер приема
"""
import requests
import time
import xml.etree.ElementTree as ET
from datetime import datetime


def create_test_message(message_type: str, id_112: str = None) -> str:
    """Создать тестовое сообщение в формате SOAP/XML"""
    
    if not id_112:
        id_112 = f"test-{int(time.time())}"
    
    timestamp = datetime.now().isoformat()
    
    messages = {
        'UpdateCardResponse': f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
               xmlns:tns="http://system112.ru/112/integration">
    <soap:Body>
        <tns:UpdateCardResponse>
            <tns:Id112>{id_112}</tns:Id112>
            <tns:Code>200</tns:Code>
        </tns:UpdateCardResponse>
    </soap:Body>
</soap:Envelope>""",

        'AddReactionNotification': f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://system112.ru/112/integration">
    <soap:Body>
        <tns:AddReaction>
            <tns:SysCode>tspg</tns:SysCode>
            <tns:Id112>{id_112}</tns:Id112>
            <tns:UnitName></tns:UnitName>
            <tns:UnitMembership></tns:UnitMembership>
            <tns:ActionType>Notification</tns:ActionType>
            <tns:Remark></tns:Remark>
            <tns:ReactOperator>
                <tns:OperatorLogin>test_operator</tns:OperatorLogin>
                <tns:OperatorPost>Диспетчер</tns:OperatorPost>
                <tns:OperatorInfo></tns:OperatorInfo>
                <tns:OperatorDN>+7-123-456-78-90</tns:OperatorDN>
                <tns:OperatorWorkplace>Рабочее место 1</tns:OperatorWorkplace>
                <tns:OperatorName>Тестовый Оператор</tns:OperatorName>
            </tns:ReactOperator>
            <tns:ActionTimeIsoStr>{timestamp}</tns:ActionTimeIsoStr>
            <tns:DdsType>FireFighter</tns:DdsType>
            <tns:ExtId>test-ext-{int(time.time())}</tns:ExtId>
        </tns:AddReaction>
    </soap:Body>
</soap:Envelope>""",

        'AddReactionDeparture': f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://system112.ru/112/integration">
    <soap:Body>
        <tns:AddReaction>
            <tns:SysCode>tspg</tns:SysCode>
            <tns:Id112>{id_112}</tns:Id112>
            <tns:UnitName>ПСЧ-1 ФГКУ "1 ОФПС по г. Москве"</tns:UnitName>
            <tns:UnitMembership>1 АЦ-5, 1 АЛ-30, личный состав – 6 чел.</tns:UnitMembership>
            <tns:ActionType>Departure</tns:ActionType>
            <tns:Remark></tns:Remark>
            <tns:ReactOperator>
                <tns:OperatorLogin>dispatcher_01</tns:OperatorLogin>
                <tns:OperatorPost>Старший диспетчер</tns:OperatorPost>
                <tns:OperatorInfo></tns:OperatorInfo>
                <tns:OperatorDN>+7-495-123-45-67</tns:OperatorDN>
                <tns:OperatorWorkplace>ЦУС-1</tns:OperatorWorkplace>
                <tns:OperatorName>Иванов И.И.</tns:OperatorName>
            </tns:ReactOperator>
            <tns:ActionTimeIsoStr>{timestamp}</tns:ActionTimeIsoStr>
            <tns:DdsType>FireFighter</tns:DdsType>
            <tns:ExtId>departure-ext-{int(time.time())}</tns:ExtId>
        </tns:AddReaction>
    </soap:Body>
</soap:Envelope>""",

        'CancelCard': f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://system112.ru/112/integration">
    <soap:Body>
        <tns:CancelCard>
            <tns:SysCode>tspg</tns:SysCode>
            <tns:Id112>{id_112}</tns:Id112>
            <tns:Reason>Ошибочный</tns:Reason>
            <tns:CancelOperator>
                <tns:OperatorLogin>operator_cancel</tns:OperatorLogin>
                <tns:OperatorPost>Диспетчер</tns:OperatorPost>
                <tns:OperatorInfo></tns:OperatorInfo>
                <tns:OperatorDN>+7-495-987-65-43</tns:OperatorDN>
                <tns:OperatorWorkplace>ЦУС-2</tns:OperatorWorkplace>
                <tns:OperatorName>Петров П.П.</tns:OperatorName>
            </tns:CancelOperator>
            <tns:ExtId>cancel-ext-{int(time.time())}</tns:ExtId>
        </tns:CancelCard>
    </soap:Body>
</soap:Envelope>""",

        'FinishReaction': f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://system112.ru/112/integration">
    <soap:Body>
        <tns:FinishReaction>
            <tns:SysCode>tspg</tns:SysCode>
            <tns:Id112>{id_112}</tns:Id112>
            <tns:FinishOperator>
                <tns:OperatorLogin>finish_operator</tns:OperatorLogin>
                <tns:OperatorPost>Начальник караула</tns:OperatorPost>
                <tns:OperatorInfo></tns:OperatorInfo>
                <tns:OperatorDN>+7-495-555-55-55</tns:OperatorDN>
                <tns:OperatorWorkplace>ПСЧ-1</tns:OperatorWorkplace>
                <tns:OperatorName>Сидоров С.С.</tns:OperatorName>
            </tns:FinishOperator>
            <tns:DdsType>FireFighter</tns:DdsType>
            <tns:ExtId>finish-ext-{int(time.time())}</tns:ExtId>
        </tns:FinishReaction>
    </soap:Body>
</soap:Envelope>""",

        'CloseCardResponse': f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://system112.ru/112/integration">
    <soap:Body>
        <tns:CloseCardResponse>
            <tns:Code>200</tns:Code>
            <tns:CodeDescr>Карточка успешно закрыта</tns:CodeDescr>
        </tns:CloseCardResponse>
    </soap:Body>
</soap:Envelope>"""
    }
    
    return messages.get(message_type, messages['UpdateCardResponse'])


def send_message(url: str, message_type: str, id_112: str = None) -> dict:
    """Отправить тестовое сообщение"""
    try:
        xml_content = create_test_message(message_type, id_112)
        
        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': f'"{message_type}"',
            'User-Agent': 'PITV-Test-Client/1.0'
        }
        
        print(f"Отправка сообщения {message_type} на {url}")
        print(f"ID карточки: {id_112 or 'auto-generated'}")
        
        response = requests.post(url, data=xml_content, headers=headers, timeout=10)
        
        result = {
            'success': response.status_code == 200,
            'status_code': response.status_code,
            'response_text': response.text,
            'message_type': message_type,
            'id_112': id_112
        }
        
        if result['success']:
            print(f"✓ Сообщение {message_type} отправлено успешно")
        else:
            print(f"✗ Ошибка отправки {message_type}: {response.status_code}")
            print(f"Ответ: {response.text}")
        
        return result
        
    except Exception as e:
        print(f"✗ Исключение при отправке {message_type}: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'message_type': message_type,
            'id_112': id_112
        }


def test_all_message_types(base_url: str = "http://localhost:8081"):
    """Тестировать все типы сообщений ПИТВ"""
    print("=== ТЕСТИРОВАНИЕ СИСТЕМЫ ПРИЕМА ПИТВ СООБЩЕНИЙ ===\n")
    
    # Проверяем доступность сервера
    try:
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            print("✓ Сервер приема сообщений доступен")
            server_info = health_response.json()
            print(f"  Сервис: {server_info.get('service', 'Unknown')}")
            print(f"  Статус: {server_info.get('status', 'Unknown')}")
            print(f"  Порт: {server_info.get('port', 'Unknown')}")
        else:
            print(f"✗ Сервер недоступен: {health_response.status_code}")
            return
    except Exception as e:
        print(f"✗ Не удалось подключиться к серверу: {str(e)}")
        return
    
    print()
    
    # URL для отправки сообщений - ПРОСТО КОРЕНЬ БЕЗ ЭНДПОИНТОВ!
    message_url = f"{base_url}/"
    
    # Генерируем общий ID карточки для связанных сообщений
    card_id = f"TEST-CARD-{int(time.time())}"
    
    # Список сообщений для тестирования
    test_messages = [
        ('UpdateCardResponse', card_id),
        ('AddReactionNotification', card_id),
        ('AddReactionDeparture', card_id),
        ('CancelCard', card_id),
        ('FinishReaction', card_id),
        ('CloseCardResponse', card_id)
    ]
    
    results = []
    
    for message_type, test_card_id in test_messages:
        print(f"\n--- Тестирование {message_type} ---")
        result = send_message(message_url, message_type, test_card_id)
        results.append(result)
        time.sleep(1)  # Пауза между отправками
    
    # Отчет о результатах
    print("\n=== РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ ===")
    successful = sum(1 for r in results if r.get('success', False))
    total = len(results)
    
    print(f"Всего отправлено: {total}")
    print(f"Успешно: {successful}")
    print(f"Ошибок: {total - successful}")
    
    if successful < total:
        print("\nОшибки:")
        for result in results:
            if not result.get('success', False):
                print(f"  - {result['message_type']}: {result.get('error', result.get('status_code', 'Unknown error'))}")
    
    print(f"\nВсе сообщения отправлены с ID карточки: {card_id}")
    print("Проверьте веб-интерфейс на порту 8080, вкладка 'Прием сообщений'")


def test_single_message(message_type: str, base_url: str = "http://localhost:8081"):
    """Тестировать один тип сообщения"""
    print(f"=== ТЕСТИРОВАНИЕ {message_type.upper()} ===\n")
    
    message_url = f"{base_url}/"  # ПРОСТО КОРЕНЬ!
    card_id = f"SINGLE-TEST-{int(time.time())}"
    
    result = send_message(message_url, message_type, card_id)
    
    if result.get('success', False):
        print(f"\n✓ Тест {message_type} прошел успешно")
    else:
        print(f"\n✗ Тест {message_type} провален")
        print(f"Ошибка: {result.get('error', result.get('status_code', 'Unknown'))}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        message_type = sys.argv[1]
        if message_type in ['UpdateCardResponse', 'AddReactionNotification', 'AddReactionDeparture', 
                           'CancelCard', 'FinishReaction', 'CloseCardResponse']:
            test_single_message(message_type)
        else:
            print(f"Неизвестный тип сообщения: {message_type}")
            print("Доступные типы: UpdateCardResponse, AddReactionNotification, AddReactionDeparture, CancelCard, FinishReaction, CloseCardResponse")
    else:
        test_all_message_types()