import requests

from digital_cortex.config import config
from digital_cortex.domain.scoring import *

HOST_URL = config.HOST_URL

BASE_PATH = "/api/v1/score"


def text_score(token: str, text_scoring_form: TextScoringForm):
    url = HOST_URL + BASE_PATH + '/text'
    payload = text_scoring_form.model_dump_json()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': "application/json"
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.text
