from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

from config.config_data import *


def check_percent_number(number: int) -> bool:
    assert 0 <= number <= 100, "call probability must be percents"
    return number


percents = Annotated[int, AfterValidator(check_percent_number)]


class Config(BaseModel):
    dropped_call_probability: percents  # percents
    files_count: int
    logs_directory_name: str
    output_directory_name: str


def load_config() -> Config:
    return Config(
        dropped_call_probability=drop_call_probability,
        files_count=files_count,
        logs_directory_name=logs_directory_name,
        output_directory_name=output_directory_name,
    )


def main():
    c = load_config()
    print(c)


if __name__ == '__main__':
    main()