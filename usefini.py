import os

import requests


def ask_question(text):
    response = requests.post(
        'https://api.usefini.com/api/v1/answer',
        data={
            'question': text,
        },
        headers={"Authorization": "Bearer " + os.getenv('FINI_API_KEY')}
    ).json()
    return response['answer']
