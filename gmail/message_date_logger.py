#!/usr/bin/python

# short script to read messages from gmail inbox
# (this script outputs only the date as unixtimestamp)
# requires gmail api token etc.
# API Quotas: 250.0 units/second/user && 1,000,000,000 units/day

# check out https://developers.google.com/gmail/api/quickstart/quickstart-python
# and https://console.developers.google.com

import sys
import httplib2
import dateutil.parser

from apiclient.discovery import build
from apiclient import errors
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

def GetMessage(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    headerFound = False

    for header in message['payload']['headers']:
      if header['name'] == 'Date': 
        headerFound = True
        print dateutil.parser.parse(header['value']).replace(day=15, hour=0, minute=0, second=0, microsecond=0).strftime('%s')

    if not headerFound:
      print >>sys.stderr, 'message', msg_id,  'without date (a hangout?)'

  except errors.HttpError, error:
    print 'An error occurred: %s (%s)' % error, header['value']
  except ValueError, error:
    print 'An ValueError occurred: %s' % error

def parseMessagePage(messages, service):
  msgs = []
  for m in messages:
    GetMessage(service, 'me', m['id'])

# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

# Start the OAuth flow to retrieve credentials
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
credentials = STORAGE.get()
if credentials is None or credentials.invalid:
  credentials = run(flow, STORAGE, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
service = build('gmail', 'v1', http=http)

onlyFirstPage = False  # for testing
startAtMessage = 0 # if script fails => guess
startAtPage = None     # if script fails => remember last page token

counter = 0
try:
    if startAtPage == None: response = service.users().messages().list(userId='me').execute()
    else: response = service.users().messages().list(userId='me', pageToken=startAtPage).execute()

    counter = counter + 1

    if startAtPage == 0 and 'messages' in response:
      parseMessagePage(response['messages'], service)

    while not onlyFirstPage and 'nextPageToken' in response:
      counter = counter + len(response['messages'])
      #if counter % 10 == 0: gc.collect()

      page_token = response['nextPageToken']
      response = service.users().messages().list(userId='me', pageToken=page_token).execute()
      #messages.extend(response['messages'])
      if counter > startAtMessage: 
        parseMessagePage(response['messages'], service)
        if 'nextPageToken' in response: print >>sys.stderr, 'nextPageToken:', response['nextPageToken'], 'at', counter

except errors.HttpError, error:
    print 'An error occurred: %s' % error

#print messages
print 'done'










