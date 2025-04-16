from flask import Flask, render_template, Response, jsonify, stream_with_context, request
import io
import sys
import os
import base64
import requests
import xml.etree.ElementTree as ET
from main import main
from threading import Thread
import time
from datetime import datetime
import json

app = Flask(__name__, template_folder='web_service/templates')

# Путь к директории с файлами
FILES_DIR = os.path.join('files', 'TEST')

# Глобальные переменные для управления автоматической генерацией
auto_generation_thread = None
auto_generation_running = False
auto_generation_start_time = None
auto_generation_end_time = None
auto_generation_interval = None
total_files_sent = 0
log_callbacks = []

class OutputCapture:
    def __init__(self):
        self.output = io.StringIO()
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.callbacks = []

    def write(self, text):
        self.output.write(text)
        self.stdout.write(text)  # Сохраняем вывод в консоль
        for callback in self.callbacks:
            callback(text)

    def flush(self):
        self.stdout.flush()

    def get_output(self):
        return self.output.getvalue()

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def remove_callback(self, callback):
        if callback in self.callbacks:
            self.callbacks.remove(callback)

def get_ukios_files():
    files = []
    base_path = os.path.join('files', 'TEST')
    
    # Проверяем существование базовой директории
    if not os.path.exists(base_path):
        return files
        
    # Перебираем все регионы
    for region in os.listdir(base_path):
        region_path = os.path.join(base_path, region, 'Ukios')
        if os.path.exists(region_path):
            # Добавляем все XML файлы из директории Ukios
            for file in os.listdir(region_path):
                if file.endswith('.xml'):
                    files.append(f"{region}/Ukios/{file}")
    
    return sorted(files)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate():
    def generate_output():
        capture = OutputCapture()
        sys.stdout = capture
        sys.stderr = capture
        
        def output_callback(text):
            yield f"data: {text}\n\n"
        
        capture.add_callback(output_callback)
        
        try:
            main()
        except Exception as e:
            yield f"data: Ошибка: {str(e)}\n\n"
        finally:
            sys.stdout = capture.stdout
            sys.stderr = capture.stderr
            capture.remove_callback(output_callback)
            yield "event: done\ndata: \n\n"
    
    return Response(stream_with_context(generate_output()), 
                   mimetype='text/event-stream',
                   headers={
                       'Cache-Control': 'no-cache',
                       'Connection': 'keep-alive',
                       'X-Accel-Buffering': 'no'
                   })

@app.route('/files')
def list_files():
    return jsonify(get_ukios_files())

@app.route('/file/<path:filename>')
def get_file(filename):
    try:
        file_path = os.path.join('files', 'TEST', filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return Response(content, mimetype='text/xml')
        else:
            return "Файл не найден", 404
    except Exception as e:
        return f"Ошибка при чтении файла: {str(e)}", 500

@app.route('/test-server', methods=['POST'])
def test_server():
    success_response = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ens="http://system112.ru/112/integration.wsdl" xmlns:ins="http://system112.ru/112/integration" xmlns:jxb="http://java.sun.com/xml/ns/jaxb">
<soap:Body>
<ins:card112ChangedResponse xmlns:ins="http://system112.ru/112/integration" xmlns="http://system112.ru/112/integration">
<ins:errorCode>0</ins:errorCode>
</ins:card112ChangedResponse>
</soap:Body>
</soap:Envelope>'''
    return success_response, 200, {'Content-Type': 'text/xml;charset=UTF-8'}

@app.route('/api/send', methods=['POST'])
def send_file():
    try:
        data = request.get_json()
        url = data.get('url')
        username = data.get('username')
        password = data.get('password')
        filename = data.get('file')

        if not all([url, username, password, filename]):
            return jsonify({
                'success': False,
                'message': 'Ошибка: не все параметры предоставлены'
            }), 400

        # Читаем содержимое файла
        file_path = os.path.join('files', 'TEST', filename)
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'message': f'Ошибка: файл {filename} не найден'
            }), 404

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Исправляем префикс XML
            content = content.replace('<?сбитый префикс для ukio', '<?xml')

        # Отправляем запрос
        headers = {
            'Content-Type': 'text/xml;charset=UTF-8',
            'Authorization': f'Basic {base64.b64encode(f"{username}:{password}".encode()).decode()}'
        }
        
        try:
            response = requests.post(
                url,
                data=content,
                headers=headers,
                timeout=30
            )
            
            # Проверяем ответ
            if response.status_code == 200:
                try:
                    # Пробуем распарсить как XML
                    root = ET.fromstring(response.text)
                    error_code = root.find('.//ins:errorCode', {'ins': 'http://system112.ru/112/integration'})
                    
                    if error_code is not None and error_code.text == '0':
                        return jsonify({
                            'success': True,
                            'message': 'Файл успешно отправлен'
                        })
                    else:
                        return jsonify({
                            'success': False,
                            'message': 'Ошибка при отправке файла'
                        })
                except ET.ParseError:
                    return jsonify({
                        'success': False,
                        'message': 'Ошибка при отправке файла'
                    })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Ошибка при отправке файла'
                })

        except requests.exceptions.RequestException:
            return jsonify({
                'success': False,
                'message': 'Ошибка при отправке файла'
            })

    except Exception:
        return jsonify({
            'success': False,
            'message': 'Ошибка при отправке файла'
        }), 500

def capture_main_output():
    sys.stderr.write("DEBUG: Начало capture_main_output\n")
    capture = OutputCapture()
    sys.stdout = capture
    sys.stderr = capture
    
    def output_callback(text):
        # Пропускаем отладочные сообщения и пустые строки
        if not text.startswith("DEBUG:") and text.strip():
            sys.stderr.write(f"DEBUG: Получено сообщение: {text}\n")
            log_message({'type': 'console_output', 'text': text})
    
    capture.add_callback(output_callback)
    
    try:
        sys.stderr.write("DEBUG: Вызов main()\n")
        main()
        sys.stderr.write("DEBUG: main() завершен\n")
    except Exception as e:
        sys.stderr.write(f"DEBUG: Ошибка в main(): {str(e)}\n")
    finally:
        sys.stdout = capture.stdout
        sys.stderr = capture.stderr
        capture.remove_callback(output_callback)
        sys.stderr.write("DEBUG: Конец capture_main_output\n")

def add_log_callback(callback):
    log_callbacks.append(callback)

def remove_log_callback(callback):
    if callback in log_callbacks:
        log_callbacks.remove(callback)

def log_message(message):
    for callback in log_callbacks:
        callback(message)

@app.route('/api/auto-generate', methods=['POST'])
def start_auto_generation():
    global auto_generation_thread, auto_generation_running, auto_generation_start_time, auto_generation_end_time, auto_generation_interval, total_files_sent
    
    data = request.json
    interval = float(data.get('interval', 1))
    duration = float(data.get('duration', 10))
    url = data.get('url')
    username = data.get('username')
    password = data.get('password')
    
    if not all([url, username, password]):
        return jsonify({
            'success': False,
            'message': 'Ошибка: не все параметры предоставлены'
        })
    
    if auto_generation_running:
        return jsonify({
            'success': False,
            'message': 'Автоматическая генерация уже запущена'
        })
    
    auto_generation_running = True
    auto_generation_start_time = time.time()
    auto_generation_end_time = auto_generation_start_time + (duration * 60)
    auto_generation_interval = interval
    total_files_sent = 0
    
    auto_generation_thread = Thread(target=auto_generation_worker, args=(url, username, password))
    auto_generation_thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Автоматическая генерация запущена',
        'start_time': auto_generation_start_time,
        'end_time': auto_generation_end_time
    })

@app.route('/api/auto-generate/stop', methods=['POST'])
def stop_auto_generation():
    global auto_generation_running
    
    if not auto_generation_running:
        return jsonify({
            'success': False,
            'message': 'Автоматическая генерация не запущена'
        })
    
    auto_generation_running = False
    return jsonify({
        'success': True,
        'message': 'Автоматическая генерация остановлена'
    })

@app.route('/api/auto-generate/status', methods=['GET'])
def get_auto_generation_status():
    if not auto_generation_running:
        return jsonify({
            'running': False,
            'message': 'Автоматическая генерация не запущена'
        })
    
    time_left = max(0, auto_generation_end_time - time.time())
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)
    
    return jsonify({
        'running': True,
        'timeLeft': f"{minutes:02d}:{seconds:02d}",
        'filesSent': total_files_sent
    })

@app.route('/api/auto-generate/logs')
def auto_generate_logs():
    def generate_logs():
        last_message = None
        while True:
            if not auto_generation_running:
                break
            time.sleep(0.1)
            
            # Создаем словарь для хранения текущего состояния
            current_state = {
                'type': 'status_update',
                'files_sent': total_files_sent,
                'messages': []
            }
            
            # Добавляем сообщения в массив
            if last_message != total_files_sent:
                last_message = total_files_sent
                if total_files_sent > 0:
                    current_state['messages'].append({
                        'type': 'files_sent',
                        'count': total_files_sent
                    })
            
            # Отправляем обновленное состояние
            if current_state['messages']:
                yield f"data: {json.dumps(current_state)}\n\n"
    
    return Response(stream_with_context(generate_logs()), 
                   mimetype='text/event-stream',
                   headers={
                       'Cache-Control': 'no-cache',
                       'Connection': 'keep-alive',
                       'X-Accel-Buffering': 'no'
                   })

def auto_generation_worker(url, username, password):
    global auto_generation_running, total_files_sent
    total_files_sent = 0
    
    while auto_generation_running:
        try:
            # Начало генерации
            log_message({'type': 'generation_start'})
            
            # Генерируем файлы с перехватом вывода
            capture_main_output()
            
            # Получаем список файлов
            files = get_ukios_files()
            total_files = len(files)
            log_message({'type': 'files_found', 'count': total_files})
            
            # Отправляем файлы
            for i, filename in enumerate(files, 1):
                log_message({'type': 'sending_file', 'current': i, 'total': total_files})
                
                try:
                    with open(os.path.join('files', 'TEST', filename), 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    
                    # Исправляем префикс XML
                    file_content = file_content.replace('<?сбитый префикс для ukio', '<?xml')
                    
                    # Отправляем файл
                    response = requests.post(
                        url,
                        auth=(username, password),
                        data=file_content,
                        headers={'Content-Type': 'text/xml;charset=UTF-8'}
                    )
                    
                    if response.status_code == 200:
                        total_files_sent += 1
                        log_message({'type': 'file_sent', 'current': i, 'total': total_files})
                    else:
                        log_message({'type': 'error', 'message': f'Ошибка при отправке файла {filename}: {response.status_code}'})
                    
                except Exception as e:
                    log_message({'type': 'error', 'message': f'Ошибка при обработке файла {filename}: {str(e)}'})
            
            # Генерация завершена
            log_message({'type': 'generation_complete'})
            
            # Ожидание следующего цикла
            log_message({'type': 'waiting', 'seconds': 60})
            time.sleep(60)
            
        except Exception as e:
            log_message({'type': 'error', 'message': f'Ошибка в цикле генерации: {str(e)}'})
            time.sleep(60)

if __name__ == '__main__':
    app.run(debug=True) 