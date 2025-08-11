import datetime
import gc
import os
import traceback
import xml.etree.ElementTree as ET

from pydantic import BaseModel

from config import load_config
from wsdl_parser.wsdl_tester import get_types_from_wsdl

config = load_config()

# Cache for WSDL types to avoid repeated file reads
_wsdl_types_cache = None


def __up_first_letter(s: str) -> str:
    if not s:
        return s
    return s[0].capitalize() + s[1:]


def __down_first_letter(s: str) -> str:
    if not s:
        return s
    return s[0].lower() + s[1:]


def get_wsdl_types():
    global _wsdl_types_cache
    if _wsdl_types_cache is None:
        _wsdl_types_cache = get_types_from_wsdl(
            "wsdl_5.wsdl", get_capital_fields=True
        )
    return _wsdl_types_cache


def __generate_xml_from_pydantic(root: ET.Element, model: dict, name="Ukio"):
    """
    recursive subtree generator from dicts
    *adding different type subtrees to root
    :param root: sub_root connecting to root
    :param model: dict with property names and values
    :param name:name in the xml file
    :return:
    """
    if not name.startswith("s112:"):
        name = "s112:" + name
    sub_root = ET.SubElement(root, name)

    for feature_name, feature_value in model.items():
        if feature_name == "PhoneCallId":
            feature_name = __down_first_letter(feature_name)
        if feature_name in get_wsdl_types():
            feature_name = __up_first_letter(feature_name)
        if feature_value is None:
            continue
        elif isinstance(feature_value, dict):
            __generate_xml_from_pydantic(
                sub_root, feature_value, name=f"s112:{feature_name}"
            )
            continue
        elif feature_name == "Ukios":
            sub_root.attrib["xmlns:s112"] = "s112"
            ukio_upper_name = __up_first_letter(feature_name)[:-1]
            for phone_call in feature_value:
                __generate_xml_from_pydantic(
                    sub_root, phone_call, name=f"s112:{ukio_upper_name}"
                )
            continue
        elif isinstance(feature_value, list):
            for value in feature_value:
                if isinstance(value, (str, int)):
                    if not feature_name.startswith("s112:"):
                        feature_name = "s112:" + feature_name
                    el = ET.SubElement(sub_root, feature_name)
                    el.text = str(value)
                else:
                    __generate_xml_from_pydantic(sub_root, value, name=feature_name)
            continue
        elif isinstance(feature_value, datetime.datetime):
            feature_value = feature_value.isoformat()
        if feature_name in ("p_min", "p_max", "class"):
            continue
        el = ET.SubElement(sub_root, f"s112:{feature_name}")
        # Обработка enum значений - берем .value вместо str()
        if hasattr(feature_value, 'value'):  # Это enum
            el.text = feature_value.value
        else:
            el.text = str(feature_value)
        if "dt" in feature_name:
            el.text += "Z"
    return sub_root


def create_file_from_model(
    model: BaseModel,
    filename: str = "output",
    basename="ukio",
    region_name: str = "",
    to_send: bool = False,
):
    """
    function creates xml file from a pydantic model
    :param region_name:
    :param basename:
    :param filename: string format
    :param model: pydantic model
    :return:  True -> file was saved successful
              False -> some exceptions
    """
    root_ = None
    sub_root = None
    tree = None
    log_file = None

    try:
        root_ = ET.Element(basename)
        sub_root = __generate_xml_from_pydantic(
            root_, model.model_dump(), f"s112:{basename}"
        )
        tree = ET.ElementTree(sub_root)

        if to_send:
            dir_path = os.path.join(
                config.output_directory_name, str(region_name), "prepared_to_send_files"
            )
        else:
            dir_path = os.path.join(
                config.output_directory_name, str(region_name), basename
            )

        file_path = os.path.join(dir_path, f"{filename}.xml")

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(file_path, "wb+") as tree_to_write:
            tree.write(tree_to_write, encoding="utf-8")

        return file_path
    except Exception:
        print(traceback.print_exc())
        log_path = os.path.join(
            config.logs_directory_name,
            "xml_generator",
            datetime.datetime.now().isoformat(),
        )
        try:
            log_file = open(log_path, mode="w+")
            traceback.print_exc(file=log_file)
        finally:
            if log_file:
                log_file.close()
        return False
    finally:
        # Clean up all resources
        if root_ is not None:
            del root_
        if sub_root is not None:
            del sub_root
        if tree is not None:
            del tree
        gc.collect()
