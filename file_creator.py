import csv
import datetime
import os
import traceback
import xml.etree.ElementTree as ET

from pydantic import BaseModel

from config import load_config
from schemas.phonecall import MissedCalls
from schemas.ukio_model import Ukios
from wsdl_parser.wsdl_tester import get_types_from_wsdl

config = load_config()


def __up_first_letter(s: str) -> str:
    if not s:
        return s
    return s[0].capitalize() + s[1:]


def __down_first_letter(s: str) -> str:
    if not s:
        return s
    return s[0].lower() + s[1:]


up_first_verb_schemas: list[str] = get_types_from_wsdl('wsdl_4_3.wsdl', get_capital_fields=True)


def __generate_xml_from_pydantic(root: ET.Element, model: dict, name='Ukio'):
    """
    recursive subtree generator from dicts
    *adding different type subtrees to root
    :param root: sub_root connecting to root
    :param model: dict with property names and values
    :param name:name in the xml file
    :return:
    """
    if not name.startswith('s112:'):
        name = "s112:" + name
    sub_root = ET.SubElement(root, name)
    for feature_name, feature_value in model.items():

        if feature_name == 'PhoneCallId':
            feature_name = __down_first_letter(feature_name)
        if feature_name in up_first_verb_schemas:

            feature_name = __up_first_letter(feature_name)
        if feature_value is None:
            continue
        elif isinstance(feature_value, dict):  # if we have pydantic model
            __generate_xml_from_pydantic(sub_root, feature_value, name=f"s112:{feature_name}")
            continue

        elif feature_name == 'Ukios':
            sub_root.attrib["xmlns:s112"] = "s112"
            ukio_upper_name = __up_first_letter(feature_name)[:-1]
            for phone_call in feature_value:
                __generate_xml_from_pydantic(sub_root, phone_call, name=f"s112:{ukio_upper_name}")
            continue

        elif isinstance(feature_value, list):
            # print(feature_name)

            for value in feature_value:

                if isinstance(value, str) or isinstance(value, int):
                    # feature_name = f"s112:{feature_name}"
                    el = ET.SubElement(sub_root, feature_name)
                    el.text = str(value)

                else:
                    # print(feature_name, value)
                    __generate_xml_from_pydantic(sub_root, value, name=feature_name)
            continue

        elif isinstance(feature_value, datetime.datetime):
            feature_value = feature_value.isoformat()
        if feature_name in ('p_min', 'p_max', 'class'):
            continue
        # print(feature_name, feature_value)
        el = ET.SubElement(sub_root, f"s112:{feature_name}")
        el.text = str(feature_value)
        if 'dt' in feature_name:
            el.text += 'Z'
    return sub_root


def create_file_from_model(model: BaseModel,
                           filename: str = 'output',
                           basename='ukio',
                           region_name: str = '',
                           to_send: bool = False):
    """
    function creates xml file from a pydantic model
    :param region_name:
    :param basename:
    :param filename: string format
    :param model: pydantic model
    :return:  True -> file was saved successful
              False -> some exceptions
    """
    try:
        root_ = ET.Element(basename)

        sub_root = __generate_xml_from_pydantic(root_, model.model_dump(), f"s112:{basename}")
        tree = ET.ElementTree(sub_root)
        # print(tree.getroot())
        if to_send:
            dir_path = os.path.join(config.output_directory_name, region_name, 'prepared_to_send_files')
        else:
            dir_path = os.path.join(config.output_directory_name, region_name, basename)

        file_path = os.path.join(dir_path, f"{filename}.xml")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        tree.write(file_path, encoding='utf-8')
        return file_path
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


def create_send_info_csv_files(filename: str, config_send_info_list: list[dict], region_name: str = ''):
    config_send_info_list.sort(key=lambda x: x['dt_send'])
    filename = f'{filename}.csv'
    csv_dir_path = os.path.join(config.output_directory_name, region_name)
    csv_file_path = os.path.join(csv_dir_path, filename)
    # Запись данных в CSV файл
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        try:
            writer = csv.DictWriter(file, fieldnames=config_send_info_list[0].keys())
            writer.writeheader()  # Записываем заголовки
            writer.writerows(config_send_info_list)  # Записываем строки данных
        except IndexError:
            return False


def prepare_files_to_send(ukios: Ukios, missed: MissedCalls, region_name: str):
    ukios = ukios.Ukios
    missed = missed.missedCalls
    print('start preparing ukios')
    for i in range(len(ukios)):
        create_file_from_model(ukios[i], filename=f'ukios_{i}', region_name=region_name, to_send=True)

    print('start preparing missed')
    for i in range(len(missed)):
        create_file_from_model(missed[i], region_name=region_name, filename=f'missed_{i}', to_send=True)
