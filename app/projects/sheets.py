import os.path
import re
import string

from apiclient import discovery
from google.oauth2 import service_account
from googleapiclient.discovery import Resource

from typing import Dict, List, Optional, Any
from googleapiclient.errors import HttpError, Error
from config import basedir


TEAM_MAX_SIZE = 8
GOOGLE_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


def get_sheets_service() -> Resource:
    secret_file = os.path.join(basedir, GOOGLE_CREDENTIALS)
    if not os.path.exists(secret_file):
        print('ERROR: No google-credentials.json file found!')
        print('Calculated path to credentials file: ' + secret_file)
        raise FileNotFoundError

    credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=SCOPES)
    service = discovery.build('sheets', 'v4', credentials=credentials)
    return service


def column_to_number(col: str):
    number =- 25
    for letter in col:
        if letter not in string.ascii_letters:
            return False
        number += ord(letter.upper())-64+25
    return number


def _safe_get(data: List, r: int, c: int):
    try:
        return data[r][c]
    except IndexError:
        return ''


def _read(range_name: str, service):
    result = service.spreadsheets().values().get(
        spreadsheetId=os.environ.get('SPREADSHEET_ID'),
        range=range_name
    ).execute()

    return result.get('values', [])


def safe_read(row: int, col: str, to_row='', to_col='', service=None):
    range_name = '%s%i:%s%s' % (col, row, to_col, to_row)
    data = _read(range_name, service)
    if to_col == '':
        cols = max(len(line) for line in data)
    else:
        cols = column_to_number(to_col) - column_to_number(col) + 1
    if to_row == '':
        rows = len(data)
    else:
        rows = int(to_row) - row + 1

    return [[_safe_get(data, r, c)
             for c in range(cols)]
            for r in range(rows)]


def sheets_write_to_cell(service: Resource, spreadsheet_id: str, cell: str, value: str) -> Dict[str, str]:
    try:
        result: Dict = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                'valueInputOption': 'RAW',
                'includeValuesInResponse': True,
                'data': [
                    {
                        'range': cell,
                        'majorDimension': 'ROWS',
                        'values': [[value]]
                    },
                ]
            }
        ).execute()

        if result.get('totalUpdatedCells') == 1:
            result.update({'index': cell})
            return {'status': 'success', 'result': result}

    except HttpError as e:
        return {'status': 'error', 'message': 'Ошибка при установлении соединения с сервером',
                'details': e.error_details}
    except Error as e:
        return {'status': 'error', 'message': 'Произошла неизвестная ошибка',
                'details': f'unknown error while writing to cell {cell} (spreadsheet_id={spreadsheet_id})'}
    except:
        raise


def sheets_team_add_member(value: str, team_cell_index: str, team_empty_slots: int) -> Dict[str, str]:
    service = get_sheets_service()

    col = re.search('[A-Z]+', team_cell_index).group(0)

    team_name_row = int(re.search('[0-9]+', team_cell_index).group(0))
    start_row = team_name_row + 1
    end_row = team_name_row + TEAM_MAX_SIZE
    squad = safe_read(row=start_row, col=col, to_row=str(end_row), to_col=col, service=service)
    try:
        row = str(squad.index(['']) + team_name_row + 1)
    except ValueError:
        msg = 'В выбранной команде нет свободных мест'
        return {'status': 'error', 'message': msg}
    cell_index = col + row

    result = sheets_write_to_cell(service, os.environ.get('SPREADSHEET_ID'), cell_index, value)

    return result

