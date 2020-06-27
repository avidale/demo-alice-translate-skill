import unittest.mock

from main import handler
from translation import translate


def test_main():
    context = unittest.mock.Mock()
    context.token = {'access_token': 'abcde'}
    event = {
        'version': 1,
        'session': {},
        'request': {
            'command': 'переведи слово katze с немецкого на английский',
            'nlu': {
                'intents': {
                    'translate_full': {
                        'slots': {
                            'phrase': {'value': 'katze'},
                            'from': {'value': 'de'},
                            'to': {'value': 'en'},
                        }
                    }
                }
            }
        }
    }
    with unittest.mock.patch('main.translate') as mock_translate:
        mock_translate.return_value = None, 'cat'
        resp = handler(event=event, context=context)
        mock_translate.assert_called_with(token='abcde', lang_from='de', lang_to='en', text='katze')
    assert resp['response']['text'] == 'cat'


def test_translate():
    with unittest.mock.patch('translation.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json = lambda: {'translations': [{'text': 'cat'}]}
        result = translate(lang_from='de', lang_to='en', token='abcde', text='katze')
        mock_post.assert_called()
    assert result == (None, 'cat')


def test_translate_without_token():
    error, result = translate(lang_from='de', lang_to='en', token=None, text='katze')
    assert error
    assert not result
