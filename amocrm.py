import json
import os
import time
import requests
import bs4

def get_token():
    try:
        session = requests.Session()
        response = session.get('https://kevgenev8.amocrm.ru/')
        session_id = response.cookies.get('session_id')
        csrf_token = response.cookies.get('csrf_token')
        headers = {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': f'session_id={session_id}; '
                      f'csrf_token={csrf_token};'
                      f'last_login=kevgenev8@mail.ru',
            'Host': 'kevgenev8.amocrm.ru',
            'Origin': 'https://kevgenev8.amocrm.ru',
            'Referer': 'https://kevgenev8.amocrm.ru/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
        payload = {
            'csrf_token': csrf_token,
            'password': "Xh1wdBlk",
            'temporary_auth': "N",
            'username': "kevgenev8@mail.ru"}

        response = session.post('https://kevgenev8.amocrm.ru/oauth2/authorize', headers=headers, data=payload)
        access_token = response.cookies.get('access_token')
        refresh_token = response.cookies.get('refresh_token')
        headers['access_token'], headers['refresh_token'] = access_token, refresh_token
        payload = {'request[chats][session][action]': 'create'}
        response = session.post('https://kevgenev8.amocrm.ru/ajax/v1/chats/session', headers=headers, data=payload)
        token = response.json()['response']['chats']['session']['access_token']
    except:
        time.sleep(3)
        return get_token()
    print('New token:', token)
    return token, session



def get_pipeline(image, s_name, text):
    token, session = get_token()
    url = 'https://kevgenev8.amocrm.ru/leads/pipeline/6731170/?skip_filter=Y'

    response = session.get(url, timeout=15)
    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    for i in soup.find_all('div', {'class': 'pipeline-unsorted__item-data'}):
        img = i.find('div', {'class': 'pipeline-unsorted__item-avatar'}). \
            get('style').replace("background-image: url(", '').replace(')', '')

        name = i.find('a', {'class': 'pipeline-unsorted__item-title'}).text
        message = i.find('div', {'class': 'pipeline_leads__linked-entities_last-message__text'}).text
        pipeline = i.find('a', {'class': 'pipeline-unsorted__item-title'}).get('href').split('/')[-1]
        if (img == image) or (message == text and s_name == name):
            return pipeline
    return None


def get_chat_history(receiver_id, token='', chat_history=""):
    while True:
        try:
            headers = {'X-Auth-Token': token}
            url = f'https://amojo.amocrm.ru/messages/{os.getenv("ACCOUNT_CHAT_ID")}/merge?stand=v15' \
                  f'&offset=0&limit=100&chat_id%5B%5D={receiver_id}&get_tags=true&lang=ru'
            chat_history = requests.get(url, headers=headers).json()['message_list']

        except Exception as e:
            print(e, 1)
            token, session = get_token()
            continue
        break
    texts = ''
    for i in chat_history[0]:
        if '/restart' in i['text']:
            break
        texts += f'\n\n{i["text"]}'
    return texts.strip()

def send_notes(pipeline_id, session, text):
    url = f'https://kevgenev8.amocrm.ru/private/notes/edit2.php?parent_element_id={pipeline_id}&parent_element_type=2'
    data = {
        'DATE_CREATE': int(time.time()),
        'ACTION': 'ADD_NOTE',
        'BODY': text,
        'ELEMENT_ID': pipeline_id,
        'ELEMENT_TYPE': '2'
    }
    resp = session.post(url, data=data)




def send_message(receiver_id: str, message: str, token=''):
    while True:
        try:
            headers = {'X-Auth-Token': token}
            url = f'https://amojo.amocrm.ru/v1/chats/{os.getenv("ACCOUNT_CHAT_ID")}/' \
                  f'{receiver_id}/messages?with_video=true&stand=v15'
            response = requests.post(url, headers=headers, data=json.dumps({"text": message}))
            print(response.status_code)
            if response.status_code != 200:
                raise Exception("Токен не подошел!")
        except Exception as e:
            print(e, 2)
            token, session = get_token()
            continue
        break

