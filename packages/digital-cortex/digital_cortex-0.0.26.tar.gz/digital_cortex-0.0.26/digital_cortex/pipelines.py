import requests

from digital_cortex.config import config
from digital_cortex.domain.pipelines import *

HOST_URL = config.HOST_URL

BASE_PATH = "/api/v1/pipelines"


def get_all_pipeline_types(token: str):
    url = HOST_URL + BASE_PATH + "/types"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def get_all_user_pipelines(token: str):
    url = HOST_URL + BASE_PATH
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def get_particular_pipeline(token: str, pipeline_id: str):
    url = HOST_URL + BASE_PATH + f"/{pipeline_id}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def create_etl_pipeline(token: str, etl_pipeline_form: EtlPipelineForm):
    url = HOST_URL + BASE_PATH + '/etl/create'
    payload = etl_pipeline_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': "application/json"
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.text


def update_etl_pipeline(token: str, update_etl_pipeline_form: UpdateEtlPipelineForm):
    url = HOST_URL + BASE_PATH + '/etl/update'
    payload = update_etl_pipeline_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': "application/json"
    }
    response = requests.put(url, headers=headers, data=payload)
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


def publish_pipeline(token: str, pipeline_id: str):
    url = HOST_URL + BASE_PATH + f"/{pipeline_id}/publish"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.put(url, headers=headers).json()
    return response


def get_all_published_pipelines(token: str):
    url = HOST_URL + BASE_PATH + "/published"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def update_description(token: str, update_description_form: UpdateDescriptionForm):
    url = HOST_URL + BASE_PATH + '/update/description'
    payload = update_description_form.model_dump_json()

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


def get_pending_actions(token: str, pipeline_id: str):
    url = HOST_URL + BASE_PATH + f"/{pipeline_id}/pendingactions"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers).json()
    return response


def delete_pipeline(token: str, pipeline_id: str):
    url = HOST_URL + BASE_PATH + f"/{pipeline_id}/delete"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.delete(url, headers=headers).json()
    return response
