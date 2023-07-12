import time

import openai
import os
import dotenv
from flask import Flask, request

import misc
import db
import amo

dotenv.load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)




@app.route('/', methods=["POST"])
def main():
    request_dict = request.form.to_dict()
    name, text, image = request_dict['message[add][0][author][name]'], request_dict['message[add][0][text]'], ''
    print('Q:', text)
    user_id = request_dict['message[add][0][chat_id]']
    if 'message[add][0][author][avatar_url]' in request_dict.keys():
        image = request_dict['message[add][0][author][avatar_url]']

    if int(request_dict['message[add][0][created_at]']) + 10 < int(time.time()): return 'ok'

    messages = [{"role": "system", "content": misc.get_annotation()}]

    pipeline = amo.get_pipeline(image, name, text)
    print('Pipeline:', pipeline, 'ChatId:', user_id)
    if pipeline is None: return 'ok'

    if text == '/restart':
        db.clear_history(user_id)
        return 'ok'

    db.add_message(user_id, text, 'user')

    translation = misc.translate_to_russian(text)
    amo.send_notes(pipeline, translation)
    print('Q_T:', translation)
    messages += db.read_history(user_id)

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=messages
    )['choices'][0]['message']['content']

    db.add_message(user_id, response, 'assistant')
    amo.send_message(user_id, response)
    print('A:', response)
    translation = misc.translate_to_russian(response)
    amo.send_notes(pipeline, translation)
    print('A_T:', translation)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)