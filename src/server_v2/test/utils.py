import os
import requests


class ApiHelper:

    # TODO: Finish this!

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        if self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]
        self.username = username
        self.password = password
        self.token = self.create_token()

    def create_token(self):
        response = requests.post(
            '{}/tokens/'.format(self.base_url),
            data={'username': self.username, 'password': self.password})
        assert response.status_code == 200, 'User {} may not exist'.format(self.username)
        return response.json()['token']

    def get(self, endpoint):
        if not endpoint.startswith('/'):
            endpoint = '/{}'.format(endpoint)
        response = requests.get(
            '{}{}'.format(self.base_url, endpoint),
            headers={'Authorization': 'Token {}'.format(self.token)})
        assert response.status_code == 200
        return response

    def post_files(self, endpoint, file_paths):
        if not endpoint.startswith('/'):
            endpoint = '/{}'.format(endpoint)
        files = {}
        for file_path in file_paths:
            files[os.path.split(file_path)[1]] = open(file_path, 'rb')
        response = requests.post(
            '{}{}'.format(self.base_url, endpoint),
            headers={'Authorization': 'Token {}'.format(self.token)}, files=files)
        assert response.status_code == 201
        return response

    def delete(self, endpoint):
        if not endpoint.startswith('/'):
            endpoint = '/{}'.format(endpoint)
        response = requests.delete(
            '{}{}/delete'.format(self.base_url, endpoint),
            headers={'Authorization': 'Token {}'.format(self.token)})
        assert response.status_code == 200
        return response
