import dropbox
from dropbox.exceptions import AuthError
from django.core.management.base import BaseCommand
from django.conf import settings
import pandas as pd


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.dropbox_list_files("")
        self.dropbox_download_file("/Tehnicna_naloga_za_Mid_Software_engineer.pdf", 'downloaded_file.pdf')

    @staticmethod
    def dropbox_connect():

        try:
            dbx = dropbox.Dropbox(settings.DROPBOX_ACCESS_TOKEN)
        except AuthError as e:
            print('Error connecting to Dropbox with access token: ' + str(e))
        return dbx

    def dropbox_list_files(self, path):
        """Return a Pandas dataframe of files in a given Dropbox folder path in the Apps directory.
        """

        dbx = self.dropbox_connect()

        try:
            files = dbx.files_list_folder(path).entries
            files_list = []
            for file in files:
                if isinstance(file, dropbox.files.FileMetadata):
                    metadata = {
                        'name': file.name,
                        'path_display': file.path_display,
                        'client_modified': file.client_modified,
                        'server_modified': file.server_modified
                    }
                    files_list.append(metadata)

            df = pd.DataFrame.from_records(files_list)
            return df.sort_values(by='server_modified', ascending=False)

        except Exception as e:
            print('Error getting list of files from Dropbox: ' + str(e))

    def dropbox_download_file(self, dropbox_file_path, local_file_path):
        """Download a file from Dropbox to the local machine."""

        try:
            dbx = self.dropbox_connect()

            with open(local_file_path, 'wb') as f:
                metadata, result = dbx.files_download(path=dropbox_file_path)
                f.write(result.content)
        except Exception as e:
            print('Error downloading file from Dropbox: ' + str(e))