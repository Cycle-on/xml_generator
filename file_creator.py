import csv
import datetime
import os
import traceback
import xml.etree.ElementTree as ET

from pydantic import BaseModel

from config import load_config
from send_files import modify_xml_file_to_send

config = load_config()


def __up_first_letter(s: str) -> str:
    if not s:
        return s
    return s[0].capitalize() + s[1:]


def __down_first_letter(s: str) -> str:
    if not s:
        return s
    return s[0].lower() + s[1:]


def __generate_xml_from_pydantic(root: ET.Element, model: dict, name='ukio'):
    """
    recursive subtree generator from dicts
    *adding different type subtrees to root
    :param root: sub_root connecting to root
    :param model: dict with property names and values
    :param name:name in the xml file
    :return:
    """
    sub_root = ET.SubElement(root, name)
    for feature_name, feature_value in model.items():
        if feature_name == 'PhoneCallId':
            feature_name = __down_first_letter(feature_value)
        if feature_name in (
                'phoneCall', 'callContent', 'address', 'era', 'psycho', 'consult', 'transferItem', 'receptionItem',
                'eosItem',
                'card01', 'card02', 'card03', 'card04', 'cardAT', 'cardCommServ', 'redirectCall', 'operator'):
            feature_name = __up_first_letter(feature_name)
        if feature_value is None:
            continue
        elif isinstance(feature_value, dict):  # if we have pydantic model
            __generate_xml_from_pydantic(sub_root, feature_value, name=feature_name)
            continue

        elif feature_name == 'Ukios':
            for phone_call in feature_value:
                __generate_xml_from_pydantic(sub_root, phone_call, name=__up_first_letter(feature_name)[:-1])
            continue

        elif isinstance(feature_value, list):
            for value in feature_value:
                if isinstance(value, str):
                    el = ET.SubElement(sub_root, feature_name)
                    el.text = str(value)

                else:
                    __generate_xml_from_pydantic(sub_root, value, name=feature_name)
            continue

        elif isinstance(feature_value, datetime.datetime):
            feature_value = feature_value.isoformat()
        if feature_name in ('p_min', 'p_max', 'class'):
            continue

        el = ET.SubElement(sub_root, feature_name)
        el.text = str(feature_value)
    return sub_root


def create_file_from_model(model: BaseModel, filename: str = 'output', basename='ukio') -> str:
    """
    function creates xml file from a pydantic model
    :param basename:
    :param filename: string format
    :param model: pydantic model
    :return:  True -> file was saved successful
              False -> some exceptions
    """
    try:
        root_ = ET.Element(basename)
        sub_root = __generate_xml_from_pydantic(root_, model.dict(), basename)
        tree = ET.ElementTree(sub_root)
        file_path = os.path.join(config.output_directory_name, f"{filename}.xml")
        tree.write(file_path, encoding='utf-8')
        modify_xml_file_to_send(file_path)
        return True
    except Exception as ex:
        print(traceback.print_exc())
        with open(
                os.path.join(
                    config.logs_directory_name,
                    "xml_generator",
                    datetime.datetime.now().isoformat()
                ),
                mode="w+") as f:
            traceback.print_exc(file=f)
        return False


def create_send_info_csv_files(filename: str, config_send_info_list: list[dict]):
    config_send_info_list.sort(key=lambda x: x['dt_send'])
    filename = f'{filename}.csv'
    # Запись данных в CSV файл
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        try:
            writer = csv.DictWriter(file, fieldnames=config_send_info_list[0].keys())
            writer.writeheader()  # Записываем заголовки
            writer.writerows(config_send_info_list)  # Записываем строки данных
        except IndexError:
            return False
