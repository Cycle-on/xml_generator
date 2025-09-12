# План параллельной реализации генератора ЦПГ

## Цель
Создать параллельный функционал генерации карточек в формате ЦПГ, не затрагивая существующий функционал ЦССИ.

## Принципы реализации
- **НЕ ТРОГАЕМ** существующий код ЦССИ
- Все новые файлы имеют суффикс `_cpg`
- Можно переключаться между режимами ЦССИ и ЦПГ
- Максимальное переиспользование существующей логики генерации

## ЭТАП 1: Создание моделей данных ЦПГ
**Результат этапа: Pydantic модели для всех структур ЦПГ**

### Шаг 1.1: Создать файл `schemas/cpg_models.py`
```python
# Базовые структуры
class CPGOperator  # из Operator WSDL
class CPGCoords    # из Coords WSDL  
class CPGAddress   # из Address WSDL
class CPGLocation  # из Location WSDL

# Основные структуры карточки
class CPGCommonData  # из CommonData WSDL
class CPGDdsData01   # из DdsData01 WSDL
class CPGCard        # из Card WSDL

# Структуры обращения (Ier)
class CPGFullName    # из FullName WSDL
class CPGSmsIer      # из SmsIer WSDL
class CPGEraCallCard # из EraCallCard WSDL
class CPGIer         # из Ier WSDL

# Сообщения (операции)
class UpdateCardRequest   # Обертка для Card + Ier
class UpdateCardResponse  # Ответ системы
```

### Шаг 1.2: Настроить дефолтные значения для новых полей
- `SysCode = "XML_GEN_112"`
- `ExtId = lambda: f"EXT_{uuid.uuid4().hex[:8].upper()}"`
- `HrId = lambda: f"INC-{random.randint(10000, 99999)}"`
- `RegionStr = "Московская область"`
- `IerType = 1`
- Все остальные новые поля = None или пустые строки

## ЭТАП 2: Создание конвертера ЦССИ → ЦПГ
**Результат этапа: Функционирующий конвертер Ukio в Card + Ier**
**🎯 ПОСЛЕ ЭТОГО ЭТАПА МОЖНО ГЕНЕРИРОВАТЬ ПЕРВУЮ КАРТОЧКУ ЦПГ**

### Шаг 2.1: Создать файл `converters/ukio_to_cpg.py`

```python
def convert_ukio_to_cpg(ukio: Ukio) -> tuple[CPGCard, CPGIer]:
    """Главная функция конвертации"""
    card = _create_card_from_ukio(ukio)
    ier = _create_ier_from_ukio(ukio)
    return card, ier
```

### Шаг 2.2: Реализовать маппинг полей по таблицам соответствия

#### Функция `_create_card_from_ukio(ukio)`:
```python
# Маппинг по таблице "Структуры данных.csv"
Id112 = ukio.globalId
ExtId = генерировать новый
Location = _map_location(ukio.address)
CommonData = _extract_common_data(ukio)
DdsData01 = _convert_card01_to_dds(ukio.card01) if ukio.card01 else None
CreateOperator = _map_operator(первый оператор из ukio)
LastChangeOperator = _map_operator(последний оператор)
IncidentState = ukio.strCardState
Created = ukio.dtCreate.isoformat() if ukio.dtCreate else None
Changed = ukio.dtUpdate.isoformat() if ukio.dtUpdate else None
```

#### Функция `_create_ier_from_ukio(ukio)`:
```python
# Маппинг обращения
Id = генерировать новый
IerIsoTime = ukio.phoneCall[0].dtCall.isoformat() if ukio.phoneCall else None
CgPn = ukio.callContent.strCgPN if ukio.callContent else None
FullName = _extract_fullname(ukio.callContent)
AcceptOperator = _map_operator(ukio.phoneCall[0].operator if ukio.phoneCall else None)
Era = _map_era(ukio.era) if ukio.era else None
Sms = _map_sms(ukio.sms[0]) if ukio.sms else None
IerType = 1  # константа
Location = _map_location(ukio.callContent.appResAddress if ukio.callContent else None)
```

### Шаг 2.3: Реализовать вспомогательные функции маппинга

```python
def _map_location(address):
    """Конвертация Address ЦССИ в Location ЦПГ"""
    
def _extract_common_data(ukio):
    """Извлечение CommonData из Ukio"""
    
def _convert_card01_to_dds(card01):
    """Конвертация Card01 в DdsData01"""
    
def _map_operator(operator):
    """Маппинг оператора"""
    
def _extract_fullname(call_content):
    """Извлечение ФИО из CallContent"""
```

## ЭТАП 3: Создание XML генератора для ЦПГ
**Результат этапа: Генерация валидного XML по схеме ЦПГ**

### Шаг 3.1: Создать файл `file_creator_cpg.py`

```python
def create_cpg_xml_file(card: CPGCard, ier: CPGIer, filename: str):
    """Создает XML файл в формате ЦПГ"""
    # Создаем UpdateCardRequest
    request = UpdateCardRequest(
        SysCode="XML_GEN_112",
        Card=card,
        Ier=ier
    )
    # Генерируем XML с namespace http://tspg.service/
    xml = _generate_xml_from_cpg_model(request)
    # Сохраняем в файл
    _save_xml_to_file(xml, filename)
```

### Шаг 3.2: Адаптировать генератор XML под новый namespace

```python
def _generate_xml_from_cpg_model(model, namespace="http://tspg.service/"):
    """Рекурсивная генерация XML из Pydantic модели"""
    # Похоже на __generate_xml_from_pydantic из file_creator.py
    # НО с новым namespace и без префикса s112
```

## ЭТАП 4: Интеграция с существующим генератором
**Результат этапа: Полноценная генерация карточек ЦПГ через существующую логику**

### Шаг 4.1: Создать файл `generators/cpg_generator.py`

```python
from generators.ukio_generator import generate_ukio_phone_call_data
from converters.ukio_to_cpg import convert_ukio_to_cpg

def generate_cpg_card_data(call_date):
    """Генерирует данные карточки ЦПГ используя логику ЦССИ"""
    # Используем существующий генератор
    ukio = generate_ukio_phone_call_data(call_date)
    if ukio is None:
        return None, None
    
    # Конвертируем в ЦПГ формат
    card, ier = convert_ukio_to_cpg(ukio)
    return card, ier
```

### Шаг 4.2: Создать файл `main_cpg.py`

```python
def generate_cpg_files(date_zero, region_name="rsc-region-05"):
    """Главная функция генерации файлов ЦПГ"""
    # Похоже на generate_region_files из main.py
    # НО:
    # - использует generate_cpg_card_data вместо generate_ukio_phone_call_data
    # - использует create_cpg_xml_file вместо create_file_from_model
    # - сохраняет в директорию files_cpg/ вместо files/
```

### Шаг 4.3: Добавить переключатель режимов в основной main.py

```python
# В main.py добавить аргумент командной строки
parser.add_argument('--mode', choices=['cssi', 'cpg'], default='cssi')

if args.mode == 'cpg':
    from main_cpg import generate_cpg_files
    generate_cpg_files(...)
else:
    # существующая логика ЦССИ
    generate_region_files(...)
```

## ЭТАП 5: Тестирование и валидация
**Результат этапа: Уверенность в корректности генерации**

### Шаг 5.1: Создать скрипт валидации `tests/validate_cpg_xml.py`

```python
def validate_cpg_xml(xml_file_path):
    """Валидация XML по WSDL схеме ЦПГ"""
    # Использует cpg_wsdl_1.wsdl для проверки
    # Проверяет обязательные поля
    # Проверяет структуру
```

### Шаг 5.2: Создать тест конвертации `tests/test_ukio_to_cpg.py`

```python
def test_conversion_preserves_data():
    """Проверка что конвертация не теряет данные"""
    # Создаем тестовый Ukio
    # Конвертируем в CPG
    # Проверяем все замапленные поля
```

### Шаг 5.3: Генерация тестового набора файлов

```bash
python main.py --mode cpg --files-count 5 --xmls 10
```
Проверить что:
- Файлы создаются
- XML валидный
- Структура соответствует WSDL

## ЭТАП 6: Документация использования
**Результат этапа: Понятная инструкция для пользователей**

### Шаг 6.1: Создать `README_CPG.md`
- Описание режима ЦПГ
- Как запускать
- Примеры сгенерированных файлов
- Список поддерживаемых полей

### Шаг 6.2: Добавить примеры в `examples/cpg/`
- Пример Card
- Пример Ier
- Пример полного UpdateCardRequest

## Контрольные точки

✅ **После ЭТАПА 2** - можно сгенерировать первую карточку ЦПГ (с тестовыми данными)
✅ **После ЭТАПА 3** - можно сохранить карточку в XML файл
✅ **После ЭТАПА 4** - полноценная генерация с существующей логикой
✅ **После ЭТАПА 5** - уверенность в корректности
✅ **После ЭТАПА 6** - готово к использованию

## Структура файлов проекта после реализации

```
xml_generator/
├── schemas/
│   ├── ukio_model.py         (НЕ ТРОГАЕМ)
│   └── cpg_models.py          (НОВЫЙ)
├── converters/
│   └── ukio_to_cpg.py         (НОВЫЙ)
├── generators/
│   ├── ukio_generator.py      (НЕ ТРОГАЕМ)
│   └── cpg_generator.py       (НОВЫЙ)
├── file_creator.py            (НЕ ТРОГАЕМ)
├── file_creator_cpg.py        (НОВЫЙ)
├── main.py                    (МИНИМАЛЬНЫЕ ИЗМЕНЕНИЯ - добавить аргумент)
├── main_cpg.py                (НОВЫЙ)
├── tests/
│   ├── validate_cpg_xml.py    (НОВЫЙ)
│   └── test_ukio_to_cpg.py    (НОВЫЙ)
├── examples/cpg/              (НОВАЯ ДИРЕКТОРИЯ)
├── README.md                  (НЕ ТРОГАЕМ)
└── README_CPG.md              (НОВЫЙ)
```

## Команды для запуска

```bash
# Генерация в режиме ЦССИ (по умолчанию)
python main.py

# Генерация в режиме ЦПГ
python main.py --mode cpg

# Генерация ЦПГ с параметрами
python main.py --mode cpg --files-count 10 --xmls 50

# Валидация сгенерированных ЦПГ файлов
python tests/validate_cpg_xml.py files_cpg/*.xml
```