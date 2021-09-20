import requests


def test_user_can_get_token():
    result = requests.post(
        'http://127.0.0.1:8000/token-requests/', data={'username': 'ralph', 'password': 'arturo4ever'})
    assert result.status_code == 200
    assert 'token' in result.json().keys()
