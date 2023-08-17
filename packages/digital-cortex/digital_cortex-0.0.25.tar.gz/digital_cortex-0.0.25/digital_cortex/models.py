import requests

from digital_cortex.config import config
from digital_cortex.domain.models import *

HOST_URL = config.HOST_URL

BASE_PATH = "/api/v1/models"


def get_all_base_models(token: str):
    url = HOST_URL + "/api/v1/basemodels"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def get_all_tasks(token: str):
    url = HOST_URL + "/api/v1/tasks"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def get_all_user_models(token: str):
    url = HOST_URL + BASE_PATH
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


def get_all_published_models(token: str):
    url = HOST_URL + BASE_PATH + "/published"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def publish_model(token: str, model_id: str):
    url = HOST_URL + BASE_PATH + f"/{model_id}/publish"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.put(url, headers=headers).json()
    return response


def get_particular_model(token: str, model_id: str):
    url = HOST_URL + BASE_PATH + f"/{model_id}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def get_user_and_published_models(token: str):
    url = HOST_URL + BASE_PATH + "/userandpublished"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def update_model_attached_tasks(token: str, update_task_form: UpdateTaskForm):
    url = HOST_URL + BASE_PATH + '/update/tasks'
    payload = update_task_form.model_dump_json()

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


def get_pending_actions(token: str, model_id: str):
    url = HOST_URL + BASE_PATH + f"/{model_id}/pendingactions"
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


def create_regex_model(token: str, regex_model_form: RegexModelForm, file_path: str):
    url = HOST_URL + BASE_PATH + '/regex/import'
    payload = {
        'modelForm': regex_model_form.model_dump_json(),
        'file': ('file', open(file_path, 'rb'))

    }
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.post(url, headers=headers, files=payload)
    return response.text


def create_pytorch_model(token: str, pytorch_model_form: PyTorchModelForm, file_path: str):
    url = HOST_URL + BASE_PATH + '/pytorch/create'
    payload = {
        'modelForm': pytorch_model_form.model_dump_json(),
        'file': ('file', open(file_path, 'rb'))
    }
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.post(url, headers=headers, files=payload)
    return response.text


def update_pytorch_model(token: str, update_pytorch_model_form: UpdatePytorchModelForm):
    url = HOST_URL + BASE_PATH + '/pytorch/update'
    payload = update_pytorch_model_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, data=payload)
    return response.text


def create_trained_model(token: str, create_trained_model_form: TrainedModelForm):
    url = HOST_URL + BASE_PATH + '/trainedmodel/create'
    payload = create_trained_model_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.text


def update_trained_model(token: str, update_trained_model_form: UpdateTrainedModelForm):
    url = HOST_URL + BASE_PATH + '/trainedmodel/update'
    payload = update_trained_model_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, data=payload)
    return response.text


def get_trained_and_base_models(token: str):
    url = HOST_URL + BASE_PATH + '/trainedandbasemodels'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(url, headers=headers)
    return response.text


def delete_model(token: str, model_id: str):
    url = HOST_URL + BASE_PATH + f"/{model_id}/delete"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.delete(url, headers=headers).json()
    return response


def is_used_in_pipeline(token: str, model_id: str):
    url = HOST_URL + BASE_PATH + f"/{model_id}/isusedinpipeline"
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers).json()
    return response
