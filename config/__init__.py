from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated
from config.config_data import *

import argparse

from config.config_data import *
from config import config_data
from constants import generator


def parse_args():
    parser = argparse.ArgumentParser()
    # Добавляем параметры со значениями по умолчанию
    parser.add_argument('--files-count', type=int, default=generator.files_count, help='количество файлов')
    parser.add_argument('--xmls', type=int, default=generator.xml_count_per_file,
                        help='Количество документов в одном файле')
    parser.add_argument('--send', action='store_true', help='Режим генератора')
    parser.add_argument(
        '--date', type=str, default=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
        help='Дата в формате: YYYY-MM-DD_HH-MM-SS'
    )

    # Парсим аргументы
    args = parser.parse_args()
    generator.files_count = args.files_count
    generator.xml_count_per_file = args.xmls
    try:
        config_data.DATE_ZERO = datetime.datetime.strptime(args.date, "%Y-%m-%d_%H-%M-%S")
        return args.send, config_data.DATE_ZERO
    except ValueError:
        print("Дата не соответствует формату YYYY-MM-DD_HH-MM-SS\nРабота прервана")
        quit()


send_files, GLOBAL_DATE = parse_args()


def check_percent_number(number: int) -> bool:
    """
    percents validator
    :param number:
    :return:
    """
    assert 0 <= number <= 100, "call probability must be percents"
    return number


percents = Annotated[int, AfterValidator(check_percent_number)]

missed_info: list[dict] = []
ukios_info: list[dict] = []


class Config(BaseModel):
    dropped_call_probability: percents  # percents
    files_count: int
    logs_directory_name: str
    output_directory_name: str
    date_zero: datetime.datetime
    low_date: datetime.datetime
    send_files: bool


_config = None


def load_config() -> Config:
    global _config
    if _config is None:
        _config = Config(
            dropped_call_probability=DROP_CALL_PROBABILITY,
            files_count=files_count,
            logs_directory_name=logs_directory_name,
            output_directory_name=output_directory_name,
            date_zero=GLOBAL_DATE,
            low_date=datetime.datetime(1, 1, 1, hour=1, minute=0, second=0),
            send_files=send_files,
        )

    return _config
