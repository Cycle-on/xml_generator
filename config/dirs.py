import os
import shutil
from pathlib import Path, PosixPath

from config import load_config

config = load_config()


def create_dirs() -> list[PosixPath]:
    """
    creating output directories on start-up
    :return: the list with directories' paths
    """
    file_dir = Path(config.base_directory_name)
    files_dir = Path(os.path.join(config.output_directory_name))
    logs_dir = Path(config.logs_directory_name)
    logs_xml_dir = Path(os.path.join(config.logs_directory_name, "xml_generator"))
    for dir_name in locals().values():
        dir_name.mkdir(exist_ok=True)


def clear_dir(dir_path: str = "./files/"):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)


def clear_cpg_dir():
    """Очищает только ЦПГ директории, не трогая ЦССИ файлы"""
    cpg_dirs = ["./files/TEST_cpg/", "./files/cpg/"]
    
    for dir_path in cpg_dirs:
        if os.path.exists(dir_path):
            print(f"[DEBUG] Очищаем ЦПГ директорию: {dir_path}")
            shutil.rmtree(dir_path)
            os.makedirs(dir_path)
        else:
            print(f"[DEBUG] ЦПГ директория не существует: {dir_path}")
    
    print("[DEBUG] Очистка ЦПГ директорий завершена")
