from google_sheet_parser import _get_service_acc
from constants import *


def fill_incident_type_lists():
    CARDS_INDEXES_INCIDENT_TYPES = {
        0: INCIDENT_TYPES_FOR_CARD01,
        1: INCIDENT_TYPES_FOR_CARD02,
        2: INCIDENT_TYPES_FOR_CARD03,
        3: GAS_INCIDENT_TYPES,
        4: AT_INCIDENT_TYPES,
        5: CS_INCIDENT_TYPES
    }

    resp = _get_service_acc().spreadsheets().values().get(spreadsheetId=SHEET_ID,
                                                          range=f"{INCIDENT_TYPES_LIST_NAME}!A1:I999").execute()
    column_name = resp['values'][0]
    for el in resp['values'][1:]:
        incident_type_name = el[0]
        ukio_count = int(el[2])
        for i, bool_card_info in enumerate(el[3:]):
            if bool(bool_card_info):
                CARDS_INDEXES_INCIDENT_TYPES[i].append(incident_type_name)


def main():
    fill_incident_type_lists()


if __name__ == '__main__':
    main()
