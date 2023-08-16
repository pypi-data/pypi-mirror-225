import glob
import os
from google.cloud import storage


class BucketHelper:
    def __init__(self, project_id):
        self.project_id = project_id
        self.client = storage.Client(project=self.project_id)

    def upload_all_files_to_bucket(self, src_path, dest_bucket_name, dest_path):
        bucket_upload = self.client.bucket(dest_bucket_name)
        if os.path.isfile(src_path):
            blob = bucket_upload.blob(os.path.join(dest_path, os.path.basename(src_path)))
            blob.upload_from_filename(src_path)
            return
        for item in glob.glob(src_path + '/*'):
            if os.path.isfile(item):
                if item == ".keep":
                    continue
                blob = bucket_upload.blob(os.path.join(dest_path, os.path.basename(item)))
                blob.upload_from_filename(item)
            else:
                self.upload_to_bucket(item, dest_bucket_name, os.path.join(dest_path, os.path.basename(item)))

    def download_all_files_from_bucket(self, src_bucket_name, src_path, dest_path):
        bucket_download = self.client.bucket(src_bucket_name)
        blobs = bucket_download.list_blobs(prefix=src_path)
        for blob in blobs:
            if blob.name.endswith("/"):
                continue
            file_name = os.path.join(dest_path, os.path.basename(blob.name))
            blob.download_to_filename(file_name)

# Example usage
# bucket = Bucket(project_id='your_project_id')
# bucket.upload_to_bucket(src_path='path/to/local/files', dest_bucket_name='your_bucket_name',
#                         dest_path='destination/path')
# bucket.download_from_bucket(src_bucket_name='your_bucket_name', src_path='source/path', dest_path='path/to/local/files')