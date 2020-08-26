import requests


class req:
    @staticmethod
    def send(token):
        url = 'http://ec2-3-85-144-25.compute-1.amazonaws.com/api/api/uploadimg/1'
        files = {'image': open('399360fc22f7c5310ef0efe4ff09c9f8.jpg', 'rb')}
        headers = {
            'Authorization': "Bearer " + token
        }
        requests.post(url, files=files, headers=headers)
    @staticmethod
    def login():
        pload = {'email': 'pruebas@mail.com', 'password': 'pruebas'}
        r = requests.post('http://ec2-3-85-144-25.compute-1.amazonaws.com/api/emp/login', data=pload)
        print(r.json()['token'])
        return r.json()['token']


req.send = staticmethod(req.send)