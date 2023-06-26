import difflib
import time

from flask import Flask, request
import dotenv

import amocrm
import db
import deepl
import ggl
import usefini

app = Flask(__name__)
dont_know_words = open('dk.txt', 'r').read().split('\n')
dotenv.load_dotenv()


def get_simantic_status(mode, text):
    info = open(mode).read().split('\n')
    for s1 in text.split():
        for s2 in info:
            matcher = difflib.SequenceMatcher(None, s1.lower(), s2.lower())
            if matcher.ratio() >= 0.8:
                return True
    return False


@app.route('/', methods=["POST"])
def main():
    request_dict = request.form.to_dict()
    name, text, image = request_dict['message[add][0][author][name]'], request_dict['message[add][0][text]'], ''

    if 'message[add][0][author][avatar_url]' in request_dict.keys():
        image = request_dict['message[add][0][author][avatar_url]']
    pipeline = amocrm.get_pipeline(image, name, text)
    if pipeline is None: return 'ok'
    chat_id = request_dict['message[add][0][chat_id]']
    if text == '/restart':
        db.restart(chat_id)
        return 'ok'

    if int(request_dict['message[add][0][created_at]']) + 10 < int(time.time()): return 'ok'
    token, session = amocrm.get_token()
    _, translation_notes = deepl.translate_it(text, 'RU')
    amocrm.send_notes(pipeline, session, translation_notes)
    chat_history = amocrm.get_chat_history(chat_id)
    order_info = db.get_order_info(chat_id)
    messages_to_user = ggl.get_messages()
    source_language, _ = deepl.translate_it(chat_history, 'EN')
    _, text_translated = deepl.translate_it(text, 'EN')
    dk_status = get_simantic_status('dk.txt', text_translated)
    answer = ''
    print(text_translated, dk_status)
    is_answer_correct = False
    if '?' in text_translated:
        answer += usefini.ask_question(text_translated)

    if order_info == 1 or dk_status:
        is_answer_correct = True


    elif order_info == 2:
        for word in text_translated.split():

            if str(word).isdigit() and len(word) == 1:
                is_answer_correct = True


    elif order_info == 3:
        if get_simantic_status('build_status.txt', text_translated):
            is_answer_correct = True


    elif order_info == 4:
        for word in text_translated.split():
            if str(word).isdigit():
                is_answer_correct = True
# incorrect работает блок определения языка

    if is_answer_correct:
        db.plus_one(chat_id)
        answer += '\n\n' + messages_to_user[order_info]

    else:
        answer += '\n\n' + messages_to_user[order_info - 1]


    _, translated_to_user = deepl.translate_it(answer.strip(), source_language)
    amocrm.send_message(chat_id, translated_to_user)
    token, session = amocrm.get_token()
    _, translation_notes = deepl.translate_it(translated_to_user, 'RU')
    amocrm.send_notes(pipeline, session, translation_notes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
