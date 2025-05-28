import base64
import io
import os
import sys
import tracemalloc

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
import time
from threading import Thread

from dotenv import load_dotenv

from config import missed_info, ukios_info
from constants import *
from constants import ALL_PROJ_CONSTANTS
from constants.constants_remaker import get_next_constants
from main import clear_dir, generate_region_files, main

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

# Глобальные переменные для управления автоматической генерацией
auto_generation_thread = None
auto_generation_running = False
auto_generation_start_time = None
auto_generation_end_time = None
auto_generation_interval = None
total_files_sent = 0
log_callbacks = []
is_generating = False


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
    return render_template("index.html")


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

            # Для каждого сгенерированного региона ищем соответствующий логин/пароль и отправляем файлы
            for region in generated_regions:
                if not auto_generation_running:
                    break

                print(f"DEBUG: Обработка региона: {region}")
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
                            log_message(
                                {
                                    "type": "error",
                                    "message": f"Ошибка при отправке файла {filename}: {response.status_code}",
                                }
                            )

                    except Exception as e:
                        print(f"DEBUG: Ошибка при обработке файла {filename}: {str(e)}")
                        log_message(
                            {
                                "type": "error",
                                "message": f"Ошибка при обработке файла {filename}: {str(e)}",
                            }
                        )

            # Генерация завершена
            print("DEBUG: Цикл генерации завершен")
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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
