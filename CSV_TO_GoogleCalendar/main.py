from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
import csv
import sys

print ("================ SCRIPT MADE BY ABDULRAHMAN NADEEM ======================")


'''
Reads a csv file.
Returns a tupe of (datetime, summary)
'''
def read_csv(file_name):
    records = []
    with open(file_name, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            summary = row[2]
            date = datetime.datetime.strptime(row[1], "%m/%d/%y")
            dateString = date.strftime("%Y-%m-%d") # 2017-06-18
            records.append( (dateString, summary) )

    return records

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



def getService():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    return service

def addEvent(service, date, summary, calendarId='primary'):
    event = {
      'summary': summary,
      'location': 'Virginia Tech',
      'description': '',
      'start': {
        'date': date,
        'timeZone': 'America/New_York',
      },
      'end': {
        'date': date,
        'timeZone': 'America/New_York',
      },
      'reminders': {
        'useDefault': False,
      },
    }

    event = service.events().insert(calendarId=calendarId, body=event).execute()
    print ('Event created: '+((event.get('htmlLink'))).encode('utf-8').strip())

def createCalendar(service, calendarName):
    calendar = {
        'summary': calendarName,
        'timeZone': 'America/Los_Angeles'
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    return created_calendar

def getCalendarList(service):
    page_token = None
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    return calendar_list

def getCalendar(service, calendarName):
    calendar_list = getCalendarList(service)
    for calendar_entry in calendar_list['items']:
        print ( calendar_entry[u'summary'] )
        if(calendar_entry['summary'] == calendarName):
            return calendar_entry
    return None

def main():
    records = read_csv('TimeTable.csv')
    service = getService()

    for record in records:
        addEvent(service, record[0], record[1])


# main

service = getService()

print (getCalendar(service, 'calendarSummary'))


# addEvent(service, "2017-06-18", "test123")
