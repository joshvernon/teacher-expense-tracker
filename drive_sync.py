import argparse
import os

import apiclient
import httplib2
from oauth2client import client, tools
from oauth2client.file import Storage

from data_access import DATABASE
from secrets3 import CLIENT_SECRET, CREDENTIAL_DIR

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

SCOPES = 'https://www.googleapis.com/auth/drive'
APPLICATION_NAME = 'Teacher Expense Tracker'
MIMETYPE = 'application/x-sqlite3'
DESCRIPTION = 'Database for Teacher Expense Tracker'

def get_credentials():
    """Gets valid user credentials from storage.

    Taken from here: https://developers.google.com/drive/v3/web/quickstart/python

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    if not os.path.exists(CREDENTIAL_DIR):
        os.makedirs(CREDENTIAL_DIR)
    credential_path = os.path.join(CREDENTIAL_DIR,
                                   'teacher-expense-tracker.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
    return credentials

def upload():
    # File content
    media_body = apiclient.http.MediaFileUpload(DATABASE, mimetype=MIMETYPE)
    # File metadata
    body = {'name': DATABASE, 'description': DESCRIPTION}

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    drive = apiclient.discovery.build('drive', 'v3', http=http)
    query = "name = '{0}'".format(DATABASE)
    list_result = drive.files().list(q=query).execute()
    if list_result['files']:
        print('The file already exists.')
        # Get the ID of the existing file.
        file_id = list_result['files'][0]['id']
        drive.files().update(fileId=file_id, body=body, media_body=media_body).execute()
        print('Updated file.')
    else:
        # The file doesn't exist - create it.
        print("The file doesn't exist.")
        drive.files().create(body=body, media_body=media_body).execute()
        print('Created file.')

if __name__ == '__main__':
    upload()
