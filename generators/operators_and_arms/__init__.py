import datetime
import random
from copy import deepcopy

from config import load_config
from constants import ALL_PROJ_CONSTANTS
from generators import check_event_probability
from generators.random_generators import get_random_name, get_random_telephone_number
from schemas.string_eos import Arm, ArmWork, Operator, OperatorWork

config = load_config()

OPERATORS_COUNT = random.randint(
    ALL_PROJ_CONSTANTS["MIN_OPERATORS_COUNT"], ALL_PROJ_CONSTANTS["MAX_OPERATORS_COUNT"]
)


def create_operator() -> Operator:
    operator_gender = (
        "M"
        if check_event_probability(ALL_PROJ_CONSTANTS["OPERATOR_MALE_PROBABILITY"])
        else "F"
    )
    surname, name, last_name = get_random_name(operator_gender)
    return Operator(
        strOperatorLastName=last_name,
        strOperatorName=name,
        strOperatorSurname=surname,
        strOperatorPost=random.choice(ALL_PROJ_CONSTANTS["OPERATORS_POSTS"]),
        isPsychologist=check_event_probability(
            ALL_PROJ_CONSTANTS["OPERATOR_PSYCHOLOGIST_PROBABILITY"]
        ),
        bOperatorTranslator=check_event_probability(
            ALL_PROJ_CONSTANTS["OPERATOR_TRANSLATOR_PROBABILITY"]
        ),
        strLanguage=["Русский", "Английский"],
    )


OPERATOR_SHIFT = {"free_operators": [], "busy_operators": [], "shift": 0}
ALL_PROJ_CONSTANTS["OPERATOR_SHIFT"] = OPERATOR_SHIFT
OPERATORS: list[OPERATOR_SHIFT] = [
    deepcopy(ALL_PROJ_CONSTANTS["OPERATOR_SHIFT"]) for _ in range(4)
]
ALL_PROJ_CONSTANTS["OPERATORS"] = OPERATORS
if (
    ALL_PROJ_CONSTANTS["OPERATORS_COUNT_PER_WORKING_SHIFT"]
    > ALL_PROJ_CONSTANTS["ARMS_COUNT"]
):
    print("Число операторов больше чем число армов")
    quit()

ALL_OPERATORS = []
ALL_PROJ_CONSTANTS["ALL_OPERATORS"] = ALL_OPERATORS


def create_operators():
    for shift in range(1, 4):
        ALL_PROJ_CONSTANTS["OPERATORS"][shift]["shift"] = shift
        ALL_PROJ_CONSTANTS["OPERATORS"][shift]["start_shift"] = (
            config.date_zero
            + datetime.timedelta(seconds=ALL_PROJ_CONSTANTS["SHIFT_TIME"] * shift)
        )
        for _ in range(ALL_PROJ_CONSTANTS["OPERATORS_COUNT_PER_WORKING_SHIFT"]):
            op = create_operator()
            ALL_PROJ_CONSTANTS["ALL_OPERATORS"].append(op)
            ALL_PROJ_CONSTANTS["OPERATORS"][shift]["free_operators"].append(
                {
                    "operator": op,
                    "start_time": config.low_date,
                    "end_time": config.low_date,
                    "shift": shift,
                }
            )


ARMS = []


def create_arm() -> Arm:
    return Arm(
        strArmNumber=get_random_telephone_number(),
        strArmPlace=random.choice(["ЦОВ", "РЦОВ"]),
    )


def create_arms():
    for _ in range(ALL_PROJ_CONSTANTS["ARMS_COUNT"]):
        ARMS.append(create_arm())


OPERATOR_WORK = []


def create_operator_work():
    for i, operator in enumerate(ALL_OPERATORS):
        OPERATOR_WORK.append(
            OperatorWork(
                strOperatorStatus="Вошел в систему",
                operator=operator,
                arm=ARMS[i],
                dtAction=config.date_zero,
            )
        )


ARM_WORK = []


def create_arm_work():
    for arm in ARMS:
        ARM_WORK.append(
            ArmWork(
                arm=arm,
                strArmStatus="доступен",
                dtAction=config.date_zero,
            )
        )


SHIFT = 1


def check_busy_operators(call_time: datetime.datetime) -> None:
    busy_operators = OPERATORS[SHIFT]["busy_operators"]
    for operator_info in busy_operators:
        if operator_info["end_time"] <= call_time and operator_info["shift"] == SHIFT:
            OPERATORS[SHIFT]["free_operators"].append(operator_info)
            OPERATORS[SHIFT]["busy_operators"].remove(operator_info)


def check_shift_time():
    global SHIFT
    if config.date_zero >= OPERATORS[SHIFT + 1]["start_shift"]:
        SHIFT += 1


def get_operator(call_time: datetime.datetime) -> Operator | None:
    free_operators = OPERATORS[SHIFT]["free_operators"]
    if len(free_operators) == 0:
        check_busy_operators(call_time)
    if len(free_operators) == 0:
        return None
    random_operator = random.choice(free_operators)
    OPERATORS[SHIFT]["free_operators"].remove(
        random_operator
    )  # delete from free operators
    OPERATORS[SHIFT]["busy_operators"].append(random_operator)  # add to busy operators
    check_shift_time()
    return random_operator


def create_arms_and_operators():
    create_operators()
    create_arms()
    create_arm_work()
    create_operator_work()


def main():
    create_arms_and_operators()


if __name__ == "__main__":
    main()
