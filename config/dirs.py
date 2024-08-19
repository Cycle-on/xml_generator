from pathlib import Path, PosixPath
import os
from config import load_config

config = load_config()


def create_dirs() -> list[PosixPath]:
    """
    creating output directories on start-up
    :return: the list with directories' paths
    """
    files_dir = Path(config.output_directory_name)
    logs_dir = Path(config.logs_directory_name)
    logs_xml_dir = Path(os.path.join(config.logs_directory_name, 'xml_generator'))
    ukio_dir = Path(os.path.join(config.output_directory_name, 'ukios'))
    calls_dir = Path(os.path.join(config.output_directory_name, 'calls'))
    for dir_name in locals().values():
        dir_name.mkdir(exist_ok=True)
