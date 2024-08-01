import datetime
from pprint import pprint

from pydantic import BaseModel

from schemas.Phone import Phone, RedirectCall
from schemas.models import Card, Police
import xml.etree.ElementTree as ET


def generate_xml_from_pydantic(root: ET.Element, model: dict, name='ukio'):
    sub_root = ET.SubElement(root, name)
    for feature_name, feature_value in model.items():
        if isinstance(feature_value, dict):  # if we have pydantic model
            generate_xml_from_pydantic(sub_root, feature_value, name=feature_name)
            continue
        elif isinstance(feature_value, datetime.datetime):
            feature_value = feature_value.isoformat()
        el = ET.SubElement(sub_root, feature_name)
        el.text = str(feature_value)
    return sub_root


def main():
    c1 = Card(
        globalId='2',
        wrong=False,
        childPlay=False,
        card02=Police(dtCreate=datetime.datetime.now()),
        phoneCalls=Phone(phoneCallId='1',
                         OperatorIniciatied=False,
                         redirectCall=RedirectCall(
                             dtRedirectConfirm_=datetime.datetime.now(),
                             redirectCancel=True,
                             newPhoneCallId='1',
                             conference=False
                         ))

    )
    root = ET.Element("ukio")
    sub_root = generate_xml_from_pydantic(root, c1.dict())
    tree = ET.ElementTree(sub_root)
    tree.write("filename.xml")


if __name__ == '__main__':
    main()
