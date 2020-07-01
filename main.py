from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import Adafruit_DHT
from datetime import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1FZIKElgO5_91rSUsapcV_OIrAwDRMHJ4H_Gjn0ia0og'
SAMPLE_RANGE_NAME = 'sheet_1!A1:C3'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    #result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
    #                            range=SAMPLE_RANGE_NAME).execute()
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 18)
    date = datetime.now().strftime('%F')
    time = datetime.now().strftime('%T')
    print(f'd: {date}, t: {time}, T: {temperature:.2f}, H: {humidity:.2f}')
    body = {'values':[[
        date,
        time,
        temperature,
        humidity]]}
    result = sheet.values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=body).execute()
    #values = result.get('values', [])
    #                            range=SAMPLE_RANGE_NAME).execute()

    #if not values:
    #    print('No data found.')
    #else:
    #    print('Name, Major:')
    #    for row in values:
    #        # Print columns A and E, which correspond to indices 0 and 4.
    #        print('%s, %s' % (row[0], row[2]))

if __name__ == '__main__':
    main()
