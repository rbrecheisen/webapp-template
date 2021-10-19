import requests


def get_token(username, password):
    result = requests.post('http://localhost:8000/token-requests/', data={'username': username, 'password': password})
    assert result.status_code == 200, 'User {} may not exist'.format(username)
    return result.json()['token']


class Api:

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password

    def get_token(self):
        response = requests.post(
            '{}/token-requests/'.format(self.base_url), data={'username': self.username, 'password': self.password})
        assert response.status_code == 200, 'User {} may not exist'.format(username)
        return response.json()['token']

    def post_files(self, endpoint):
        pass
