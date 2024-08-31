xml_count_per_file = 1  # Количество записей в одном файле
files_count = 10000  # Количество файлов
files_prefix = 'TEST'  # префикс перед global_id в ukio и call
SERVER_ADDRESS = '0.0.0.0'
# google sheets table information
SHEET_ID = '1bVCN8REheC7NrINGyiB3s837J6VmkOiwufSbyHztA4c'
INCIDENT_TYPES_LIST_NAME = 'IncidentTypes'
ADDRESSES_LIST_NAME = 'Addresses'

MAX_RECALL_ATTEMPTS = 3  # максимальное количество попыток перезвона при сброшенном вызове
DATE_ZERO_FORMAT = "2024-08-31_20-38-00"  # формат: YYYY-MM-DD_HH-MM-SS

AVG_DELAY_BETWEEN_CALLS_TIME = 5  # секунды, задержка между каждым вызовом

OPERATOR_STATES = ['вошел в систему', 'вышел из системы']
ARM_PLACES = ["ЦОВ", "РЦОВ", "ЕДДС", "ДДС 01", "ДДС 02", "ДДС 03", "ДДС 04", "ДДС АТ", "ДДС ЖКХ", "другое"]
# константы с припиской _SCALE - среднеквадратичное отклонение
# other eos timings
CALL_CONTENT_APPLICANT_MALE_PROBABILITY = 50
CALL_NUMBER_APPLICANT_NUMBER_EQUALITY_PROBABILITY = 30
INCIDENT_DESCRIPTIONS = ["desc1", "desc2"]

OPERATOR_WAIT_ANSWER_RECALL_WORK_TYPE = 'normal'
AVG_OPERATOR_WAIT_ANSWER_RECALL_TIME = 60  # секунды, время дозвона со стороны оператора при обратном вызове
OPERATOR_WAIT_ANSWER_RECALL_SCALE = 4

CONSULT_WORK_TYPE = 'normal'
AVG_CONSULT_TIME = 120  # секунды, время консультации
CONSULT_SCALE = 8

PSYCHO_WORK_TYPE = 'normal'
AVG_PSYCHO_TIME = 15  # минуты, среднее время психологической поддержки
PSYCHO_SCALE = 5
PSYCHO_IN_HOUSE_PROBABILITY = 50  # в процентах от 0 до 100

CARD_CREATE_WORK_TYPE = 'normal'
AVG_CARD_CREATE_TIME = 75  # секунды, среднее время вызова/составления карточки/dtConnect - dtEndCall
CARD_CREATE_SCALE = 10

EOS_CARD_CREATE_WORK_TYPE = 'normal'
AVG_EOS_CARD_CREATE_TIME = 300  # секунды, среднее время составления карточки со стороны службы/dtCreate
EOS_CARD_CREATE_SCALE = 8

OPERATOR_RECALL_WAITING_WORK_TYPE = 'normal'
AVG_OPERATOR_RECALL_WAITING_TIME = 5  # секунды, среднее время задержки перед обратным вызовом/dtCall
OPERATOR_RECALL_WAITING_SCALE = 2

OPERATOR_WAITING_WORK_TYPE = 'normal'
AVG_OPERATOR_WAITING_TIME = 15  # секунды, среднее время в течение которого отвечает человек при обратном вызове/dtConnect
OPERATOR_WAITING_SCALE = 10

OPERATOR_REACTION_WORK_TYPE = 'normal'
AVG_OPERATOR_REACTION_TIME = 8  # секунды, время реакции оператора на вызов
OPERATOR_REACTION_SCALE = 3

AVG_DEPARTMENT_ANSWER_TIME = 15  # среднее время ответа службы(используется только в card04->dtConfirm)
DEPARTMENT_SCALE = 8

# все вероятности в процентах от 0 до 100
CALLS_WITHOUT_ANSWER_PROBABILITY = 10  # вероятность вызова без ответа оператора

CHILD_PLAY_UKIO_PROBABILITY = 5  # вероятность детской шалости
WRONG_CALLS_PROBABILITY = 5  # вероятность ложного вызова

DROP_CALL_PROBABILITY = 20  # Вероятность того что вызов будет сброшен
# Eos Type info
EOS_ITEM_CANCEL_PROBABILITY = 10  # проценты

DT_DEPART_WORK_TYPE = 'normal'
AVG_DT_DEPART = 60  # секунды
DT_DEPART_SCALE = 30

DT_DEPART_CONFIRM_WORK_TYPE = 'normal'
AVG_DT_DEPART_CONFIRM = 60  # секунды
DT_DEPART_CONFIRM_SCALE = 30

DT_ARRIVAL_WORK_TYPE = 'normal'
AVG_DT_ARRIVAL = 60  # секунды
DT_ARRIVAL_SCALE = 30

DT_COMPLETE_WORK_TYPE = 'normal'
AVG_DT_COMPLETE = 60  # секунды
DT_COMPLETE_SCALE = 30

DT_CANCEL_WORK_TYPE = 'normal'
AVG_DT_CANCEL = 60  # секунды
DT_CANCEL_SCALE = 30

# Eos Resource
MEMBERSHIP = ["mem1", "mem2", "mem3"]

# in %
EOS_SHARE_MIN = 55  # две вероятности выпадения службы
EOS_SHARE_MAX = 65  # будет выбираться рандомное значение из этих двух

# main eos in %
FIRE_SHARE_MIN = 2
FIRE_SHARE_MAX = 10

INCIDENT_TYPES_FOR_CARD01 = []
OBJECT_FOR_CARD01 = ["01obj1", "01obj2"]
INCIDENT_STOREY = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
OBJECT_GASIFIED_PROBABILITY = 60  # проценты
ESTIMATION = 2  # минуты
ESTIMATION_SCALE = 1
OBSERVED_CONSEQUENCES_FIRE = ['разрушение Перекрытий', 'обрушение кровли']
ROADS_CHARACTERS = ["Пробки", 'скопление автомобилей во дворах']
WORKING_CONDITIONS_CHARACTERS = ["нахождение объекта в огражденной", "охраняемой зоне", "наличие ворот", "шлагбаумов",
                                 "решеток и жалюзи на окнах"]
NEED_RESCUE_WORK_PROBABILITY = 20  # проценты
EVACUATIONS_POSSIBILITIES = ["наличие незадымленных лестничных клеток", "лестниц между балконами", "открытых галерей"]
OWNERS_INFO = ["номер-имя1 номер-имя2", "номер-имя2 номер-имя2"]
# police info
POLICE_SHARE_MIN = 15
POLICE_SHARE_MAX = 25
INCIDENT_TYPES_FOR_CARD02 = []

OFFENDERS_NUMBER_WORK_TYPE = 'normal'
AVG_OFFENDERS_NUMBER = 5
OFFENDERS_NUMBER_SCALE = 1

VEHICLE_NUMBER_WORK_TYPE = 'normal'
AVG_VEHICLE_NUMBER = 5
VEHICLE_NUMBER_SCALE = 1

# suspect
HOW_MANY_SUSPECTS_WORK_TYPE = 'normal'
AVG_HOW_MANY_SUSPECTS = 5
HOW_MANY_SUSPECTS_SCALE = 1
SUSPECT_MALE_GENDER_PROBABILITY = 50  # Вероятность того, что подозреваемый мужского пола

SUSPECT_AGE_WORK_TYPE = 'normal'
AVG_SUSPECT_AGE = 27
SUSPECT_AGE_SCALE = 1

HEIGHT_TYPES = ["Рост 1", "Рост 2"]
BODY_TYPES = ["Тип тела 1", 'тип тела 2', 'тип тела 3']
DRESSES = ["одежда1", "одежда2", 'одежда3']
SPECIAL_SIGNS = ['спец знак 1', 'спец знак 2']
# Wanted Person
HOW_MANY_WANTED_WORK_TYPE = 'normal'
AVG_HOW_MANY_WANTED = 4
HOW_MANY_WANTED_SCALE = 1

WANTED_MALE_GENDER_PROBABILITY = 50

WANTED_AGE_WORK_TYPE = 'normal'
AVG_WANTED_AGE = 30
WANTED_AGE_SCALE = 3
# vehicles
VEHICLES_COUNT_WORK_TYPE = 'normal'
AVG_VEHICLES_COUNT = 3
VEHICLES_COUNT_SCALE = 1

VEHICLE_TYPES = ["vehicle type 1", "vehicle type 2"]
VEHICLE_COLORS = ["color1", "color2"]
VEHICLE_NUMBERS = ["number1", "number2"]
VEHICLE_REGIONS = ["region 1", "region2 "]
VEHICLE_HIDDEN_PROBABILITY = 30

# ambulance info
AMBULANCE_SHARE_MIN = 55
AMBULANCE_SHARE_MAX = 70

PATIENTS_COUNT_WORK_TYPE = 'normal'
AVG_PATIENTS_COUNT = 5
PATIENTS_COUNT_SCALE = 1

INCIDENT_TYPES_FOR_CARD03 = []
WHO_CALLED = ['прохожий', 'родственник']
AMBULANCE_CONSULT_PROBABILITY = 50

AMBULANCE_MALE_PROBABILITY = 50

AMBULANCE_AGE_WORK_TYPE = 'normal'
AVG_AMBULANCE_AGE = 30
AMBULANCE_AGE_SCALE = 1

OCCASION_TYPES = ["повод 1", 'повод2']
ABILITY_MOVE_INDEPENDENTLY = ['ability1', 'ability2']

# card 04 info
GAS_SHARE_MIN = 0
GAS_SHARE_MAX = 10
GAS_INCIDENT_TYPES = []
GAS_INSTRUCTIONS = ['instruction1', 'instruction2']
GAS_CONSULT_PROBABILITY = 50

# card comm serv info
CARD_CS_SHARE_MIN = 0
CARD_CS_SHARE_MAX = 5
CS_INCIDENT_TYPES = []
C_S = ['служба 1', 'служба 2']
CS_INSTRUCTIONS = ['instruction 1', 'instruction 2']
CS_CONSULT_PROBABILITY = 50

SERVICES_COUNT_WORK_TYPE = 'normal'
AVG_SERVICES_COUNT = 3
SERVICES_COUNT_SCALE = 1

CS_SERVICES = ['service1', 'service2', 'service3']
CS_APPEALS = ['appeal 1', 'appeal 2']
# Anti Terror card info
CARD_AT_SHARE_MIN = 0
CARD_AT_SHARE_MAX = 2
AT_INCIDENT_TYPES = []

PERISHED_PEOPLE_WORK_TYPE = 'normal'
AVG_PERISHED_PEOPLE = 3
PERISHED_PEOPLE_SCALE = 1

AFFECTED_PEOPLE_WORK_TYPE = 'normal'
AVG_AFFECTED_PEOPLE = 3
AFFECTED_PEOPLE_SCALE = 1

SUSPECT_PEOPLE_WORK_TYPE = 'normal'
AVG_SUSPECT_PEOPLE = 3
SUSPECT_PEOPLE_SCALE = 1
SUSPECT_DESCRIPTION = ['desc1', 'desc2']

ARMAMENTS_WORK_TYPE = 'normal'
AVG_ARMAMENTS = 3
ARMAMENTS_SCALE = 1
ARMAMENTS = ['arma1', 'arma2']
DIRECTION_TYPES = ['dir1', 'dir2']
AT_INJURIES = ['inj1', 'inj2']

# other eos in %
MCHS_SHARE_MIN = 0
MCHS_SHARE_MAX = 1

EDDS_SHARE_MIN = 0
EDDS_SHARE_MAX = 1

ROSGV_SHARE_MIN = 0
ROSGV_SHARE_MAX = 1

AVIALES_SHARE_MIN = 0
AVIALES_SHARE_MAX = 1

ROSAVTODOR_SHARE_MIN = 0
ROSAVTODOR_SHARE_MAX = 1

ROSLESHOZ_SHARE_MIN = 0
ROSLESHOZ_SHARE_MAX = 1

CONSULT_SHARE_MIN = 5
CONSULT_SHARE_MAX = 10

PSYCHO_SHARE_MIN = 5
PSYCHO_SHARE_MAX = 10

""""⌄⌄⌄ ❌DONT TOUCH ❌⌄⌄⌄"""
ALL_PROJ_CONSTANTS = globals()
