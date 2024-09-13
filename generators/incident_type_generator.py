"""
module in progress...
"""

import random

from schemas.string_eos import StringEosType


def check_list_equality(l1: list, l2: list) -> bool:
    return set(l1) == set(l2)


def delete_linked_eos_from_list_by_needed_count(incident_type_list: list, eos_count: int = 1,
                                                ignored_types=None):
    if ignored_types is None:
        ignored_types = []
    ans = []
    for el in incident_type_list:
        # if I have linked eoses, I need to check eoses which are ignored
        if len(el.get('linked_eos', [])) < eos_count:
            ans.append(el)
    return ans


def get_names_from_eos_type_list(eos_type_list: list[StringEosType]) -> list[str]:
    ans = []
    for el in eos_type_list:
        ans.append(el['name'])
    return ans


def __make_section_from_list(s: list[dict]):
    counter = 0
    for el in s:
        el['section_min'] = counter + 1
        el['section_max'] = counter + el['ukio_count']
        counter += el['ukio_count']
    return s, counter


def generate_card_incident_types_from_list(eos_type_list: list[StringEosType]) -> str:
    return '-'
    # if len(eos_type_list) == 1:
    #     string_eos_incident_types_list = delete_linked_eos_from_list_by_needed_count(
    #         CARDS_INDEXES_INCIDENT_TYPES[int(eos_type_list[0]['code'])]
    #     )
    # else:
    #     string_eos_incident_types_list = delete_linked_eos_from_list_by_needed_count(
    #         CARDS_INDEXES_INCIDENT_TYPES[int(eos_type_list[0]['code'])]
    #     )
    # else:
    #
    #     string_eos_incident_types_list = []
    #     added_names = []
    #     for i in range(len(eos_type_list)):
    #         incident_types_list_by_eos: list = CARDS_INDEXES_INCIDENT_TYPES[int(eos_type_list[i]['code'])]
    #
    #         for var in incident_types_list_by_eos:
    #             if var['name'] in added_names:
    #                 continue
    #
    #             # at first, check double eoses
    #             if var.get('linked_eos'):
    #                 if len(var['linked_eos']) <= len(eos_type_list) - 1:  # if I have one linked eos
    #                     linked_eos_name = var['linked_eos'][0]
    #                     if linked_eos_name in get_names_from_eos_type_list(eos_type_list):
    #                         string_eos_incident_types_list.append(var)
    #             # at second, add without linked
    #             else:
    #                 string_eos_incident_types_list.append(var)
    #             added_names.append(var['name'])
    # if len(eos_type_list) == 1:
    #     string_eos_incident_types_list, last_number = __make_section_from_list(string_eos_incident_types_list)
    #     one_incident = get_solo_incident_type(string_eos_incident_types_list, last_number)
    # else:
    #     # many eoses algorithm
    #     pass
    # return one_incident['name']


def get_random_eos_incident_type(eos_type_list: list, incident_types_list, max_number):
    eos_count = len(eos_type_list)
    random_value = random.randint(1, max_number)  # 13
    filtered_incident_types_list = []
    for el in incident_types_list:
        if el['section_min'] <= random_value <= el['section_max']:
            if eos_count == 1:
                filtered_incident_types_list.append(el)
                break
            if el.get('linked_eos'):
                if len(el['linked_eos']) == eos_count - 1:
                    filtered_incident_types_list.append(el)
                    break
                else:
                    filtered_incident_types_list.append(el)
                    return get_random_eos_incident_type(
                        eos_type_list,
                        delete_linked_eos_from_list_by_needed_count(
                            incident_types_list,
                            eos_count - len(el['linked_eos']),
                            ignored_types=el['linked_eos']
                        ),
                        max_number
                    )
            else:
                filtered_incident_types_list.append(el)
                return  # something

    return filtered_incident_types_list


def get_solo_incident_type(section_incident_type_list: list, last_number: int):
    random_value = random.randint(1, last_number)
    for el in section_incident_type_list:
        if el['section_min'] <= random_value <= el['section_max']:
            return el
