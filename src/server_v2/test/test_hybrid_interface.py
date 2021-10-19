import requests

from .utils import get_token


# def test_api():
#     token = get_token('ralph', 'arturo4ever')
#     response = requests.get('http://localhost:8000/api/', headers={'Authorization': 'Token {}'.format(token)})
#     assert response.json()['message'] == 'Hello!'
#
#
# def test_html():
#     response = requests.get('http://0.0.0.0:8000/login/', params={'username': 'ralph', 'password': 'arturo4ever'})
#     assert response.status_code == 200
#     response = requests.get('http://0.0.0.0:8000/', cookies=response.cookies)
#     assert response.status_code == 200
#     assert 'Hello!' in response.text
