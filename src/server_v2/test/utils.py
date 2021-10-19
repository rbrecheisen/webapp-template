import requests


def get_token(username, password):
    result = requests.post('http://localhost:8000/token-requests/', data={'username': username, 'password': password})
    assert result.status_code == 200, 'User {} may not exist'.format(username)
    return result.json()['token']
