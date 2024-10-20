from .generator import *
from .sender import *
from .union_constants import *

ALL_PROJ_CONSTANTS = globals()


def get_file_prefix(prefix_var_name: str):
    if prefix_var_name:
        return prefix_var_name
    return BASE_SOAP_PREFIX


def get_file_postfix(postfix_var_name: str):
    if postfix_var_name:
        return postfix_var_name
    return BASE_SOAP_POSTFIX


def parse_constants_to_tab_format():
    for constant_name, constant_value in ALL_PROJ_CONSTANTS.items():
        if '__' in constant_name:
            continue

        print(constant_name, end='\t')
    print()
    for constant_name, constant_value in ALL_PROJ_CONSTANTS.items():
        if '__' in constant_name:
            continue

        print(constant_value, end='\t')
