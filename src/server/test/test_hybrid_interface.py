from .utils import ApiHelper


def test_api():
    api = ApiHelper('http://localhost:8000/api', 'ralph', 'arturo4ever')
    api.create_token()
    response = api.get('/')
    assert response.json()['message'] == 'Hello!'


def test_html():
    import requests
    response = requests.get('http://0.0.0.0:8000/login/', params={'username': 'ralph', 'password': 'arturo4ever'})
    assert response.status_code == 200
    response = requests.get('http://0.0.0.0:8000/', cookies=response.cookies)
    assert response.status_code == 200
    assert 'Maastricht University' in response.text
