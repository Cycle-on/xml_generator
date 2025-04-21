import argparse
import datetime
from datetime import timedelta as td

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

from config import config_data
from config.config_data import logs_directory_name, output_directory_name, base_directory_name
from constants import ALL_PROJ_CONSTANTS


def parse_args():
    parser = argparse.ArgumentParser()
    # Добавляем параметры со значениями по умолчанию
    # parser.add_argument('--files-count', type=int, default=generator.files_count, help='количество файлов')
    # parser.add_argument('--xmls', type=int, default=generator.xml_count_per_file,
    #                     help='Количество документов в одном файле')
    parser.add_argument('--send', action='store_true', help='Режим генератора')
    parser.add_argument(
        '--date', type=str, default=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f'),
        help='Дата в формате: YYYY-MM-DD_HH-MM-SS'
    )

    # Парсим аргументы
    args = parser.parse_args()

    # ALL_PROJ_CONSTANTS["files_count"] = args.files_count
    # ALL_PROJ_CONSTANTS['xml_count_per_file'] = args.xmls
    # if args.send:
    #     print(args.files_count)
    #     ALL_PROJ_CONSTANTS["files_count"] *= random.randint(sender.COEF_MIN, sender.COEF_MAX) / 100
    #     ALL_PROJ_CONSTANTS["files_count"] = int(generator.files_count)
    #     print("ff", ALL_PROJ_CONSTANTS["files_count"])
    try:
        config_data.DATE_ZERO = datetime.datetime.strptime(args.date, "%Y-%m-%d_%H-%M-%S-%f") - td(hours=3)
        return args.send, config_data.DATE_ZERO
    except ValueError:
        print("Дата не соответствует формату YYYY-MM-DD_HH-MM-SS\nРабота прервана")
        quit()


__send_files, GLOBAL_DATE = parse_args()


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
    base_directory_name: str


_config = None


def load_config() -> Config:
    global _config
    if _config is None:
        _config = Config(
            dropped_call_probability=ALL_PROJ_CONSTANTS['DROP_CALL_PROBABILITY'],
            files_count=ALL_PROJ_CONSTANTS['files_count'],
            logs_directory_name=logs_directory_name,
            output_directory_name=output_directory_name,
            date_zero=GLOBAL_DATE,
            low_date=datetime.datetime(1, 1, 1, hour=1, minute=0, second=0),
            send_files=__send_files,
            base_directory_name=base_directory_name,
        )

    return _config
