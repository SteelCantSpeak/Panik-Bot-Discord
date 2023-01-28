from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import Levenshtein as lev
from fuzzywuzzy import fuzz
from lib import Rolling as roll

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
REFSHEETID = '115Ji6RbAqe9WzTjMSQDHXj_AkJussvB_lgfE-VrZ50k'
REFSHEETRANGE = 'Concatenation!E1:G139'



def AccessData(sheetID, _range): #Connect to Sheet for Read-Only Data collection
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
    result = sheet.values().get(spreadsheetId= sheetID, range= _range).execute()
    values = result.get('values', [])
    return values

#USE COMMANDS

def Lookup(message): #find info from the Reference Sheet
    x = message.split()
    power = x[1]

    array = AccessData(REFSHEETID, REFSHEETRANGE)

    if power.startswith('"'):
        power += x[1]

    results = compareValues(array, power.lower())
    Header = results[0].capitalize()
    body = results[1]
    Footer = results[2]

    return [Header, body, Footer]

def rollFromSheet(array, search): #Find dice value from Character Array and roll Integer
    score = compareValues(array, search) #gives row for name and dice count
    try:
        result = roll.rollDice(getCharacterName(array) +" rolls " + score[0], int(score[1]))
        return [result[0], result[1], result[2], getCharacterImage(array)]
    except: #If score isn't image?
        return [getCharacterName(array) +" rolls... their " + score[1]+"?", "Please try again", "$check" , getCharacterImage(array)]


def compareValues(array = [], wanted = ""): #Compare each row[0] value for closest to WANTED
        answer = ""
        correctness = 0
        for row in array:
            if similarTest(row[0].lower(), wanted) > correctness:
                answer = row
                correctness = similarTest(row[0].lower(), wanted)
        return answer

def similarTest(value = "", wanted = ""): #Analysis for Comparision of two strings
    return fuzz.ratio(value, wanted)


def getSheetLink(url = ""): #Convert Sheet's addess into Sheet ID
    text = url.replace("https://docs.google.com/spreadsheets/d/","")
    final = text.split("/")
    return final[0]

def getCharacterArray(sheetID): #Get Skeleton Info from character sheet
    # 0, IMAGE 
    # 1, Name 2, Tier 3, Edge 4, Resolve
    # 5, Health 6, Hero Points 7, Max Speed 8, Max Carry 9, Passive Defense 10, Active Defense 11, Mental Defense
    # 12, Agility 13, Intellect 14, Might 15, Perception 16, Toughness 17, Willpower 
    # 18, Academics 19, Charm 20, Command 21, Covert 22, Investigation 23, Medicine 24, Professional 25, Science 26, Streetwise 27, Survival 28, Technology 29, Vehicles

    array = AccessData(sheetID, "Hidden Data!O2:P130")
    return array

def getCharacterImage(array):
    return array[0][1] #IMAGE

def getCharacterName(array):
    return array[1][1]

def getCharacterBio(array):
    value = [x[1] for x in array] #Only the numbers, so value[13] is 10 instead of array[13][1] = 10
    basics = """**__Hero__**
    **Edge:** %s            **Resolve:** %s
    **Health:** %s          **Hero points:** %s
    **Max Speed:** *%s*
    **Max Carry/Push:** *%s*
    **__Defenses__**
    **Passive:** %sd
    **Active:** %sd
    **Mental:** %sd
    """ % (value[3],value[4],value[5],value[6],value[7],value[8],value[9],value[10],value[11],)

    abilities = """**__Abilities__**
    **Agility:** %sd     **Intellect:** %sd
    **Might:** %sd       **Perception:** %sd
    **Toughness:** %sd   **Willpower:** %sd
    """ % (value[12],value[13],value[14],value[15],value[16],value[17],)

    talents = """**__Talents__**
    **Academics:** %sd       **Charm:** %sd
    **Command:** %sd         **Covert:** %sd
    **Investigation:** %sd   **Medicine:** %sd
    **Professional:** %sd    **Science:** %sd
    **Streetwise:** %sd      **Survival:** %sd
    **Technology:** %sd      **Vehicles:** %sd
    """ % (value[18],value[19],value[20],value[21],value[22],value[23],value[24],value[25],value[26],value[27],value[28],value[29],)

    powers = """**__Powers__**""" 
    if len(array) > 30:
        for x in range(len(array)):
            if x <= 29:
                continue
            powers += "\n ***%s** %sd*" % (array[x][0], array[x][1],) #Only time in this section ARRAY should be used instead of VALUE
    
    body = basics + abilities + talents + powers
    return [getCharacterName(array), body, "$import to upload a new character, or $list to see your roster", getCharacterImage(array)]
