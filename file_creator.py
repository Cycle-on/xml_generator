import datetime
import os

from pydantic import BaseModel

import xml.etree.ElementTree as ET


def __generate_xml_from_pydantic(root: ET.Element, model: dict, name='ukio'):
    """
    recursive subtree generator from dicts
    adding different type subtrees to root
    :param root:
    :param model:
    :param name:
    :return:
    """
    sub_root = ET.SubElement(root, name)
    for feature_name, feature_value in model.items():
        if isinstance(feature_value, dict):  # if we have pydantic model
            __generate_xml_from_pydantic(sub_root, feature_value, name=feature_name)
            continue

        elif isinstance(feature_value, datetime.datetime):
            feature_value = feature_value.isoformat()
        elif feature_name == "phoneCalls":
            for phone_call in feature_value:
                __generate_xml_from_pydantic(sub_root, phone_call, name='PhoneCall')
            continue
        elif isinstance(feature_value, list):
            sub_root_wrapper = ET.SubElement(sub_root, feature_name)
            for value in feature_value:
                __generate_xml_from_pydantic(sub_root_wrapper, value, name=feature_name[:-1])
            continue

        elif feature_value is None:
            continue
        if feature_name in ('p_min', 'p_max', 'class'):
            continue
        el = ET.SubElement(sub_root, feature_name)
        el.text = str(feature_value)
    return sub_root


def create_file_from_model(model: BaseModel, filename: str = 'output', basename='ukio') -> str:
    """
    function which create xml file from pydantic model
    :param filename: string format
    :param model: pydantic model
    :return:  True -> file was saved successful
              False -> some exceptions
    """
    try:
        root_ = ET.Element(basename)
        sub_root = __generate_xml_from_pydantic(root_, model.dict(), basename)
        tree = ET.ElementTree(sub_root)
        tree.write(os.path.join("files", f"{filename}.xml"), encoding='utf-8')
        return True
    except Exception as ex:
        with open(os.path.join("logs", "xml_creator", datetime.datetime.now().isoformat()), "w+") as f:
            f.write(str(ex))
        return False


def main():
    from test_cards import cards
    c1 = cards[0]
    create_file_from_model(c1)


if __name__ == '__main__':
    main()
