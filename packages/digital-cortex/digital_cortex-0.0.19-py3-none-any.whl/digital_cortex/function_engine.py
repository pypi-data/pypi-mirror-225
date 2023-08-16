import requests

from config import config

HOST_URL = config.HOST_URL

BASE_PATH = 'api/v1/functions/engines'


def get_all_function_engine(token):
    url = HOST_URL + BASE_PATH

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers, data=payload).json()
    return response


user_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTI0MjM5NDksImlhdCI6MTY4NzIzOTk0OSwidXNlcklkIjoiNmI0MWRlYzItNjA4Ni00OWFkLTg2NDAtODgyM2ZjM2NmMzkxIiwiZW1haWwiOiJ0aGlyZG5vcm1hbDkyMDJAZ21haWwuY29tIiwiZmlyc3ROYW1lIjoiQUJDIiwibGFzdE5hbWUiOiJYWVoifQ.mPRcnaE87TW3ZcP0jcnedVDuAD1-6aYuApU1UkKM8Dw"
get_all_function_engine(user_token)
