import logging
import re
import requests


def detect_lang(text, token, hint='ru'):
    data = {
        'text': text,
        'languageCodeHints': [hint],
    }
    resp = requests.post(
        url='https://translate.api.cloud.yandex.net/translate/v2/detect',
        json=data,
        headers={
            'Authorization': 'Bearer ' + token,
        }
    )
    if resp.status_code != 200:
        return None
    j = resp.json()
    return j['languageCode']


def translate(text, token, lang_to='ru', lang_from=None):
    if not token:
        error = f'Чтобы перевести "{text}" с {lang_from} на {lang_to}, ' \
                'нужно при создании функции указать сервисный аккаунт, ' \
                'тогда вы получите IAM токен для доступа к API переводчика.'
        return error, None
    data = {
        'texts': [text],
        'targetLanguageCode': lang_to,
    }
    if lang_from is None:
        lang_from = detect_lang(token=token, text=text)
        if lang_from is None:
            return 'Не поняла, на каком языке это.', ''
    data['sourceLanguageCode'] = lang_from
    logging.info('translating data: {}'.format(data))
    resp = requests.post(
        url='https://translate.api.cloud.yandex.net/translate/v2/translate',
        json=data,
        headers={
            'Authorization': 'Bearer ' + token,
        }
    )
    if resp.status_code != 200:
        return 'Не достучался до переводчика: {}'.format(resp.text), ''

    j = resp.json()
    return None, j['translations'][0]['text']


def is_like_russian(text):
    if not text:
        return False
    text = text.lower().strip()
    return re.match('^[а-яё ]+$', text)
