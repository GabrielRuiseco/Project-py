import requests


def send(token):
    url = 'http://127.0.0.1:3000/api/uploadimg/1'
    files = {'image': open('399360fc22f7c5310ef0efe4ff09c9f8.jpg', 'rb')}
    headers = {
        'Authorization': "Bearer " + token
    }
    requests.post(url, files=files, headers=headers)


def login():
    pload = {'email': 'pruebas@mail.com', 'password': 'pruebas'}
    r = requests.post('http://127.0.0.1:3000/emp/login', data=pload)
    print(r.json()['token'])
    return r.json()['token']


token = login()
send(token)
