import requests

from digital_cortex.config import config

HOST_URL = config.HOST_URL

BASE_PATH = "/api/v1/tags"


def get_all_tags(token: str):
    url = HOST_URL + BASE_PATH
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers).json()
    return response


def create_tag(token: str, tag_name: str):
    url = HOST_URL + BASE_PATH + f"/create?name={tag_name}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url, headers=headers).json()
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
