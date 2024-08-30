import os.path

import httplib2
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials




def main():
    resp = get_service_sacc().spreadsheets().values().get(spreadsheetId=INCIDENT_TYPES_SHEET_ID,
                                                          range="Лист1!A1:A999").execute()
    print(resp)


if __name__ == '__main__':
    main()
