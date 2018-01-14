import argparse
import io
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

class DriveClient():

    def __init__(self):
        self.drive = self._create_client()
        self.file_id = None

    def _create_client(self):
        """Create an instance of the Google Drive client."""
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        drive = apiclient.discovery.build('drive', 'v3', http=http)
        return drive
    
    def _get_credentials(self):
        """Gets valid user credentials from storage.

        MODIFIED FROM THIS SAMPLE CODE: https://developers.google.com/drive/v3/web/quickstart/python

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

    def file_exists(self):
        """Test if the file exists, and set the fileId if it does."""
        query = "name = '{0}'".format(DATABASE)
        query_result = self.drive.files().list(q=query).execute()
        if query_result['files']:
            if not self.file_id:
                self.file_id = query_result['files'][0]['id']
            return True
        else:
            return False
    
    def download(self):
        """MODIFIED FROM THIS SAMPLE CODE: https://developers.google.com/drive/v3/web/manage-downloads"""
        if self.file_exists():
            request = self.drive.files().get_media(fileId=self.file_id)
            fh = io.FileIO(DATABASE, 'w')
            downloader = apiclient.http.MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print('Download {0:d}%'.format(int(status.progress() * 100)))

    def upload(self):
        """MODIFIED FROM THIS SAMPLE CODE: https://developers.google.com/drive/v3/web/manage-uploads"""
        # File content
        media_body = apiclient.http.MediaFileUpload(DATABASE, mimetype=MIMETYPE)
        # File metadata
        body = {'name': DATABASE, 'description': DESCRIPTION}
        if self.file_exists():
            # Upload a new version of the file.
            self.drive.files().update(
                fileId=self.file_id,
                body=body,
                media_body=media_body
            ).execute()
            print('Updated file.')
        else:
            # The file doesn't exist - create it.
            print("The file doesn't exist.")
            self.drive.files().create(body=body, media_body=media_body).execute()
            print('Created file.')
