import os
import io
import datetime
import pytz
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# Use full read-write scope
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    """Authenticate the user and return the Drive service object."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def list_folder_contents(service, folder_id):
    """List all files and subfolders within a folder."""
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return results.get('files', [])

def list_versions(service, file_id):
    """List all versions of a specific file."""
    versions = service.revisions().list(fileId=file_id, fields="revisions(id, modifiedTime)").execute()
    return versions.get('revisions', [])

def download_version(service, file_id, version_id, temp_filename):
    """Download a specific version of a file to a temporary local file."""
    request = service.revisions().get_media(fileId=file_id, revisionId=version_id)
    fh = io.FileIO(temp_filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Downloading {temp_filename}: {int(status.progress() * 100)}%")
    print(f"Downloaded {temp_filename} successfully.")

def upload_file(service, folder_id, filename, local_path):
    """Upload the rescued file back to the same folder in Google Drive."""
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload(local_path, resumable=True)
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded file '{filename}' with ID: {uploaded_file['id']}")

def sanitize_filename(filename):
    """Remove the '.C85ACF099A00' virus extension if it exists."""
    if filename.endswith('.C85ACF099A00'):
        return filename[:-len('.C85ACF099A00')]
    return filename

def traverse_and_rescue(service, folder_id, target_datetime):
    """Recursively traverse folders and rescue only encrypted files."""
    items = list_folder_contents(service, folder_id)

    for item in items:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            print(f"Entering folder: {item['name']}")
            traverse_and_rescue(service, item['id'], target_datetime)
        elif item['name'].endswith('.C85ACF099A00'):
            # Process only files with the virus extension
            print(f"Processing encrypted file: {item['name']}")
            versions = list_versions(service, item['id'])
            for version in versions:
                modified_time = datetime.datetime.fromisoformat(version['modifiedTime'].replace('Z', '+00:00'))
                if modified_time <= target_datetime:
                    sanitized_filename = sanitize_filename(item['name'])
                    temp_filename = f"temp_{sanitized_filename}"
                    
                    # Download the old version to a temporary file
                    download_version(service, item['id'], version['id'], temp_filename)
                    
                    # Upload the sanitized file back to Google Drive
                    upload_file(service, folder_id, sanitized_filename, temp_filename)
                    
                    # Remove the temporary file
                    os.remove(temp_filename)
                    break  # Stop after downloading the closest version
        else:
            print(f"Skipping file: {item['name']} (Already rescued or not encrypted)")

def main(folder_id, target_date):
    """Main function to authenticate and rescue encrypted files."""
    service = authenticate()

    # Parse the target date and make it timezone-aware (UTC)
    target_datetime = datetime.datetime.strptime(target_date, "%Y-%m-%d").replace(tzinfo=pytz.UTC)

    # Start the recursive rescue process from the specified folder
    traverse_and_rescue(service, folder_id, target_datetime)

if __name__ == '__main__':
    # Replace with the folder ID you want to start from (root folder or specific subfolder)
    folder_id = 'FOLDER_ID_TO_RECOVER'
    # Change the target date to the desired one (format: YYYY-MM-DD)
    target_date = "2024-10-15"
    main(folder_id, target_date)
