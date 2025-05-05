from config import load_config

config = load_config()


def modify_xml_file_to_send(
    file_path: str, prefix_var_name: str, postfix_var_name: str
):
    with open(file_path, "r", encoding="utf-8") as f:
        middle_file = [prefix_var_name]
        for row in f:
            middle_file.append(row)
        middle_file.append(postfix_var_name)
    with open(file_path, "w+", encoding="utf-8") as f:
        f.writelines(middle_file)
