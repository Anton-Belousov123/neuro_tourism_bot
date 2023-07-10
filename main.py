import openai
import os
import dotenv
from flask import Flask, request

import ggl
import db
import amo

dotenv.load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)


def translate_to_russian(text):
    messages = [
        {'role': 'assistant', 'content': "Переведи текст на русский язык"},
        {'role': 'user', 'content': text}
    ]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )['choices'][0]['message']['content']
    return response


@app.route('/', methods=["POST"])
def main():
    request_dict = request.form.to_dict()
    name, text, image = request_dict['message[add][0][author][name]'], request_dict['message[add][0][text]'], ''

    user_id = request_dict['message[add][0][chat_id]']
    if 'message[add][0][author][avatar_url]' in request_dict.keys():
        image = request_dict['message[add][0][author][avatar_url]']

    messages = [{"role": "system", "content": ggl.get_annotation()}]
    pipeline = amo.get_pipeline(image, name, text)
    if pipeline is None: return 'ok'

    if text == '/restart':
        db.clear_history(user_id)
        return 'ok'

    db.add_message(user_id, text, 'user')

    token, session = amo.get_token()
    amo.send_notes(pipeline, session, translate_to_russian(text))

    messages += db.read_history(user_id)

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )['choices'][0]['message']['content']

    db.add_message(user_id, response, 'assistant')
    amo.send_message(user_id, response)
    token, session = amo.get_token()
    amo.send_notes(pipeline, session, translate_to_russian(response))
