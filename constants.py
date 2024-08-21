xml_count = 1000  # Количество записей в одном файле
files_count = 1  # Количество файлов
files_prefix = 'ukio'  # префикс перед global_id в ukio и call

OPERATOR_WAIT_ANSWER_RECALL = 60  # секунды, время дозвона со стороны оператора при обратном вызове
MAX_RECALL_ATTEMPTS = 3  # максимальное количество попыток перезвона при сброшенном вызове

DATE_ZERO_FORMAT = "2023-10-23_10-30-10"  # формат: YYYY-MM-DD_HH-MM-SS

DELAY_BETWEEN_CALLS = 5  # секунды, задержка между каждым вызовом
# константы с припиской _SCALE - среднеквадратичное отклонение

# other eos timings
CONSULT_TIME = 120  # секунды, время консультации

AVG_PSYCHO_TIME = 15  # минуты, среднее время психологической поддержки
PSYCHO_SCALE = 5

AVERAGE_CALL_TIME = 75  # секунды, среднее время вызова/составления карточки/dtConnect - dtEndCall
CARD_CREATE_TIME_SCALE = 10

AVERAGE_EOS_CARD_CREATE_TIME = 300  # секунды, среднее время составления карточки со стороны службы/dtCreate
EOS_CARD_CREATE_SCALE = 8

AVG_TIME_OPERATOR_RECALL_WAITING = 5  # секунды, среднее время задержки перед обратным вызовом/dtCall
OPERATOR_RECALL_WAITING_SCALE = 2

AVG_TIME_OPERATOR_WAITING = 15  # секунды, среднее время в течение которого отвечает человек при обратном вызове/dtConnect
OPERATOR_TIME_WAITING_SCALE = 10

OPERATOR_REACTION_TIME = 8  # секунды, время реакции оператора на вызов
OPERATOR_REACTION_TIME_SCALE = 3

AVG_DEPARTMENT_ANSWER = 15  # среднее время ответа службы(используется только в card04->dtConfirm)
DEPARTMENT_SCALE = 8

# все вероятности в процентах от 0 до 100
CALLS_WITHOUT_ANSWER_PROBABILITY = 10  # вероятность вызова без ответа оператора

CHILD_PLAY_UKIO_PROBABILITY = 10  # вероятность детской шалости
WRONG_CALLS_PROBABILITY = 10  # вероятность ложного вызова

DROP_CALL_PROBABILITY = 20  # Вероятность того что вызов будет сброшен

# in %
EOS_SHARE_MIN = 55  # две вероятности выпадения службы
EOS_SHARE_MAX = 65  # будет выбираться рандомное значение из этих двух

# main eos in %
FIRE_SHARE_MIN = 2
FIRE_SHARE_MAX = 10

POLICE_SHARE_MIN = 15
POLICE_SHARE_MAX = 25

AMBULANCE_SHARE_MIN = 55
AMBULANCE_SHARE_MAX = 70

GAS_SHARE_MIN = 0
GAS_SHARE_MAX = 10

CARD_CS_SHARE_MIN = 0
CARD_CS_SHARE_MAX = 5

CARD_AT_SHARE_MIN = 0
CARD_AT_SHARE_MAX = 2
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
