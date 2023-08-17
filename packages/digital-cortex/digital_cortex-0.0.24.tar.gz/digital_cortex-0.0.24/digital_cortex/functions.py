import requests

from digital_cortex.models.functions import *
from digital_cortex.config import config

HOST_URL = config.HOST_URL

BASE_PATH = '/api/v1/functions'


def get_all_function_engine(token):
    url = HOST_URL + BASE_PATH + "/engines"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers).json()
    return response


def get_all_user_function(token: str):
    url = HOST_URL + BASE_PATH
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def get_particular_function(token: str, function_id: str):
    url = HOST_URL + BASE_PATH + f"/{function_id}"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers).json()
    return response


def get_all_published_function(token: str):
    url = HOST_URL + BASE_PATH + "/published"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def get_user_and_published_function(token: str):
    url = HOST_URL + BASE_PATH + "/userandpublished"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def create_function(token: str, function_form: FunctionForm, code_file_path: str = None,
                    dependency_file_path: str = None):
    url = HOST_URL + BASE_PATH + '/create'
    payload = {
        'functionForm': function_form.model_dump_json()
    }
    if code_file_path:
        payload['codeFile'] = ('codeFile', open(code_file_path, 'rb'))

    if dependency_file_path:
        payload['dependencyFile'] = ('dependencyFile', open(dependency_file_path, 'rb'))

    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.post(url, headers=headers, files=payload)
    return response.text


def update_code(token: str, update_function_code_form: UpdateFunctionCodeForm):
    url = HOST_URL + BASE_PATH + "/update/code"

    payload = update_function_code_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, data=payload)
    return response.text


def update_code_file(token: str, function_id: str, code_file_path: str):
    url = HOST_URL + BASE_PATH + "/update/codefile"
    payload = {
        'id': function_id,
        'codeFile': ('codeFile', open(code_file_path, 'rb'))
    }

    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.put(url, headers=headers, files=payload)
    return response.text


def update_dependency(token: str, update_dependency_form: UpdateDependencyForm, dependency_file_path: str = None):
    url = HOST_URL + BASE_PATH + '/update/dependency'
    payload = {
        'updateDependencyForm': update_dependency_form.model_dump_json()
    }

    if dependency_file_path:
        payload['dependencyFile'] = ('dependencyFile', open(dependency_file_path, 'rb'))

    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.put(url, headers=headers, files=payload)
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


def update_general_fields(token: str, update_general_fields_form: UpdateGeneralFieldsForm):
    url = HOST_URL + BASE_PATH + '/update/generalfields'
    payload = update_general_fields_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, data=payload)
    return response.text


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


def get_pending_actions(token: str, function_id: str):
    url = HOST_URL + BASE_PATH + f"/{function_id}/pendingactions"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers).json()
    return response


def publish_function(token: str, function_id: str):
    url = HOST_URL + BASE_PATH + f"/{function_id}/publish"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.put(url, headers=headers).json()
    return response


def remove_dependency(token: str, function_id: str):
    url = HOST_URL + BASE_PATH + f"/{function_id}/removedependency"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.delete(url, headers=headers).json()
    return response


def delete_function(token: str, function_id: str):
    url = HOST_URL + BASE_PATH + f"/{function_id}/delete"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.delete(url, headers=headers).json()
    return response


def is_used_in_pipeline(token: str, function_id: str):
    url = HOST_URL + BASE_PATH + f"/{function_id}/isusedinpipeline"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers).json()
    return response


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


def execute(token: str, function_id: str, payload: dict):
    url = HOST_URL + BASE_PATH + f'/execute/{function_id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.text
