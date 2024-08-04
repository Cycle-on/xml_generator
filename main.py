import datetime
import os

from test_cards import cards
import xml.etree.ElementTree as ET


def __generate_xml_from_pydantic(root: ET.Element, model: dict, name='ukio'):
    sub_root = ET.SubElement(root, name)
    for feature_name, feature_value in model.items():
        if isinstance(feature_value, dict):  # if we have pydantic model
            __generate_xml_from_pydantic(sub_root, feature_value, name=feature_name)
            continue
        elif isinstance(feature_value, datetime.datetime):
            feature_value = feature_value.isoformat()
        elif isinstance(feature_value, list):
            sub_root_wrapper = ET.SubElement(sub_root, feature_name)
            for value in feature_value:
                __generate_xml_from_pydantic(sub_root_wrapper, value, name=feature_name[:-1])
            continue

        el = ET.SubElement(sub_root, feature_name)
        el.text = str(feature_value)
    return sub_root


def create_file_from_model(filename: str = 'output') -> str:
    """
    :param filename: string format
    :return:  True -> file was saved successful
              False -> some exceptions
    """
    try:
        root_ = ET.Element("ukio")
        c1 = cards[0]
        sub_root = __generate_xml_from_pydantic(root_, c1.dict())
        tree = ET.ElementTree(sub_root)
        tree.write("filename.xml")
        return True
    except Exception as ex:
        with open(os.path.join("logs", "xml_creator", datetime.datetime.now().isoformat()), "w+") as f:
            f.write(str(ex))
        return False


def main():
    create_file_from_model()


if __name__ == '__main__':
    main()
