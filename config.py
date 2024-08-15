from dataclasses import dataclass


@dataclass
class Config:
    dropped_call_probability = 100  # in %


def load_config():
    return Config()
