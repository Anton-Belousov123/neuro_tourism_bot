import requests
import os

import os
import openai
import dotenv

headers = {
    'Host': 'api.deepl.com',
    'Authorization': f'DeepL-Auth-Key {os.getenv("DEEPL_API_KEY")}',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/114.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}
dotenv.load_dotenv()


def translate_it(text: str, lang: str):
    response = requests.post(
        url='https://www.deepl.com/v2/translate',
        headers=headers,
        data={'text': text, 'target_lang': lang}).json()
    return response['translations'][0]['detected_source_language'], response['translations'][0]['text'].lower().strip()


def translate_it2(text: str, command: str):

    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
        {"role": "system", "content": command},
        {"role": "assistant", "content": text}]
    )
    return response['choices'][0]['message']['content']




