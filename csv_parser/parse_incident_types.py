from pprint import pprint

import numpy as np
import pandas as pd

from constants import ALL_PROJ_CONSTANTS
from csv_reader import get_csv_from_url
from schemas.string_eos import IncidentType, get_string_eos_type

list_names = [
    "INCIDENT_TYPES_FOR_CARD01",
    "INCIDENT_TYPES_FOR_CARD02",
    "INCIDENT_TYPES_FOR_CARD03",
    "INCIDENT_TYPES_FOR_CARD04",
    "AT_INCIDENT_TYPES",
    "CS_INCIDENT_TYPES",
]
CARDS_INDEXES_INCIDENT_TYPES = {
    1: ALL_PROJ_CONSTANTS["INCIDENT_TYPES_FOR_CARD01"],
    2: ALL_PROJ_CONSTANTS["INCIDENT_TYPES_FOR_CARD02"],
    3: ALL_PROJ_CONSTANTS["INCIDENT_TYPES_FOR_CARD03"],
    4: ALL_PROJ_CONSTANTS["INCIDENT_TYPES_FOR_CARD04"],
    5: ALL_PROJ_CONSTANTS["AT_INCIDENT_TYPES"],
    6: ALL_PROJ_CONSTANTS["CS_INCIDENT_TYPES"],
}


def __clear_incident_types():
    global CARDS_INDEXES_INCIDENT_TYPES
    for k in CARDS_INDEXES_INCIDENT_TYPES:
        CARDS_INDEXES_INCIDENT_TYPES[k].clear()


def __delete_duplicates_from_list():
    for k, lst in CARDS_INDEXES_INCIDENT_TYPES.items():
        doubles = []
        for el in lst:
            if el in doubles:
                continue
            doubles.append(el)
        CARDS_INDEXES_INCIDENT_TYPES[k] = doubles


ALL_PROJ_CONSTANTS["INCIDENT_TYPES_LIST"]: list[IncidentType] = []


def get_string_eos_type_id_by_eos_name(eos_name: str):
    for el in get_string_eos_type().model_dump()["values"]:
        if el["name"] == eos_name:
            return el.get("id", 0)
    return None


def fill_incident_type_lists(region_name: str = ""):
    global CARDS_INDEXES_INCIDENT_TYPES
    __clear_incident_types()
    resp: pd.Series = get_csv_from_url(ALL_PROJ_CONSTANTS["INCIDENT_TYPES_URL"])
    for el in resp:
        if el["region_name"] != region_name:
            continue
        incident_type_info_dict = {}
        incident_type_info_dict["incidentId"] = el["IncidentId"]
        incident_type_info_dict["parentIncidentId"] = el["parentIncidentId"]
        incident_type_info_dict["eosClassTypeId"] = []
        incident_type_info_dict["incidentTitle"] = el["ukio_type"]

        el = el.replace(np.nan, "").to_dict()
        incident_type_name = el["ukio_type"]
        ukio_count = el["count_ukio"]
        F: list[int] = []  # list with indexes
        incident_type_names = []
        column_names = [
            "Пожарная служба",
            "Полиция",
            "Скорая помощь",
            "Газовая служба",
            "Антитеррор",
            "ЖКХ",
        ]
        eos_columns = [el[column_names[i]] for i in range(len(column_names))]

        for i, bool_card_info in enumerate(eos_columns, 1):  # eos iteration
            # if row has more than one eos
            if bool(bool_card_info):
                incident_type_info_dict["eosClassTypeId"].append(
                    get_string_eos_type_id_by_eos_name(column_names[i - 1])
                )
                if F:
                    # add new eos to the linked
                    CARDS_INDEXES_INCIDENT_TYPES[i].append(
                        {
                            "name": incident_type_name,
                            "linked_eos": [column_names[F[0] - 1]],
                            "ukio_count": ukio_count,
                            "type": column_names[i - 1],
                        }
                    )
                    incident_type_names.append(incident_type_name)
                    # add self to the first eos
                    if CARDS_INDEXES_INCIDENT_TYPES[F[0]][-1].get("linked_eos"):
                        CARDS_INDEXES_INCIDENT_TYPES[F[0]][-1]["linked_eos"].append(
                            column_names[i - 1]
                        )
                    else:
                        CARDS_INDEXES_INCIDENT_TYPES[F[0]][-1]["linked_eos"] = [
                            column_names[i - 1]
                        ]
                    # appending self eos to the other eoses
                    for eos_index in F[1:]:
                        CARDS_INDEXES_INCIDENT_TYPES[i][-1]["linked_eos"].append(
                            column_names[eos_index]
                        )
                        if CARDS_INDEXES_INCIDENT_TYPES[eos_index][-1].get(
                            "linked_eos"
                        ):
                            CARDS_INDEXES_INCIDENT_TYPES[eos_index][-1][
                                "linked_eos"
                            ].append(column_names[i - 1])
                        else:
                            CARDS_INDEXES_INCIDENT_TYPES[eos_index][-1][
                                "linked_eos"
                            ] = [column_names[i]]
                else:
                    if incident_type_name in incident_type_names:
                        continue
                    CARDS_INDEXES_INCIDENT_TYPES[i].append(
                        {
                            "name": incident_type_name,
                            "ukio_count": ukio_count,
                            "type": column_names[i - 1],
                        }
                    )
                    incident_type_names.append(incident_type_name)

                F.append(i)
        ALL_PROJ_CONSTANTS["INCIDENT_TYPES_LIST"].append(
            IncidentType(**incident_type_info_dict)
        )
    __delete_duplicates_from_list()
    for i, el in enumerate(list_names):
        ALL_PROJ_CONSTANTS[el] = CARDS_INDEXES_INCIDENT_TYPES[i + 1]


def main():
    pprint(CARDS_INDEXES_INCIDENT_TYPES)


if __name__ == "__main__":
    main()
