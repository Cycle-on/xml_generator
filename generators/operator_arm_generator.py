import random

from constants import ALL_PROJ_CONSTANTS
from generators.random_generators import get_random_telephone_number
from schemas.string_eos import OperatorWork, Operator, Arm


def __generate_arm() -> Arm:
    return Arm(
        strArmNumber=get_random_telephone_number(),
        strArmPlace=random.choice(ALL_PROJ_CONSTANTS['ARM_PLACES']),

    )


def generate_operator_work(operator: Operator, date_from) -> OperatorWork:
    arm = __generate_arm()
    return OperatorWork(
        operator=operator,
        operatorId=operator.operatorId,
        strOperatorStatus=random.choice(ALL_PROJ_CONSTANTS['OPERATOR_STATES']),
        dtAction=date_from,
        arm=arm,
        armId=arm.armId,
        dtSend=date_from
    )


def main():
    pass


if __name__ == '__main__':
    main()
