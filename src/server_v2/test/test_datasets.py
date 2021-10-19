import os
import requests

from .utils import get_token


def test_datasets():
    token = get_token('ralph', 'arturo4ever')
    files = {}
    for f in os.listdir('data'):
        files[f] = open(os.path.join('data', f), 'rb')
    response = requests.post(
        'http://localhost:8000/api/datasets/create', headers={'Authorization': 'Token {}'.format(token)}, files=files)
    assert response.status_code == 201
    assert response.json()['name'] != ''
    response = requests.get('http://localhost:8000/api/datasets/', headers={'Authorization': 'Token {}'.format(token)})
    assert response.status_code == 200
    assert len(response.json()) > 0
    items = response.json()
    for item in items:
        response = requests.delete('http://localhost:8000/api/datasets/{}/delete'.format(item['id']))
        # assert response.status_code == 200
