#!/usr/bin/python

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
    for header in message['payload']['headers']:
    	if header['name'] == 'Date': yield dateutil.parser.parse(header['value']).replace(day=15, hour=0, minute=0, second=0, microsecond=0).strftime('%s')
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def parseMessagePage(messages, service):
	msgs = []
	for m in messages:
		msgs.extend(GetMessage(service, 'me', m['id']))
	return msgs

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

onlyFirstPage = True # for testing
counter = 0
try:
    response = service.users().messages().list(userId='me').execute()
    messages = []
    msgs = []
    counter = counter + 1
    if 'messages' in response:
      messages.extend(response['messages'])
      msgs.extend(parseMessagePage(response['messages'], service))

    while not onlyFirstPage and 'nextPageToken' in response:
      counter = counter + 1
      print "reading page", counter

      page_token = response['nextPageToken']
      response = service.users().messages().list(userId='me',
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])
except errors.HttpError, error:
    print 'An error occurred: %s' % error

#print messages
print msgs










