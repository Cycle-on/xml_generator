import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def _get_service_sacc():
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scopes).authorize(
        httplib2.Http())
    return build('sheets', 'v4', http=creds_service)
