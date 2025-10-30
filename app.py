import base64
import io
import os
import sys
import tracemalloc
import threading
import time
import queue
import json
import socket

import requests
from flask import (
    Flask,
    Response,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    stream_with_context,
    url_for,
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
)

tracemalloc.start()
from constants import fill_constants

fill_constants()
import json
import queue
import time
from threading import Thread

from dotenv import load_dotenv

from config import missed_info, ukios_info
from constants import *
from constants import ALL_PROJ_CONSTANTS
from constants.constants_remaker import get_next_constants
from main import clear_dir, generate_region_files, main

# Импорты для сервера приема сообщений
try:
    from message_receiver import start_message_receiver_server, stop_message_receiver_server, is_running as receiver_running
    from message_logger import message_logger
    PITV_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Не удалось загрузить модули ПИТВ: {e}")
    PITV_AVAILABLE = False

# Загружаем переменные окружения
load_dotenv()

# Константы для генерации
# TAKE_CONSTANTS_FROM_FILE = True  # Если True - берем константы из файла, если False - из get_next_constants()

app = Flask(__name__, template_folder="web_service/templates")
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# Путь к директории с файлами
FILES_DIR = os.path.join("files", "TEST")

# Глобальные переменные для управления автоматической генерацией ЦССИ
auto_generation_thread = None
auto_generation_running = False
auto_generation_start_time = None
auto_generation_end_time = None
auto_generation_interval = None
total_files_sent = 0
log_callbacks = []
is_generating = False

# Глобальные переменные для управления автоматической генерацией второй системы
cpg_auto_generation_thread = None
cpg_auto_generation_running = False
cpg_auto_generation_start_time = None
cpg_auto_generation_end_time = None
cpg_auto_generation_interval = None
cpg_total_files_sent = 0
cpg_log_callbacks = []
cpg_is_generating = False

# Глобальные переменные для ПИТВ
pitv_message_callbacks = []


# Получаем список логинов и паролей из .env
def get_credentials():
    credentials = []
    # Читаем .env файл напрямую, так как os.environ не поддерживает множественные значения
    try:
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("LOGIN_PASSWORD="):
                    login_password = line.split("=", 1)[1].strip()
                    if ":" in login_password:
                        login, password = login_password.split(":", 1)
                        credentials.append({"login": login, "password": password})
                        # print(f"Добавлена пара логин-пароль: {login}")
    except Exception as e:
        print(f"Ошибка при чтении .env файла: {str(e)}")

    print(f"Всего найдено пар логин-пароль: {len(credentials)}")
    return credentials


# Получаем список доступных регионов (логинов)
def get_available_regions():
    credentials = get_credentials()
    return [cred["login"] for cred in credentials]


# Получаем пароль для конкретного логина
def get_password_for_login(login):
    credentials = get_credentials()
    for cred in credentials:
        if cred["login"] == login:
            return cred["password"]
    return None


# Color formatting utilities
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_colored(text, color):
    print(f"{color}{text}{Colors.ENDC}")


def print_request_details(url, headers, data):
    print_colored("\n=== Request Details ===", Colors.HEADER)
    print_colored(f"URL: {url}", Colors.BLUE)
    print_colored("\nHeaders:", Colors.CYAN)
    for key, value in headers.items():
        if key.lower() == "authorization":
            # Mask the password in the Authorization header
            auth_parts = value.split(" ")
            if len(auth_parts) == 2 and auth_parts[0].lower() == "basic":
                try:
                    decoded = base64.b64decode(auth_parts[1]).decode()
                    username, _ = decoded.split(":")
                    print_colored(
                        f"{key}: Basic {base64.b64encode(f'{username}:******'.encode()).decode()}",
                        Colors.CYAN,
                    )
                except:
                    print_colored(f"{key}: {value}", Colors.CYAN)
            else:
                print_colored(f"{key}: {value}", Colors.CYAN)
        else:
            print_colored(f"{key}: {value}", Colors.CYAN)
    print_colored("\nRequest Body:", Colors.GREEN)
    print_colored(data, Colors.GREEN)


def print_response_details(response):
    print_colored("\n=== Response Details ===", Colors.HEADER)
    print_colored(f"Status Code: {response.status_code}", Colors.YELLOW)
    # print_colored("\nResponse Headers:", Colors.CYAN)
    for key, value in response.headers.items():
        print_colored(f"{key}: {value}", Colors.CYAN)
    # print_colored("\nResponse Body:", Colors.GREEN)
    # print_colored(response.text, Colors.GREEN)


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
    base_path = os.path.join("files", "TEST")

    # Проверяем существование базовой директории
    if not os.path.exists(base_path):
        return files

    # Перебираем все регионы
    for region in os.listdir(base_path):
        region_path = os.path.join(base_path, region, "Ukios")
        if os.path.exists(region_path):
            # Добавляем все XML файлы из директории Ukios
            for file in os.listdir(region_path):
                if file.endswith(".xml"):
                    files.append(f"{region}/Ukios/{file}")

    return sorted(files)


def get_cpg_files():
    """Получает список ЦПГ файлов"""
    files = []
    base_path = os.path.join("files", "TEST_cpg")

    # Проверяем существование базовой директории
    if not os.path.exists(base_path):
        return files

    # Перебираем все регионы
    for region in os.listdir(base_path):
        region_path = os.path.join(base_path, region, "UpdateCard")
        if os.path.exists(region_path):
            # Добавляем все XML файлы из директории UpdateCard
            for file in os.listdir(region_path):
                if file.endswith(".xml"):
                    files.append(f"{region}/UpdateCard/{file}")

    return sorted(files)


def get_cpg_regions():
    """Получает список ЦПГ регионов из .env"""
    credentials = []
    try:
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("CPG_LOGIN_PASSWORD="):
                    login_password = line.split("=", 1)[1].strip()
                    if ":" in login_password:
                        login, password = login_password.split(":", 1)
                        credentials.append({"login": login, "password": password})
    except Exception as e:
        print(f"Ошибка при чтении .env файла: {str(e)}")

    return [cred["login"] for cred in credentials]


def get_cpg_password_for_login(login):
    """Получает пароль для ЦПГ логина"""
    try:
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("CPG_LOGIN_PASSWORD="):
                    login_password = line.split("=", 1)[1].strip()
                    if ":" in login_password:
                        l, password = login_password.split(":", 1)
                        if l == login:
                            return password
    except Exception as e:
        print(f"Ошибка при чтении .env файла: {str(e)}")
    return None


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == os.getenv(
            "ADMIN_USERNAME", "xml-sender"
        ) and password == os.getenv("ADMIN_PASSWORD", "o7_5nDUJkp"):
            user = User(username)
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Неверное имя пользователя или пароль")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    # Читаем настройки отображения вкладок из .env
    show_cssi = os.getenv("SHOW_CSSI", "true").lower() == "true"
    show_cpg = os.getenv("SHOW_CPG", "true").lower() == "true" 
    show_token = os.getenv("SHOW_TOKEN", "true").lower() == "true"
    show_messages = os.getenv("SHOW_MESSAGES", "true").lower() == "true"
    
    return render_template("index.html", 
                         show_cssi=show_cssi,
                         show_cpg=show_cpg, 
                         show_token=show_token,
                         show_messages=show_messages)


@app.route("/generate/<region>")
@login_required
def generate(region):
    # print(111, region, type(region))

    def generate_output():
        capture = OutputCapture()
        sys.stdout = capture
        sys.stderr = capture

        def output_callback(text):
            yield f"data: {text}\n\n"

        capture.add_callback(output_callback)

        try:
            # Очищаем директорию перед генерацией
            print("[DEBUG] Начало функции generate()")
            clear_dir()
            print("[DEBUG] Директория очищена")

            """ # Пересоздаем константы генератора
            print("[DEBUG] Вызов reset_generator_constants()")
            reset_generator_constants()
            print("[DEBUG] reset_generator_constants() завершен")"""
            # Выводим сообщение о начале генерации
            yield "data: Начинаю генерацию...\n\n"

            # Запускаем генерацию в зависимости от значения TAKE_CONSTANTS_FROM_FILE
            if TAKE_CONSTANTS_FROM_FILE:
                print(
                    "[DEBUG] TAKE_CONSTANTS_FROM_FILE = True, вызываем generate_region_files()"
                )
                generate_region_files()
                print("[DEBUG] generate_region_files() завершен")
            else:
                print(
                    "[DEBUG] TAKE_CONSTANTS_FROM_FILE = False, получаем константы из get_next_constants()"
                )
                try:
                    print("[DEBUG] Вызов get_next_constants()")
                    for constants_dict in get_next_constants():
                        print(
                            2222,
                            constants_dict.get("region_name/constant name", "region1"),
                        )
                        if region != constants_dict.get(
                            "region_name/constant name", "region1"
                        ):
                            continue
                        print(
                            f"[DEBUG] Обработка констант для региона: {constants_dict.get('region_name/constant name', 'region1')}"
                        )

                        # Обновляем константы перед очисткой словарей
                        ALL_PROJ_CONSTANTS.update(constants_dict)
                        # make lists from strings
                        for k, v in ALL_PROJ_CONSTANTS.items():
                            if isinstance(v, str) and "[" in v:
                                ALL_PROJ_CONSTANTS[k] = eval(v)

                        # Проверяем, что важные константы определены и не пустые
                        if (
                            "INCIDENT_TYPES_FOR_CARD01" not in ALL_PROJ_CONSTANTS
                            or not ALL_PROJ_CONSTANTS["INCIDENT_TYPES_FOR_CARD01"]
                        ):
                            print(
                                "[WARNING] INCIDENT_TYPES_FOR_CARD01 не определена или пуста, устанавливаем значение по умолчанию"
                            )
                            ALL_PROJ_CONSTANTS["INCIDENT_TYPES_FOR_CARD01"] = [
                                "Пожар",
                                "Взрыв",
                                "Обрушение",
                            ]  # Примерное значение по умолчанию

                        # Теперь очищаем словари
                        ukios_info.clear()
                        missed_info.clear()

                        region_name = constants_dict.get(
                            "region_name/constant name", "region1"
                        )
                        print(f"[DEBUG] Генерация файлов для региона: {region_name}")
                        generate_region_files(region_name=region_name)
                        print(
                            f"[DEBUG] Генерация файлов для региона {region_name} завершена"
                        )
                except Exception as e:
                    print(f"[ERROR] Ошибка при получении констант: {str(e)}")
                    print(f"[ERROR] Тип ошибки: {type(e).__name__}")
                    import traceback

                    print(f"[ERROR] Трассировка: {traceback.format_exc()}")
                    yield f"data: Ошибка при получении констант: {str(e)}. Используем значение по умолчанию.\n\n"
                    generate_region_files()

            # Подсчитываем количество сгенерированных файлов
            print("[DEBUG] Подсчет сгенерированных файлов")
            ukios_files = get_ukios_files()
            file_count = len(ukios_files)

            # Ваш код здесь

            # snapshot = tracemalloc.take_snapshot()
            # top_stats = snapshot.statistics('lineno')
            #
            # print("[Top 10 memory usage]")
            # for stat in top_stats[:10]:
            #     print(stat)
            # print(f"[DEBUG] Сгенерировано файлов: {file_count}")

            # from pympler import muppy, summary
            #
            # all_objects = muppy.get_objects()
            # sum_obj = summary.summarize(all_objects)
            # summary.print_(sum_obj)

            # Выводим сообщение о завершении
            yield f"data: Генерация завершена успешно, сгенерировано файлов: {file_count}\n\n"

        except Exception as e:
            print(f"[ERROR] Ошибка в генерации: {str(e)}")
            print(f"[ERROR] Тип ошибки: {type(e).__name__}")
            import traceback

            print(f"[ERROR] Трассировка: {traceback.format_exc()}")
            yield f"data: Ошибка в генерации: {str(e)}\n\n"
        finally:
            sys.stdout = capture.stdout
            sys.stderr = capture.stderr
            capture.remove_callback(output_callback)
            yield "event: done\ndata: \n\n"

    return Response(
        stream_with_context(generate_output()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.route("/files")
@login_required
def list_files():
    return jsonify(get_ukios_files())


@app.route("/file/<path:filename>")
@login_required
def get_file(filename):
    try:
        file_path = os.path.join("files", "TEST", filename)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return Response(content, mimetype="text/xml")
        else:
            return "Файл не найден", 404
    except Exception as e:
        return f"Ошибка при чтении файла: {str(e)}", 500


@app.route("/test-server", methods=["POST"])
@login_required
def test_server():
    success_response = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ens="http://system112.ru/112/integration.wsdl" xmlns:ins="http://system112.ru/112/integration" xmlns:jxb="http://java.sun.com/xml/ns/jaxb">
<soap:Body>
<ins:card112ChangedResponse xmlns:ins="http://system112.ru/112/integration" xmlns="http://system112.ru/112/integration">
<ins:errorCode>0</ins:errorCode>
</ins:card112ChangedResponse>
</soap:Body>
</soap:Envelope>"""
    return success_response, 200, {"Content-Type": "text/xml;charset=UTF-8"}


@app.route("/api/regions")
@login_required
def get_regions():
    regions = get_available_regions()
    print(f"API /api/regions: возвращаю регионы: {regions}")
    return jsonify(regions)


@app.route("/api/send", methods=["POST"])
@login_required
def send_file():
    try:
        data = request.get_json()
        url = data.get("url")
        region = data.get("region")  # Теперь получаем регион вместо логина/пароля
        filename = data.get("file")

        if not all([url, region, filename]):
            return jsonify(
                {"success": False, "message": "Ошибка: не все параметры предоставлены"}
            ), 400

        # Получаем пароль для выбранного региона
        password = get_password_for_login(region)
        if not password:
            return jsonify(
                {
                    "success": False,
                    "message": f"Ошибка: не найден пароль для региона {region}",
                }
            ), 404

        # Читаем содержимое файла
        file_path = os.path.join("files", "TEST", filename)
        if not os.path.exists(file_path):
            return jsonify(
                {"success": False, "message": f"Ошибка: файл {filename} не найден"}
            ), 404

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Исправляем префикс XML
            content = content.replace("<?сбитый префикс для ukio", "<?xml")

        # Отправляем запрос
        headers = {
            "Content-Type": "text/xml;charset=UTF-8",
            "Authorization": f"Basic {base64.b64encode(f'{region}:{password}'.encode()).decode()}",
        }

        try:
            print_colored(f"\n[Отправка файла: {filename}]", Colors.BOLD)
            # print_request_details(url, headers, content)

            response = requests.post(
                url, data=content, headers=headers, timeout=30, verify=False
            )

            # print_response_details(response)

            if response.status_code == 200:
                return jsonify(
                    {
                        "success": True,
                        "message": f"Файл успешно отправлен ({response.status_code})",
                    }
                )
            else:
                return jsonify(
                    {
                        "success": False,
                        "message": f"Ошибка при отправке файла: {response.status_code}",
                    }
                ), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify(
                {"success": False, "message": f"Ошибка при отправке запроса: {str(e)}"}
            ), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка: {str(e)}"}), 500


def capture_main_output():
    sys.stderr.write("DEBUG: Начало capture_main_output\n")
    capture = OutputCapture()
    sys.stdout = capture
    sys.stderr = capture

    def output_callback(text):
        # Пропускаем отладочные сообщения и пустые строки
        if not text.startswith("DEBUG:") and text.strip():
            sys.stderr.write(f"DEBUG: Получено сообщение: {text}\n")
            log_message({"type": "console_output", "text": text})

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

def cpg_log_message(message):
    for callback in cpg_log_callbacks:
        callback(message)


@app.route("/api/auto-generate", methods=["POST"])
@login_required
def start_auto_generation():
    global \
        auto_generation_thread, \
        auto_generation_running, \
        auto_generation_start_time, \
        auto_generation_end_time, \
        auto_generation_interval, \
        total_files_sent

    data = request.json
    interval = float(data.get("interval", 1))
    duration = float(data.get("duration", 10))
    url = data.get("url")  # URL теперь опциональный

    if auto_generation_running:
        return jsonify(
            {"success": False, "message": "Автоматическая генерация уже запущена"}
        )

    auto_generation_running = True
    auto_generation_start_time = time.time()
    auto_generation_end_time = auto_generation_start_time + (duration * 60)
    auto_generation_interval = interval
    total_files_sent = 0

    auto_generation_thread = Thread(target=auto_generation_worker, args=(url,))
    auto_generation_thread.start()

    return jsonify(
        {
            "success": True,
            "message": "Автоматическая генерация запущена",
            "start_time": auto_generation_start_time,
            "end_time": auto_generation_end_time,
        }
    )


@app.route("/api/auto-generate/stop", methods=["POST"])
@login_required
def stop_auto_generation():
    global auto_generation_running

    if not auto_generation_running:
        return jsonify(
            {"success": False, "message": "Автоматическая генерация не запущена"}
        )

    auto_generation_running = False
    return jsonify({"success": True, "message": "Автоматическая генерация остановлена"})


@app.route("/api/auto-generate/status", methods=["GET"])
@login_required
def get_auto_generation_status():
    if not auto_generation_running:
        return jsonify(
            {"running": False, "message": "Автоматическая генерация не запущена"}
        )

    time_left = max(0, auto_generation_end_time - time.time())
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)

    return jsonify(
        {
            "running": True,
            "timeLeft": f"{minutes:02d}:{seconds:02d}",
            "filesSent": total_files_sent,
        }
    )


@app.route("/api/auto-generate/logs")
@login_required
def auto_generate_logs():
    def generate_logs():
        try:
            # Отправляем начальное сообщение для установки соединения
            yield ": keep-alive\n\n"

            while True:
                try:
                    if not auto_generation_running:
                        # Если генерация остановлена, отправляем сообщение и ждем
                        yield f"data: {json.dumps({'type': 'status_update', 'status': 'stopped'})}\n\n"
                        time.sleep(1)
                        continue

                    # Создаем словарь для хранения текущего состояния
                    current_state = {
                        "type": "status_update",
                        "files_sent": total_files_sent,
                        "time_left": max(0, auto_generation_end_time - time.time()),
                    }

                    # Отправляем обновленное состояние
                    yield f"data: {json.dumps(current_state)}\n\n"
                    time.sleep(0.1)

                except GeneratorExit:
                    # Клиент закрыл соединение
                    break
                except Exception as e:
                    print(f"Ошибка в генераторе логов: {str(e)}")
                    time.sleep(1)
                    continue

        except Exception as e:
            print(f"Критическая ошибка в генераторе логов: {str(e)}")

    response = Response(
        stream_with_context(generate_logs()), mimetype="text/event-stream"
    )

    # Добавляем необходимые заголовки для SSE
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    response.headers["X-Accel-Buffering"] = "no"
    response.headers["Access-Control-Allow-Origin"] = "*"

    return response


def get_generated_regions():
    """Получает список фактически сгенерированных регионов из директории"""
    regions = []
    base_path = os.path.join("files", "TEST")

    if not os.path.exists(base_path):
        return regions

    for region in os.listdir(base_path):
        region_path = os.path.join(base_path, region, "Ukios")
        if os.path.exists(region_path) and os.listdir(region_path):
            regions.append(region)

    return sorted(regions)


def auto_generation_worker(url=None):
    global auto_generation_running, total_files_sent
    total_files_sent = 0

    print("DEBUG: Запущен worker")
    print(
        f"DEBUG: Время работы - start: {auto_generation_start_time}, end: {auto_generation_end_time}, interval: {auto_generation_interval}"
    )

    # Используем URL из запроса или из конфигурации
    if not url:
        url = os.getenv("TEST_SERVER_URL", "http://localhost:5000/test-server")
    print(f"DEBUG: Используется URL: {url}")

    while auto_generation_running:
        try:
            current_time = time.time()
            time_left = auto_generation_end_time - current_time
            minutes_left = int(time_left // 60)
            seconds_left = int(time_left % 60)

            print(f"DEBUG: Осталось времени: {minutes_left:02d}:{seconds_left:02d}")
            log_message({"type": "time_left", "minutes": minutes_left, "seconds": seconds_left})

            # Проверяем, не истекло ли время
            if current_time >= auto_generation_end_time:
                print("DEBUG: Время генерации истекло")
                log_message(
                    {"type": "console_output", "text": "Время генерации истекло"}
                )
                auto_generation_running = False
                print("DEBUG: Автогенерация завершена")
                log_message(
                    {"type": "console_output", "text": "Автогенерация завершена"}
                )
                break

            # Начало генерации
            print("DEBUG: Начало цикла генерации")
            log_message({"type": "console_output", "text": "Начало цикла генерации"})
            log_message({"type": "generation_start"})

            # Генерируем файлы
            capture = OutputCapture()
            sys.stdout = capture
            sys.stderr = capture

            def output_callback(text):
                if not text.startswith("DEBUG:"):
                    log_message({"type": "console_output", "text": text})

            capture.add_callback(output_callback)

            try:
                # Очищаем директорию перед генерацией

                clear_dir()

                # Генерируем файлы
                # Генерируем файлы
                if TAKE_CONSTANTS_FROM_FILE:
                    # print("DEBUG: TAKE_CONSTANTS_FROM_FILE = True, вызываем generate_region_files()")
                    generate_region_files()
                    # print("DEBUG: generate_region_files() завершен")
                else:
                    # print("DEBUG: TAKE_CONSTANTS_FROM_FILE = False, получаем константы из get_next_constants()")
                    try:
                        constants_loaded = False
                        for constants_dict in get_next_constants():
                            constants_loaded = True
                            region_name = constants_dict.get(
                                "region_name/constant name", "region1"
                            )
                            print(f"DEBUG: Генерация файлов для региона: {region_name}")
                            # Обновляем все константы из словаря
                            ALL_PROJ_CONSTANTS.update(constants_dict)
                            # Преобразуем строковые представления списков в списки
                            for k, v in ALL_PROJ_CONSTANTS.items():
                                if isinstance(v, str) and "[" in v:
                                    ALL_PROJ_CONSTANTS[k] = eval(v)
                            generate_region_files(region_name=region_name)

                        if not constants_loaded:
                            print("DEBUG: Не удалось загрузить константы - нет данных")
                            log_message(
                                {
                                    "type": "error",
                                    "message": "Не удалось загрузить константы из Google таблицы",
                                }
                            )
                    except Exception as e:
                        error_msg = f"DEBUG: Ошибка при получении констант: {str(e)}"
                        print(error_msg)
                        log_message({"type": "error", "message": error_msg})
                        import traceback

                        traceback_msg = traceback.format_exc()
                        print(f"DEBUG: Traceback: {traceback_msg}")
                        log_message(
                            {
                                "type": "error",
                                "message": "Подробная ошибка: " + traceback_msg,
                            }
                        )
                        # Не выполняем generate_region_files() при ошибке

            finally:
                sys.stdout = capture.stdout
                sys.stderr = capture.stderr
                capture.remove_callback(output_callback)

            # Получаем список фактически сгенерированных регионов
            generated_regions = get_generated_regions()
            print(f"DEBUG: Сгенерированные регионы: {generated_regions}")
            log_message({"type": "console_output", "text": f"Сгенерированные регионы: {generated_regions}"})

            # Для каждого сгенерированного региона ищем соответствующий логин/пароль и отправляем файлы
            for region in generated_regions:
                if not auto_generation_running:
                    break

                print(f"DEBUG: Обработка региона: {region}")
                log_message({"type": "console_output", "text": f"Обработка региона: {region}"})
                log_message(
                    {"type": "console_output", "text": f"Обработка региона: {region}"}
                )

                # Получаем пароль для текущего региона
                password = get_password_for_login(region)
                if not password:
                    print(f"DEBUG: Не найден пароль для региона {region}")
                    log_message(
                        {
                            "type": "console_output",
                            "text": f"Не найден пароль для региона {region}",
                        }
                    )
                    continue

                # Получаем список файлов для текущего региона
                files = get_ukios_files()
                region_files = [f for f in files if f.startswith(f"{region}/Ukios/")]

                if not region_files:
                    print(f"DEBUG: Нет файлов для региона {region}")
                    log_message(
                        {
                            "type": "console_output",
                            "text": f"Нет файлов для региона {region}",
                        }
                    )
                    continue

                print(
                    f"DEBUG: Найдено файлов для региона {region}: {len(region_files)}"
                )
                log_message({"type": "files_found", "count": len(region_files)})

                # Отправляем каждый файл региона
                for i, filename in enumerate(region_files, 1):
                    if not auto_generation_running:
                        break

                    print(f"DEBUG: Отправка файла {i}/{len(region_files)}: {filename}")
                    log_message({"type": "sending_file", "current": i, "total": len(region_files)})
                    log_message(
                        {
                            "type": "sending_file",
                            "current": i,
                            "total": len(region_files),
                        }
                    )

                    try:
                        # Читаем содержимое файла
                        file_path = os.path.join("files", "TEST", filename)
                        if not os.path.exists(file_path):
                            print(f"DEBUG: Файл {filename} не найден")
                            continue

                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            # Исправляем префикс XML
                            content = content.replace(
                                "<?сбитый префикс для ukio", "<?xml"
                            )

                        # Отправляем запрос напрямую на тестовый сервер
                        headers = {
                            "Content-Type": "text/xml;charset=UTF-8",
                            "Authorization": f"Basic {base64.b64encode(f'{region}:{password}'.encode()).decode()}",
                        }

                        print_colored(f"\n[Отправка файла: {filename}]", Colors.BOLD)
                        # print_request_details(url, headers, content)

                        response = requests.post(
                            url, data=content, headers=headers, timeout=30, verify=False
                        )

                        # print_response_details(response)

                        if response.status_code == 200:
                            total_files_sent += 1
                            print(f"DEBUG: Файл {filename} успешно отправлен")
                            log_message(
                                {
                                    "type": "console_output",
                                    "text": f"Файл {filename} успешно отправлен",
                                }
                            )
                        else:
                            print(
                                f"DEBUG: Ошибка при отправке файла {filename}: {response.status_code}"
                            )
                            # Добавляем вывод тела ответа для диагностики
                            if response.status_code == 500:
                                print(f"DEBUG: Ответ сервера: {response.text[:500]}")  # Первые 500 символов
                            log_message(
                                {
                                    "type": "error",
                                    "message": f"Ошибка при отправке файла {filename}: {response.status_code}",
                                }
                            )

                    except Exception as e:
                        error_msg = f"Ошибка при обработке файла {filename}: {str(e)}"
                        print(f"DEBUG: {error_msg}")
                        log_message({"type": "error", "message": error_msg})
                        log_message(
                            {
                                "type": "error",
                                "message": f"Ошибка при обработке файла {filename}: {str(e)}",
                            }
                        )

            # Генерация завершена
            print("DEBUG: Цикл генерации завершен")
            log_message({"type": "console_output", "text": "Цикл генерации завершен"})
            log_message({"type": "generation_complete"})

            # Проверяем, не истекло ли время после завершения цикла
            if time.time() >= auto_generation_end_time:
                print("DEBUG: Время генерации истекло после завершения цикла")
                log_message(
                    {"type": "console_output", "text": "Время генерации истекло"}
                )
                auto_generation_running = False
                break

            # Ожидание следующего цикла
            wait_seconds = int(auto_generation_interval * 60)
            print(f"DEBUG: Ожидание {wait_seconds} секунд до следующего цикла")
            log_message({"type": "console_output", "text": f"Ожидание {wait_seconds} секунд до следующего цикла"})
            log_message({"type": "waiting", "seconds": wait_seconds})

            # Проверяем, не истекло ли время во время ожидания
            end_time = time.time() + wait_seconds
            while time.time() < end_time and auto_generation_running:
                if time.time() >= auto_generation_end_time:
                    auto_generation_running = False
                    break
                time.sleep(1)

        except Exception as e:
            print(f"DEBUG: Ошибка в цикле генерации: {str(e)}")
            log_message(
                {"type": "error", "message": f"Ошибка в цикле генерации: {str(e)}"}
            )
            time.sleep(1)


# ========== ЦПГ API ЭНДПОИНТЫ ==========

@app.route("/cpg/generate/<region>")
@login_required
def cpg_generate(region):
    def generate_cpg_output():
        capture = OutputCapture()
        sys.stdout = capture
        sys.stderr = capture

        def output_callback(text):
            yield f"data: {text}\n\n"

        capture.add_callback(output_callback)

        try:
            print("[DEBUG] Начало генерации")
            
            # Импортируем функции
            from main_cpg import generate_cpg_region_files
            from config.dirs import clear_dir, clear_cpg_dir
            from constants.constants_remaker import get_next_constants
            
            # Очищаем только ЦПГ директории, не трогаем ЦССИ
            print("[DEBUG] Очистка ЦПГ директорий перед генерацией")
            clear_cpg_dir()
            yield "data: Начинаю генерацию...\n\n"
            
            print(f"[DEBUG] Генерация для региона: {region}")
            
            # Запускаем генерацию в зависимости от значения TAKE_CONSTANTS_FROM_FILE
            if TAKE_CONSTANTS_FROM_FILE:
                print("[DEBUG] TAKE_CONSTANTS_FROM_FILE = True, вызываем generate_cpg_region_files() с константами из файла")
                generate_cpg_region_files(region_name=region)
            else:
                print("[DEBUG] TAKE_CONSTANTS_FROM_FILE = False, получаем константы из get_next_constants()")
                try:
                    print("[DEBUG] Вызов get_next_constants() для ЦПГ")
                    for constants_dict in get_next_constants():
                        print(f"[DEBUG] Обрабатываем константы для региона: {constants_dict.get('region_name/constant name', region)}")
                        
                        # Обновляем константы как в ЦССИ режиме
                        ALL_PROJ_CONSTANTS.update(constants_dict)
                        
                        # Преобразуем строки в списки если нужно
                        for k, v in ALL_PROJ_CONSTANTS.items():
                            if isinstance(v, str) and "[" in v:
                                ALL_PROJ_CONSTANTS[k] = eval(v)
                        
                        generate_cpg_region_files(
                            region_name=constants_dict.get("region_name/constant name", region)
                        )
                        print(f"[DEBUG] Генерация завершена для региона: {constants_dict.get('region_name/constant name', region)}")
                        
                except Exception as e:
                    print(f"[ERROR] Ошибка при загрузке констант из Google Sheets: {e}")
                    print("[DEBUG] Используем константы из файла как fallback")
                    generate_cpg_region_files(region_name=region)
            
            print("[DEBUG] Генерация завершена")
            
            # Подсчитываем количество сгенерированных файлов
            cpg_files = get_cpg_files()
            # Фильтрация файлов по региону
            file_count = len([f for f in cpg_files if region in f])
            
            yield f"data: Генерация завершена успешно, сгенерировано файлов: {file_count}\n\n"

        except Exception as e:
            print(f"[ERROR] Ошибка в генерации: {str(e)}")
            import traceback
            print(f"[ERROR] Трассировка: {traceback.format_exc()}")
            yield f"data: Ошибка в генерации: {str(e)}\n\n"
        finally:
            sys.stdout = capture.stdout
            sys.stderr = capture.stderr
            capture.remove_callback(output_callback)
            yield "event: done\ndata: \n\n"

    return Response(
        stream_with_context(generate_cpg_output()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.route("/cpg/files")
@login_required
def list_cpg_files():
    return jsonify(get_cpg_files())


@app.route("/cpg/file/<path:filename>")
@login_required
def get_cpg_file(filename):
    try:
        file_path = os.path.join("files", "TEST_cpg", filename)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return Response(content, mimetype="text/xml")
        else:
            return "Файл не найден", 404
    except Exception as e:
        return f"Ошибка при чтении файла: {str(e)}", 500


@app.route("/api/cpg/regions")
@login_required
def get_cpg_regions_api():
    regions = get_cpg_regions()
    print(f"API /api/cpg/regions: возвращаю регионы: {regions}")
    return jsonify(regions)


@app.route("/api/clear-files", methods=["POST"])
@login_required
def clear_all_files():
    try:
        import shutil
        deleted_count = 0
        deleted_folders = []
        
        # Пути к директориям
        test_dir = os.path.join("files", "TEST")
        test_cpg_dir = os.path.join("files", "TEST_cpg")
        
        # Удаляем содержимое TEST директории
        if os.path.exists(test_dir):
            for item in os.listdir(test_dir):
                item_path = os.path.join(test_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    deleted_folders.append(f"TEST/{item}")
                else:
                    os.remove(item_path)
                    deleted_count += 1
                    
        # Удаляем содержимое TEST_cpg директории  
        if os.path.exists(test_cpg_dir):
            for item in os.listdir(test_cpg_dir):
                item_path = os.path.join(test_cpg_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    deleted_folders.append(f"TEST_cpg/{item}")
                else:
                    os.remove(item_path)
                    deleted_count += 1
        
        message = f"Удалено {len(deleted_folders)} папок и {deleted_count} файлов"
        if deleted_folders:
            message += f". Папки: {', '.join(deleted_folders)}"
            
        print_colored(f"\n[Очистка файлов: {message}]", Colors.YELLOW)
        
        return jsonify({
            "success": True,
            "message": message,
            "deleted_folders": len(deleted_folders),
            "deleted_files": deleted_count
        })
        
    except Exception as e:
        error_msg = f"Ошибка при удалении файлов: {str(e)}"
        print_colored(f"\n[ОШИБКА очистки файлов: {error_msg}]", Colors.RED)
        return jsonify({
            "success": False,
            "message": error_msg
        }), 500


@app.route("/api/get-token", methods=["POST"])
@login_required  
def get_auth_token():
    try:
        data = request.get_json()
        url = data.get("url")
        client_id = data.get("client_id")
        client_secret = data.get("client_secret")

        if not all([url, client_id, client_secret]):
            return jsonify(
                {"success": False, "message": "Ошибка: не все параметры предоставлены"}
            ), 400

        # Подготавливаем данные для запроса токена
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            print_colored(f"\n[Запрос токена для client_id: {client_id}]", Colors.BOLD)
            print_request_details(url, headers, str(token_data))

            response = requests.post(
                url, 
                data=token_data, 
                headers=headers, 
                timeout=30, 
                verify=False
            )

            print_response_details(response)

            if response.status_code == 200:
                token_response = response.json()
                access_token = token_response.get("access_token")
                
                if access_token:
                    return jsonify({
                        "success": True,
                        "access_token": access_token,
                        "message": "Токен успешно получен"
                    })
                else:
                    return jsonify({
                        "success": False,
                        "message": "Токен не найден в ответе сервера"
                    }), 400
            else:
                return jsonify({
                    "success": False,
                    "message": f"Ошибка получения токена: {response.status_code}. Ответ: {response.text[:200]}"
                }), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify(
                {"success": False, "message": f"Ошибка при отправке запроса: {str(e)}"}
            ), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка: {str(e)}"}), 500


@app.route("/api/cpg/send", methods=["POST"])
@login_required
def send_cpg_file():
    try:
        data = request.get_json()
        url = data.get("url")
        region = data.get("region")
        filename = data.get("file")
        auth_token = data.get("auth_token")  # Опциональный Bearer токен

        if not all([url, region, filename]):
            return jsonify(
                {"success": False, "message": "Ошибка: не все параметры предоставлены"}
            ), 400

        # Читаем содержимое файла
        file_path = os.path.join("files", "TEST_cpg", filename)
        if not os.path.exists(file_path):
            return jsonify(
                {"success": False, "message": f"Ошибка: файл {filename} не найден"}
            ), 404

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Оборачиваем в SOAP envelope
        from constants.sender import BASE_SOAP_PREFIX, BASE_SOAP_POSTFIX
        soap_content = BASE_SOAP_PREFIX + content + BASE_SOAP_POSTFIX

        # Определяем тип авторизации
        headers = {
            "Content-Type": "text/xml;charset=UTF-8",
        }
        
        if auth_token:
            # Используем Bearer токен
            headers["Authorization"] = f"Bearer {auth_token}"
            print_colored(f"\n[Отправка файла с Bearer токеном: {filename}]", Colors.BOLD)
        else:
            # Используем Basic авторизацию (старый способ)
            password = get_cpg_password_for_login(region)
            if not password:
                return jsonify(
                    {
                        "success": False,
                        "message": f"Ошибка: не найден пароль для региона {region} и не указан токен",
                    }
                ), 404
            headers["Authorization"] = f"Basic {base64.b64encode(f'{region}:{password}'.encode()).decode()}"
            print_colored(f"\n[Отправка файла с Basic авторизацией: {filename}]", Colors.BOLD)

        try:
            print_colored(f"\n[Отправка файла: {filename}]", Colors.BOLD)
            
            # Выводим первые 500 символов SOAP XML для отладки
            print(f"[DEBUG] SOAP XML содержимое (первые 500 символов):")
            print(soap_content[:500])

            response = requests.post(
                url, data=soap_content, headers=headers, timeout=30, verify=False
            )

            if response.status_code == 200:
                return jsonify(
                    {
                        "success": True,
                        "message": f"Файл успешно отправлен ({response.status_code})",
                    }
                )
            else:
                # Выводим ответ сервера для диагностики
                print(f"[DEBUG] Ошибка {response.status_code}, ответ сервера:")
                print(response.text[:1000])
                return jsonify(
                    {
                        "success": False,
                        "message": f"Ошибка при отправке файла: {response.status_code}. Ответ: {response.text[:200]}",
                    }
                ), response.status_code

        except requests.exceptions.RequestException as e:
            return jsonify(
                {"success": False, "message": f"Ошибка при отправке запроса: {str(e)}"}
            ), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка: {str(e)}"}), 500


# ========== АВТОГЕНЕРАЦИЯ ДЛЯ ВТОРОЙ СИСТЕМЫ ==========

@app.route("/api/cpg/auto-generate", methods=["POST"])
@login_required
def start_cpg_auto_generation():
    global \
        cpg_auto_generation_thread, \
        cpg_auto_generation_running, \
        cpg_auto_generation_start_time, \
        cpg_auto_generation_end_time, \
        cpg_auto_generation_interval, \
        cpg_total_files_sent

    data = request.json
    interval = float(data.get("interval", 1))
    duration = float(data.get("duration", 10))
    url = data.get("url")
    auth_token = data.get("auth_token")  # Опциональный Bearer токен
    selected_regions = data.get("selected_regions", [])  # Опциональный список регионов

    if cpg_auto_generation_running:
        return jsonify(
            {"success": False, "message": "Автоматическая генерация уже запущена"}
        )

    cpg_auto_generation_running = True
    cpg_auto_generation_start_time = time.time()
    cpg_auto_generation_end_time = cpg_auto_generation_start_time + (duration * 60)
    cpg_auto_generation_interval = interval
    cpg_total_files_sent = 0

    cpg_auto_generation_thread = Thread(target=cpg_auto_generation_worker, args=(url, auth_token, selected_regions))
    cpg_auto_generation_thread.start()

    return jsonify(
        {
            "success": True,
            "message": "Автоматическая генерация запущена",
            "start_time": cpg_auto_generation_start_time,
            "end_time": cpg_auto_generation_end_time,
        }
    )


@app.route("/api/cpg/auto-generate/stop", methods=["POST"])
@login_required
def stop_cpg_auto_generation():
    global cpg_auto_generation_running

    if not cpg_auto_generation_running:
        return jsonify(
            {"success": False, "message": "Автоматическая генерация не запущена"}
        )

    cpg_auto_generation_running = False
    return jsonify({"success": True, "message": "Автоматическая генерация остановлена"})


@app.route("/api/cpg/auto-generate/status", methods=["GET"])
@login_required
def get_cpg_auto_generation_status():
    if not cpg_auto_generation_running:
        return jsonify(
            {"running": False, "message": "Автоматическая генерация не запущена"}
        )

    time_left = max(0, cpg_auto_generation_end_time - time.time())
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)

    return jsonify(
        {
            "running": True,
            "timeLeft": f"{minutes:02d}:{seconds:02d}",
            "filesSent": cpg_total_files_sent,
        }
    )


@app.route("/api/cpg/auto-generate/logs")
@login_required
def cpg_auto_generate_logs():
    def generate_cpg_logs():
        message_queue = queue.Queue()
        
        def log_callback(message):
            message_queue.put(message)
        
        # Добавляем callback для получения логов
        cpg_log_callbacks.append(log_callback)
        
        try:
            yield ": keep-alive\n\n"
            while True:
                try:
                    # Проверяем наличие сообщений в очереди (неблокирующе)
                    try:
                        message = message_queue.get_nowait()
                        yield f"data: {json.dumps(message)}\n\n"
                    except queue.Empty:
                        pass
                    
                    # Если автогенерация не запущена, отправляем статус
                    if not cpg_auto_generation_running:
                        time.sleep(1)
                        continue
                        
                    time.sleep(0.1)
                except GeneratorExit:
                    break
                except Exception as e:
                    print(f"Ошибка в генераторе логов ЦПГ: {str(e)}")
                    time.sleep(1)
                    continue
        except Exception as e:
            print(f"Критическая ошибка в генераторе логов ЦПГ: {str(e)}")
        finally:
            # Удаляем callback при закрытии соединения
            if log_callback in cpg_log_callbacks:
                cpg_log_callbacks.remove(log_callback)

    response = Response(
        stream_with_context(generate_cpg_logs()), mimetype="text/event-stream"
    )
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    response.headers["X-Accel-Buffering"] = "no"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def get_cpg_generated_regions():
    """Получает список фактически сгенерированных регионов из директории TEST_cpg"""
    regions = []
    base_path = os.path.join("files", "TEST_cpg")

    if not os.path.exists(base_path):
        return regions

    for region in os.listdir(base_path):
        region_path = os.path.join(base_path, region, "UpdateCard")
        if os.path.exists(region_path) and os.listdir(region_path):
            regions.append(region)

    return sorted(regions)


def cpg_auto_generation_worker(url=None, auth_token=None, selected_regions=None):
    global cpg_auto_generation_running, cpg_total_files_sent
    cpg_total_files_sent = 0

    print("DEBUG: Запущен worker автогенерации")
    cpg_log_message({"type": "console_output", "text": "Запущен worker автогенерации"})
    print(
        f"DEBUG: Время работы - start: {cpg_auto_generation_start_time}, end: {cpg_auto_generation_end_time}, interval: {cpg_auto_generation_interval}"
    )
    
    # Очищаем ЦПГ директории перед началом автогенерации
    print("DEBUG: Очистка ЦПГ директорий перед автогенерацией")
    cpg_log_message({"type": "console_output", "text": "Очистка ЦПГ директорий"})
    from config.dirs import clear_cpg_dir
    clear_cpg_dir()

    if not url:
        url = "https://tspg-connect-master.connect.lan/soap_1?"
    
    auth_type = "Bearer токеном" if auth_token else "Basic авторизацией"
    regions_text = f" для регионов: {', '.join(selected_regions)}" if selected_regions else " для всех регионов"
    print(f"DEBUG: auth_token = '{auth_token}', selected_regions = {selected_regions}")
    print(f"DEBUG: Используется URL: {url} с {auth_type}{regions_text}")
    cpg_log_message({"type": "console_output", "text": f"Используется URL: {url} с {auth_type}{regions_text}"})

    while cpg_auto_generation_running:
        try:
            current_time = time.time()
            time_left = cpg_auto_generation_end_time - current_time
            minutes_left = int(time_left // 60)
            seconds_left = int(time_left % 60)

            print(f"DEBUG: Осталось времени: {minutes_left:02d}:{seconds_left:02d}")
            cpg_log_message({"type": "time_left", "minutes": minutes_left, "seconds": seconds_left})

            if current_time >= cpg_auto_generation_end_time:
                print("DEBUG: Время генерации истекло")
                cpg_log_message({"type": "console_output", "text": "Время генерации истекло"})
                cpg_auto_generation_running = False
                print("DEBUG: Автогенерация завершена")
                cpg_log_message({"type": "console_output", "text": "Автогенерация завершена"})
                break

            print("DEBUG: Начало цикла генерации")
            cpg_log_message({"type": "console_output", "text": "Начало цикла генерации"})

            # Генерируем файлы для выбранных регионов или всех
            if selected_regions:
                cpg_regions = [region for region in selected_regions if region in get_cpg_regions()]
                print(f"DEBUG: Используются выбранные регионы: {cpg_regions}")
            else:
                cpg_regions = get_cpg_regions()
                print(f"DEBUG: Используются все регионы: {cpg_regions}")
            
            for region in cpg_regions:
                if not cpg_auto_generation_running:
                    break
                
                print(f"DEBUG: Генерация для региона {region}")
                cpg_log_message({"type": "console_output", "text": f"Генерация для региона {region}"})
                try:
                    from main_cpg import generate_cpg_region_files
                    from constants.constants_remaker import get_next_constants
                    
                    # Запускаем генерацию в зависимости от значения TAKE_CONSTANTS_FROM_FILE
                    if TAKE_CONSTANTS_FROM_FILE:
                        print(f"[DEBUG] TAKE_CONSTANTS_FROM_FILE = True, генерация {region} с константами из файла")
                        generate_cpg_region_files(region_name=region)
                    else:
                        print(f"[DEBUG] TAKE_CONSTANTS_FROM_FILE = False, загружаем константы из Google Sheets для {region}")
                        constants_loaded = False
                        for constants_dict in get_next_constants():
                            # Фильтруем по текущему региону - пропускаем если это не тот регион
                            region_from_constants = constants_dict.get("region_name/constant name", "")
                            if region_from_constants != region:
                                print(f"[DEBUG] Пропускаем константы для региона {region_from_constants}, нужен {region}")
                                continue
                                
                            print(f"[DEBUG] Найдены константы для региона {region}")
                            # Обновляем константы
                            ALL_PROJ_CONSTANTS.update(constants_dict)
                            
                            # Преобразуем строки в списки если нужно
                            for k, v in ALL_PROJ_CONSTANTS.items():
                                if isinstance(v, str) and "[" in v:
                                    ALL_PROJ_CONSTANTS[k] = eval(v)
                            
                            generate_cpg_region_files(region_name=region)
                            constants_loaded = True
                            break  # Генерируем только для текущего региона
                            
                        if not constants_loaded:
                            print(f"[DEBUG] Не удалось загрузить константы из Google Sheets для {region}, используем файловые")
                            generate_cpg_region_files(region_name=region)
                            
                except Exception as e:
                    error_msg = f"Ошибка генерации для {region}: {str(e)}"
                    print(f"DEBUG: {error_msg}")
                    cpg_log_message({"type": "error", "message": error_msg})
                    continue

            # Получаем список сгенерированных регионов
            generated_regions = get_cpg_generated_regions()
            print(f"DEBUG: Сгенерированные регионы: {generated_regions}")
            cpg_log_message({"type": "console_output", "text": f"Сгенерированные регионы: {generated_regions}"})

            # Отправляем файлы для каждого региона
            for region in generated_regions:
                if not cpg_auto_generation_running:
                    break

                print(f"DEBUG: Обработка региона: {region}")
                cpg_log_message({"type": "console_output", "text": f"Обработка региона: {region}"})

                # Получаем пароль для региона (только если не используется токен)
                password = None
                if not auth_token:
                    password = get_cpg_password_for_login(region)
                    if not password:
                        error_msg = f"Не найден пароль для региона {region}"
                        print(f"DEBUG: {error_msg}")
                        cpg_log_message({"type": "console_output", "text": error_msg})
                        continue

                # Получаем список файлов для региона
                files = get_cpg_files()
                region_files = [f for f in files if f.startswith(f"{region}/")]

                if not region_files:
                    msg = f"Нет файлов для региона {region}"
                    print(f"DEBUG: {msg}")
                    cpg_log_message({"type": "console_output", "text": msg})
                    continue

                print(f"DEBUG: Найдено файлов для региона {region}: {len(region_files)}")
                cpg_log_message({"type": "files_found", "count": len(region_files)})

                # Отправляем каждый файл
                for i, filename in enumerate(region_files, 1):
                    if not cpg_auto_generation_running:
                        break

                    print(f"DEBUG: Отправка файла {i}/{len(region_files)}: {filename}")
                    cpg_log_message({"type": "sending_file", "current": i, "total": len(region_files)})

                    try:
                        file_path = os.path.join("files", "TEST_cpg", filename)
                        if not os.path.exists(file_path):
                            continue

                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        # Оборачиваем в SOAP
                        from constants.sender import BASE_SOAP_PREFIX, BASE_SOAP_POSTFIX
                        soap_content = BASE_SOAP_PREFIX + content + BASE_SOAP_POSTFIX

                        # Определяем тип авторизации
                        headers = {
                            "Content-Type": "text/xml;charset=UTF-8",
                        }
                        
                        if auth_token:
                            # Используем Bearer токен
                            headers["Authorization"] = f"Bearer {auth_token}"
                        else:
                            # Используем Basic авторизацию (старый способ)
                            if not password:
                                error_msg = f"Не найден пароль для региона {region} и не указан токен"
                                print(f"DEBUG: {error_msg}")
                                cpg_log_message({"type": "console_output", "text": error_msg})
                                continue
                            headers["Authorization"] = f"Basic {base64.b64encode(f'{region}:{password}'.encode()).decode()}"

                        response = requests.post(
                            url, data=soap_content, headers=headers, timeout=30, verify=False
                        )

                        if response.status_code == 200:
                            cpg_total_files_sent += 1
                            success_msg = f"Файл {filename} успешно отправлен"
                            print(f"DEBUG: {success_msg}")
                            cpg_log_message({"type": "file_sent_success", "filename": filename, "total_sent": cpg_total_files_sent})
                        else:
                            error_msg = f"Ошибка при отправке файла {filename}: {response.status_code}"
                            print(f"DEBUG: {error_msg}")
                            cpg_log_message({"type": "file_sent_error", "filename": filename, "status_code": response.status_code})

                    except Exception as e:
                        error_msg = f"Ошибка при обработке файла {filename}: {str(e)}"
                        print(f"DEBUG: {error_msg}")
                        cpg_log_message({"type": "error", "message": error_msg})

            print("DEBUG: Цикл генерации завершен")
            cpg_log_message({"type": "console_output", "text": "Цикл генерации завершен"})

            if time.time() >= cpg_auto_generation_end_time:
                cpg_auto_generation_running = False
                break

            # Ожидание следующего цикла
            wait_seconds = int(cpg_auto_generation_interval * 60)
            print(f"DEBUG: Ожидание {wait_seconds} секунд до следующего цикла")
            cpg_log_message({"type": "console_output", "text": f"Ожидание {wait_seconds} секунд до следующего цикла"})

            end_time = time.time() + wait_seconds
            while time.time() < end_time and cpg_auto_generation_running:
                if time.time() >= cpg_auto_generation_end_time:
                    cpg_auto_generation_running = False
                    break
                time.sleep(1)

        except Exception as e:
            error_msg = f"Ошибка в цикле генерации: {str(e)}"
            print(f"DEBUG: {error_msg}")
            cpg_log_message({"type": "error", "message": error_msg})
            time.sleep(1)


# ========== ПИТВ API ЭНДПОИНТЫ ==========

@app.route("/api/pitv/messages", methods=["GET"])
@login_required
def get_pitv_messages():
    """Получить сообщения ПИТВ из журнала"""
    if not PITV_AVAILABLE:
        return jsonify({"success": False, "error": "ПИТВ модули недоступны"}), 503
    
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
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/pitv/messages/clear", methods=["POST"])
@login_required
def clear_pitv_messages():
    """Очистить журнал сообщений ПИТВ"""
    if not PITV_AVAILABLE:
        return jsonify({"success": False, "error": "ПИТВ модули недоступны"}), 503
    
    try:
        success = message_logger.clear_messages()
        return jsonify({
            "success": success,
            "message": "Журнал очищен" if success else "Ошибка очистки"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/pitv/statistics", methods=["GET"])
@login_required
def get_pitv_statistics():
    """Получить статистику сообщений ПИТВ"""
    if not PITV_AVAILABLE:
        return jsonify({"success": False, "error": "ПИТВ модули недоступны"}), 503
    
    try:
        stats = message_logger.get_statistics()
        return jsonify({
            "success": True,
            "statistics": stats
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/pitv/status", methods=["GET"])
@login_required
def get_pitv_status():
    """Получить статус сервера приема ПИТВ"""
    if not PITV_AVAILABLE:
        return jsonify({
            "success": False, 
            "available": False,
            "error": "ПИТВ модули недоступны"
        })
    
    try:
        # Проверяем доступность через HTTP запрос
        import requests
        response = requests.get("http://localhost:8081/health", timeout=2)
        server_status = response.status_code == 200
        server_data = response.json() if response.status_code == 200 else {}
    except:
        server_status = False
        server_data = {}
    
    return jsonify({
        "success": True,
        "available": True,
        "server_running": server_status,
        "server_data": server_data
    })


@app.route("/api/pitv/messages/stream", methods=["GET"])
@login_required
def stream_pitv_messages():
    """SSE поток для real-time обновлений сообщений ПИТВ"""
    if not PITV_AVAILABLE:
        return Response("ПИТВ модули недоступны", status=503)
    
    def generate_messages():
        message_queue = queue.Queue()
        
        def message_callback(message_data):
            message_queue.put(message_data)
        
        # Добавляем callback для получения новых сообщений
        pitv_message_callbacks.append(message_callback)
        message_logger.add_callback(message_callback)
        
        try:
            yield ": keep-alive\n\n"
            
            while True:
                try:
                    # Проверяем наличие новых сообщений (неблокирующе)
                    try:
                        message = message_queue.get_nowait()
                        yield f"data: {json.dumps(message)}\n\n"
                    except queue.Empty:
                        pass
                    
                    time.sleep(0.1)
                    
                except GeneratorExit:
                    break
                except Exception as e:
                    print(f"Ошибка в генераторе ПИТВ сообщений: {str(e)}")
                    time.sleep(1)
                    continue
                    
        except Exception as e:
            print(f"Критическая ошибка в генераторе ПИТВ сообщений: {str(e)}")
        finally:
            # Удаляем callback при закрытии соединения
            if message_callback in pitv_message_callbacks:
                pitv_message_callbacks.remove(message_callback)
            message_logger.remove_callback(message_callback)

    response = Response(
        stream_with_context(generate_messages()), 
        mimetype="text/event-stream"
    )
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"
    response.headers["X-Accel-Buffering"] = "no"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def check_port_free(port):
    """Проверить свободен ли порт"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False


def kill_process_on_port(port):
    """Убить процесс на порту"""
    try:
        import subprocess
        result = subprocess.run(['lsof', '-ti', f':{port}'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                try:
                    subprocess.run(['kill', pid])
                    print(f"[Port Killer] Остановлен процесс {pid} на порту {port}")
                except:
                    pass
            time.sleep(1)  # Даем время процессу завершиться
        return True
    except:
        return False


def start_pitv_server():
    """Запустить сервер приема ПИТВ сообщений"""
    if PITV_AVAILABLE:
        # Проверяем порт 8081
        if not check_port_free(8081):
            print("[Main App] ⚠️  Порт 8081 занят, освобождаем...")
            kill_process_on_port(8081)
            
        print("[Main App] Запуск сервера приема ПИТВ сообщений...")
        success = start_message_receiver_server()
        if success:
            print("[Main App] ✅ Сервер ПИТВ запущен на порту 8081")
            print("[Main App] 🔥 ПРОСТО ШЛИТЕ XML НА http://localhost:8081/ БЕЗ ЭНДПОИНТОВ!")
        else:
            print("[Main App] ❌ Не удалось запустить сервер ПИТВ")
        return success
    else:
        print("[Main App] ⚠️  ПИТВ модули недоступны")
        return False


if __name__ == "__main__":
    print("🚀 === XML GENERATOR WITH PITV MESSAGE RECEIVER ===")
    print("Запуск системы...")
    print()
    
    # Проверяем порт 8080
    if not check_port_free(8080):
        print("[Main App] ⚠️  Порт 8080 занят, освобождаем...")
        kill_process_on_port(8080)
    
    # Запускаем сервер ПИТВ в фоновом режиме
    pitv_started = start_pitv_server()
    
    if pitv_started:
        print("✅ Сервер приема ПИТВ: http://localhost:8081/")
        print("✅ Основное приложение: http://localhost:8080")
        print("✅ Веб-интерфейс: http://localhost:8080 -> вкладка 'Прием сообщений'")
    else:
        print("⚠️  Сервер ПИТВ не запущен, но основное приложение работает")
        print("✅ Основное приложение: http://localhost:8080")
    
    print()
    print("🔥 ГИС ЦПГ должна слать сообщения на: http://ваш-сервер:8081/")
    print("📝 Нажмите Ctrl+C для остановки")
    print("=" * 60)
    
    try:
        # Запускаем основное приложение
        app.run(host="0.0.0.0", port=8080)
    except KeyboardInterrupt:
        print("\n🛑 Завершение работы...")
        if PITV_AVAILABLE:
            stop_message_receiver_server()
        print("✅ Серверы остановлены")
