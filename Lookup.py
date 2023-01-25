from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import Levenshtein as lev
from fuzzywuzzy import fuzz

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '115Ji6RbAqe9WzTjMSQDHXj_AkJussvB_lgfE-VrZ50k'
SAMPLE_RANGE_NAME = 'Powers!A2:E'

global Header
global Body
global Footer

def AccessData(_range):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range= _range).execute()
    values = result.get('values', [])
    return values

def getListArray(group = "Powers"):
    return group + "!A2:E"    

def Lookup(message):

    link = ""

    x = message.split()

    branch = x[1].lower()
    
    correctValue = 50

    if similarTest(branch, "ability") > correctValue:
        SAMPLE_RANGE_NAME = getListArray("Abilities")
        Header = "Ability"
    elif similarTest(branch, "skill") > correctValue:
        SAMPLE_RANGE_NAME = getListArray("Skills")
        Header = "Skill"
    elif similarTest(branch, "power") > correctValue:
        SAMPLE_RANGE_NAME = getListArray("Powers")
        Header = "Power"
    else:
        return "Please try again"

    array = AccessData(SAMPLE_RANGE_NAME)

    searchQuery = x[2]

    if searchQuery.startswith('"'):
        y = 1
        while searchQuery.endswith('\"') == False and y+2 < len(x):
            searchQuery += x[2+y]
            print(searchQuery)
            y+= 1

    results = compareValues(array, searchQuery.lower())
    Header += ": " + results[0].capitalize()
    body = results[1]
    Footer = results[2]

    return [Header, body, Footer]

def compareValues( array = [], wanted = ""):
        answer = ""
        correctness = 0
        for row in array:
            if similarTest(row[0].lower(), wanted) > correctness:
                answer = row
                correctness = similarTest(row[0].lower(), wanted)
        return answer

def similarTest(value = "", wanted = ""):
    return fuzz.ratio(value, wanted)