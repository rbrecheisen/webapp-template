import requests


def get_token(username, password):
    result = requests.post('http://localhost:8000/token-requests/', data={'username': username, 'password': password})
    assert result.status_code == 200, 'User {} may not exist'.format(username)
    return result.json()['token']


########################################################################################################################
# TESTS
def test_api():
    token = get_token('ralph', 'arturo4ever')
    response = requests.get('http://localhost:8000?format=json', headers={'Authorization': 'Token {}'.format(token)})
    assert response.json()['message'] == 'Hello!'


def test_html():
    token = get_token('ralph', 'arturo4ever')
    response = requests.get('http://localhost:8000?format=html', headers={'Authorization': 'Token {}'.format(token)})
    assert 'Hello!' in response.text
