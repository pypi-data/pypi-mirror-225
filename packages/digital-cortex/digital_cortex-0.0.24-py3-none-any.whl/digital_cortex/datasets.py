import requests

from digital_cortex.config import config
from digital_cortex.models.datasets import *

HOST_URL = config.HOST_URL

BASE_PATH = "/api/v1/datasets"


def get_all_datasets_type(token: str):
    url = HOST_URL + BASE_PATH + "/types"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers).json()
    return response


def get_all_users_datasets(token: str):
    url = HOST_URL + BASE_PATH
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def get_local_files(token: str):
    url = HOST_URL + BASE_PATH + "/fileon/local"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def get_particular_dataset(token: str, dataset_id: str):
    url = HOST_URL + BASE_PATH + f"/{dataset_id}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def get_user_and_published_datasets(token: str):
    url = HOST_URL + BASE_PATH + "/userandpublished"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers).json()
    return response


def create_remote_file_dataset(token: str, dataset_url_form: DatasetUrlForm):
    url = HOST_URL + BASE_PATH + "/url/create"

    payload = dataset_url_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.text


def create_cloud_file_dataset(token: str, dataset_cloud_file_form: DatasetCloudFileForm):
    url = HOST_URL + BASE_PATH + "/file/cloud/create"

    payload = dataset_cloud_file_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.text


def create_local_file_dataset(token: str, dataset_local_file_form: DatasetLocalFileForm, file_path: str):
    url = HOST_URL + BASE_PATH + '/file/local/create'
    payload = {
        'datasetForm': dataset_local_file_form.model_dump_json(),
        'file': ('codeFile', open(file_path, 'rb'))
    }

    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.post(url, headers=headers, files=payload)
    return response.text


def create_database_dataset(token: str, database_dataset_form: DatabaseDatasetForm):
    url = HOST_URL + BASE_PATH + '/database/create'
    payload = database_dataset_form.model_dump_json()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.text


def is_exists(token: str, name: str, id: str = None):
    if id is None:
        url = HOST_URL + BASE_PATH + f"/isexists?name={name}"
    else:
        url = HOST_URL + BASE_PATH + f"/isexists?name={name}&id={id}"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers).json()
    return response


def attach_tags(token: str, tag_form: TagForm):
    url = HOST_URL + BASE_PATH + '/attachtags'
    payload = tag_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.text


def detach_tags(token: str, tag_form: TagForm):
    url = HOST_URL + BASE_PATH + '/detachtags'
    payload = tag_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.delete(url, headers=headers, data=payload)
    return response.text


def get_all_published_datasets(token: str):
    url = HOST_URL + BASE_PATH + "/published"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def publish_dataset(token: str, dataset_id: str):
    url = HOST_URL + BASE_PATH + f"/{dataset_id}/publish"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.put(url, headers=headers).json()
    return response


def delete_dataset(token: str, dataset_id: str):
    url = HOST_URL + BASE_PATH + f"/{dataset_id}/delete"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.delete(url, headers=headers).json()
    return response


def is_used_in_pipeline(token: str, dataset_id: str):
    url = HOST_URL + BASE_PATH + f"/{dataset_id}/isusedinpipeline"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers).json()
    return response


def update_remote_file_dataset(token: str, update_dataset_url_form: UpdateDatasetUrlForm):
    url = HOST_URL + BASE_PATH + '/update/url'
    payload = update_dataset_url_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, data=payload)
    return response.text


def update_cloud_file_dataset(token: str, update_dataset_cloud_file_form: UpdateDatasetCloudFileForm):
    url = HOST_URL + BASE_PATH + '/update/file/cloud'
    payload = update_dataset_cloud_file_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, data=payload)
    return response.text


def update_local_file_dataset(token: str, update_dataset_local_file_form: UpdateDatasetLocalFileForm):
    url = HOST_URL + BASE_PATH + '/update/file/local'
    payload = update_dataset_local_file_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, data=payload)
    return response.text


def update_database_dataset(token: str, update_database_dataset_form: UpdateDatabaseDatasetForm):
    url = HOST_URL + BASE_PATH + '/update/database'
    payload = update_database_dataset_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, data=payload)
    return response.text


def update_general_fields(token: str, update_general_fields_form: UpdateGeneralFieldsForm):
    url = HOST_URL + BASE_PATH + '/update/generalfields'
    payload = update_general_fields_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, data=payload)
    return response.text


def update_description(token: str, update_description_form: UpdateDescriptionForm):
    url = HOST_URL + BASE_PATH + '/update/description'
    payload = update_description_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, data=payload)
    return response.text


def validate_database(token: str, db_info: DBInfo):
    url = HOST_URL + BASE_PATH + '/database/validate'
    payload = db_info.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.text


def get_pending_actions(token: str, dataset_id: str):
    url = HOST_URL + BASE_PATH + f"/{dataset_id}/pendingactions"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers).json()
    return response
