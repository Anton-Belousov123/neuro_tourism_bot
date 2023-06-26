
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_messages() -> dict:
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('google.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('ЧАТ').sheet1
    messages = {
        1: sheet.cell(1, 2).value,
        2: sheet.cell(2, 2).value,
        3: sheet.cell(3, 2).value,
        4: sheet.cell(4, 2).value,
        'dk': sheet.cell(5, 2).value
    }
    return messages
