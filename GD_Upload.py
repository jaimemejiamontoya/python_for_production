import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

class DriveAPI:

    def __init__(self, scopes):
        self.scopes = scopes
        self.creds = self.load_credentials()

    def load_credentials(self):
        creds = None
        if os.path.exists("C:/Users/jaime/python_for_production/token.json"):
            creds = Credentials.from_authorized_user_file("C:/Users/jaime/python_for_production/token.json", self.scopes)
        if not creds or not creds.valid:
            creds = self.authorize_user()
            self.save_credentials(creds)
        return creds

    def authorize_user(self):
        flow = InstalledAppFlow.from_client_secrets_file("C:/Users/jaime/python_for_production/credentials.json", self.scopes)
        return flow.run_local_server(port=0)

    def save_credentials(self, creds):
        with open("C:/Users/jaime/python_for_production/token.json", "w") as token:
            token.write(creds.to_json())

    def create_file(self, file_name, file_path, mime_type):
        service = build("drive", "v3", credentials=self.creds)
        file_metadata = {"name": file_name}
        media = MediaFileUpload(file_path, mimetype=mime_type)
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        return file

def uploadFile(file_name, file_path):
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    drive_api = DriveAPI(SCOPES)
    file = drive_api.create_file(file_name, file_path, "image/jpeg")
