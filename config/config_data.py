import datetime
import os

CHILD_PLAY_UKIO_PROBABILITY = 1  # from 0 to 100
WRONG_CALLS_PROBABILITY = 1  # from 0 to 100

OPERATOR_WAIT_ANSWER_RECALL = 60  # seconds
MAX_RECALL_ATTEMPTS = 2

PHONE_CALL_STRUCTURE_PROBABILITY_IN_UKIO = 50

drop_call_probability: int = 50  # percents from 0 to 100
files_count: int = 100
base_directory_name = 'files'

output_directory_name: str = os.path.join(
    base_directory_name,
    f'file_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}'
)
logs_directory_name: str = 'errors'
date_zero = datetime.datetime(  # can fill: datetime.datetime.now()
    year=2023,
    month=12,
    day=23,
    hour=10,
    minute=30,
    second=1,
    microsecond=252_329  # microsecond must be in 0...999999
)

# constants
AVERAGE_CALL_TIME = 75
CARD_CREATE_TIME_SCALE = 10

AVERAGE_EOS_CARD_CREATE_TIME = 5 * 60  # seconds
EOS_CARD_CREATE_SCALE = 100

AVG_TIME_OPERATOR_RECALL_WAITING = 5
OPERATOR_RECALL_WAITING_SCALE = 2

MAX_TIME_OPERATOR_WAITING = 60
AVG_TIME_OPERATOR_WAITING = 15
OPERATOR_TIME_WAITING_SCALE = 10

OPERATOR_REACTION_TIME = 8
OPERATOR_REACTION_TIME_SCALE = 3

AVG_DEPARTMENT_ANSWER = 15
DEPARTMENT_SCALE = 8

# in %
EOS_SHARE_MIN = 55
EOS_SHARE_MAX = 65

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

PSYCHO_SHARE_MIN = 0
PSYCHO_SHARE_MAX = 5

# other eos timings
CONSULT_TIME = 120  # seconds

AVG_PSYCHO_TIME = 15  # minutes
PSYCHO_SCALE = 5
