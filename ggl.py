import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_annotation() -> str:
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('google.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('ЧАТ').sheet1
    return sheet.cell(1, 2).value
