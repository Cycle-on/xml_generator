from google_sheet_parser import _get_service_sacc
from constants import *


def main():
    resp = _get_service_sacc().spreadsheets().values().get(spreadsheetId=SHEET_ID,
                                                           range=f"{INCIDENT_TYPES_LIST_NAME}!A1:A999").execute()
    print(resp)


if __name__ == '__main__':
    main()
