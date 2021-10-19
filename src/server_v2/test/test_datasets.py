import os

from .utils import ApiHelper


def test_datasets():
    api = ApiHelper('http://localhost:8000/api', 'ralph', 'arturo4ever')
    api.create_token()
    file_paths = []
    for f in os.listdir('data'):
        file_paths.append(os.path.join('data', f))
    response = api.post_files('/datasets/create', file_paths)
    assert response.json()['name'] != ''
    response = api.get('/datasets/')
    assert len(response.json()) > 0
    items = response.json()
    for item in items:
        api.delete('/datasets/{}'.format(item['id']))
