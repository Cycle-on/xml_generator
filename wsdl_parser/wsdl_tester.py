import xml.etree.ElementTree as ET
from pprint import pprint


def __is_first_letter_capitalized(s: str) -> bool:
    return s[0].isupper()


def __down_first_letter(s: str) -> str:
    return s[0].lower() + s[1:]


def get_types_from_wsdl(
    path: str, get_capital_fields: bool = False
) -> dict[str, set] | list:
    cards = {}
    tree = ET.parse(path)
    root = tree.getroot()
    capital_schemas: list[str] = []
    schemas = root[0][0]  # get types child
    for schema in schemas:  # get wsdl schemas
        schema_fields = schema[0]  # get schema fields
        if get_capital_fields and __is_first_letter_capitalized(schema.attrib["name"]):
            capital_schemas.append(__down_first_letter(schema.attrib["name"]))
        cards[schema.attrib["name"]] = set()
        for field in schema_fields:
            if field.attrib.get("name"):  # get element tag
                cards[schema.attrib["name"]].add(field.attrib["name"])
    if get_capital_fields:
        return capital_schemas
    return cards


def get_xml_tree_fields_by_path(path: str):
    tree = ET.parse(path)
    root = tree.getroot()

    def get_nested_fields(card) -> dict:
        card_features = {}
        for field in card:
            if len(field) != 0:
                card_features |= get_nested_fields(field)
            try:
                card_features[card.tag].add(field.tag)
            except KeyError:
                card_features[card.tag] = {field.tag}
        return card_features

    for card in root:
        yield get_nested_fields(card)


def check_fields_by_file_path(file_path: str, wsdl_path: str) -> None:
    wsdl_types = get_types_from_wsdl(wsdl_path)
    missed_fields = {}
    ukio_count = 0
    for ukio_fields in get_xml_tree_fields_by_path(file_path):
        ukio_count += 1
        for schema_name, schema_fields in ukio_fields.items():
            missed_fields[schema_name] = missed_fields.get(schema_name, {})
            missed_fields[schema_name]["count"] = (
                missed_fields[schema_name].get("count", 0) + 1
            )

            try:
                missed_card_fields = wsdl_types[schema_name] - schema_fields
            except KeyError:
                print(f"Неправильно указано поле {schema_name}")
                continue

            for field in missed_card_fields:
                missed_fields[schema_name][field] = (
                    missed_fields[schema_name].get(field, 0) + 1
                )

    for field_name, field_values in missed_fields.items():
        if len(field_values) > 0:
            print(field_name, field_values["count"], ":", end="")
            pprint(field_values)
            print("______")
    # pprint(missed_fields)


def main():
    check_fields_by_file_path(
        "../files/file_2024-10-16_12-54-03/ukios_0.xml", "wsdl_5.wsdl"
    )
    # s = get_types_from_wsdl(get_capital_fields=True)
    # print(s)


if __name__ == "__main__":
    main()
