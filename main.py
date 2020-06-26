import os
import pymongo
import datetime


from translation import translate, is_like_russian

INTRO_TEXT = 'Привет! Вы находитесь в приватном навыке "Крот-Полиглот". ' \
    'Скажите, какое слово вы хотите перевести с какого на какой язык.' \
    'Чтобы выйти, скажите "Хватит".'


# If you want to store logs, please connect a mongodb cluster.
# You can get a free one on https://cloud.mongodb.com.
MONGODB_URI = os.environ.get('MONGODB_URI')
db = None
logs_collection = None
if MONGODB_URI:
    # w=0 means fast non-blocking write
    client = pymongo.MongoClient(MONGODB_URI, w=0)
    db = client.get_default_database()
    logs_collection = db.get_collection('logs')


def do_translate(form, translate_state, token):
    api_req = {
        'text': form['slots'].get('phrase', {}).get('value'),
        'lang_from': form['slots'].get('from', {}).get('value'),
        'lang_to': form['slots'].get('to', {}).get('value'),
    }
    api_req = {k: v for k, v in api_req.items() if v}
    translate_state.update(api_req)
    if 'text' not in translate_state:
        return 'Не поняла, какой текст нужно перевести', translate_state
    if is_like_russian(translate_state['text']) and 'lang_to' not in translate_state:
        return 'На какой язык нужно перевести?', translate_state
    if not is_like_russian(translate_state['text']) and 'lang_from' not in translate_state:
        return 'С какого языка нужно перевести?', translate_state
    tran_error, tran_result = translate(**translate_state, token=token)
    text = tran_error or tran_result
    return text, translate_state


def handler(event, context):
    # токен для доступа к API перевода забираем прямо из функции, если у вас есть сервисный аккаунт
    token = None
    if context and hasattr(context, 'token') and context.token:
        token = context.token.get('access_token')

    translate_state = event.get('state', {}).get('session', {}).get('translate', {})
    last_phrase = event.get('state', {}).get('session', {}).get('last_phrase')
    intents = event.get('request', {}).get('nlu', {}).get('intents', {})
    command = event.get('request', {}).get('command')

    text = INTRO_TEXT
    end_session = 'false'

    translate_full = intents.get('translate_full')
    if intents.get('exit'):
        text = 'Приятно было попереводить для вас! ' \
               'Чтобы вернуться в навык, скажите "Запусти навык Крот-Полиглот". До свидания!'
        end_session = 'true'
    elif intents.get('help'):
        text = INTRO_TEXT
    elif intents.get('repeat'):
        if last_phrase:
            text = last_phrase
        else:
            text = 'Ох, я забыл, что нужно повторить. Попросите меня лучше что-нибудь перевести.'
    elif not token:
        text = 'Чтобы навык заработал, нужно при создании функции указать сервисный аккаунт, ' \
               'тогда вы получите IAM токен для доступа к API переводчика..'
    elif translate_full:
        text, translate_state = do_translate(translate_full, translate_state, token=token)
    elif command:
        text = 'Не понял вас. Чтобы выйти из навыка "Крот-Полиглот", скажите "Хватит".'

    response = {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': end_session
        },
        'session_state': {'translate': translate_state, 'last_phrase': text}
    }

    utterance = event.get('request', {}).get('original_utterance')
    if logs_collection and utterance != 'ping':
        logs_collection.insert_one({
            'request': event,
            'response': response,
            'time': datetime.datetime.now(),
            'app_id': event['session'].get('application', {}).get('application_id'),
            'utterance': utterance,
            'response_text': response['response']['text'],
        })
    return response
