from pathlib import Path, PosixPath
import os
from config import load_config, base_directory_name

config = load_config()


def create_dirs() -> list[PosixPath]:
    """
    creating output directories on start-up
    :return: the list with directories' paths
    """
    file_dir = Path(base_directory_name)
    files_dir = Path(os.path.join(config.output_directory_name))
    logs_dir = Path(config.logs_directory_name)
    logs_xml_dir = Path(os.path.join(config.logs_directory_name, 'xml_generator'))
    for dir_name in locals().values():
        dir_name.mkdir(exist_ok=True)
