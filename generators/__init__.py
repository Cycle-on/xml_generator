import datetime
from datetime import timedelta as td
import random
from typing import TypeVar

import numpy as np

from config import ALL_PROJ_CONSTANTS


def check_event_probability(p1, p2=None) -> bool:
    """
    function takes random probability from [p1, p2] and uses it to check event probability
    *p2>p1
    :param p1: first probability
    :param p2: second probability
    :return:
    """
    if p2 is None:
        p2 = p1
    event_probability = random.randint(p1, p2)
    if random.randint(1, 100) <= event_probability:
        return True
    return False


S = TypeVar("S", "poisson", "uniform", "normal")


def get_distribution_var_by_work_type(work_type: S, var_name: str) -> int | float:
    match work_type:
        case "poisson":
            try:
                return abs(np.random.poisson(
                    ALL_PROJ_CONSTANTS.get(f"{var_name}_LAMBDA")
                ))
            except Exception:
                raise AttributeError(f"Не задано значение лямбды для переменной {var_name}")
        case "normal":
            try:
                return abs(np.random.normal(
                    ALL_PROJ_CONSTANTS.get(f"AVG_{var_name}_TIME"),
                    ALL_PROJ_CONSTANTS.get(f"{var_name}_SCALE")

                ))
            except Exception:
                raise AttributeError(
                    f"Не заданы значения для нормального распределения у переменной {var_name}"
                )

        case "uniform":
            try:
                return abs(np.random.uniform(
                    ALL_PROJ_CONSTANTS.get(f"{var_name}_LOW"),
                    ALL_PROJ_CONSTANTS.get(f"{var_name}_HIGH"),
                ))
            except Exception:
                raise AttributeError(
                    f"Не заданы значения для равномерного распределения у переменной {var_name}"
                )


def get_random_birth_date_by_year(year: int):
    start = datetime.datetime(year=year, month=1, day=1)
    end = datetime.datetime(year=year, month=12, day=31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + td(days=random_days)
