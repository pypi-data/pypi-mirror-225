import pandas as pd
from google.cloud import storage
from pathlib import Path


def get_csv_from_gcs(bucket_name, path):
    full_path = 'gs://{bucket}/{path}'.format(bucket=bucket_name, path=path)
    file_type = path.split(".")[-1]
    result_df = pd.DataFrame()
    if file_type == 'csv':
        result_df = pd.read_csv(full_path)
    elif file_type == 'xlsx' or file_type == 'xls':
        result_df = pd.read_excel(full_path, engine='openpyxl')
    return result_df


def get_all_file_from_gcs_folder(bucket_name, path, file_type='csv'):
    file_dict = {}
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        for blob in bucket.list_blobs(prefix=str(path)):
            current_path = Path(blob.name)
            if str(current_path) != str(path):
                full_path = 'gs://{bucket}/{path}'.format(bucket=bucket_name, path=str(current_path))
                file = pd.DataFrame()
                if file_type == 'csv':
                    file = pd.read_csv(full_path)
                elif file_type == 'excel':
                    file = pd.read_excel(full_path)
                file_dict[current_path] = file
    except Exception as e:
        raise e
    return file_dict


def get_file_as_string_from_gcs(bucket_name, path) -> bytes:
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(path)

    # Download the contents of the blob as a string and then parse it using json.loads() method
    return blob.download_as_string(client=None)

