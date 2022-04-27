import requests
import json
import pytest


class Test(object):

    def user(self):

        headers = {
            "Content-type": "Application/json"
        }
        data = {
            "name": "Hanna Sali",
            "email": "hannay@.com",
            "password": 1234567
        }

        r = requests.post(url='http://restapi.adequateshop.com/api/authaccount/registration', headers=headers,
                          data=json.dumps(data))
        assert r.status_code == 201

        headers = {
            "Content-type": "Application/json"
        }
        data = {
            "email": "hannay@.com",
            "password": 1234567
        }

        r = requests.post(url='http://restapi.adequateshop.com/api/authaccount/login',
                          headers=headers, data=json.dumps(data))
        assert r.status_code == 200

    def exist_user(self):
        headers = {
            "Content-type": "Application/json"
        }
        data = {
            "name": "Hanna Sali",
            "email": "hannay@.com",
            "password": 1234567
        }
        r = requests.post(url='http://restapi.adequateshop.com/api/authaccount/registration',
                          headers=headers, data=json.dumps(data))
        assert r.json()["message"] == "The email address you have entered is already registered"

    @pytest.fixture()
    def get_token(self):
        headers = {
            "Content-type": "Application/json"
        }
        data = {
            "email": "hanna@.com",
            "password": 1234567
        }
        r = requests.post(url='http://restapi.adequateshop.com/api/authaccount/login',
                          headers=headers, data=json.dumps(data))
        authorization = r.json()["data"]["Token"]
        headers["Authorization"] = 'Bearer ' + authorization
        return headers

    def new_user(self, token_taker):
        data = {
            "id": "",
            "name": "Olle6",
            "email": "olle6@.com",
            "location": "SE"
        }

        r = requests.post(url='http://restapi.adequateshop.com/api/authaccount/registration', headers=token_taker,
                          data=json.dumps(data))
        assert r.status_code == 200


    def id_get(self, token_taker, data):
        p = requests.get(url='http://restapi.adequateshop.com/api/users?page=1', headers=token_taker)
        item = p.json()["total_pages"]
        n = int(item)
        while True:
            r = requests.get(url='http://restapi.adequateshop.com/api/users?page=' + f'{str(item)}',
                             headers=token_taker)
            for user in r.json()["data"]:
                if user["email"] == data["email"]:
                    return user["id"]

            n += 1

    @pytest.fixture()
    def update_user(self, id_finder, token_taker):

        data = {
            "id": "",
            "name": "Olle6",
            "email": "olle6@.com",
            "location": "SEe"
        }

        user_id = id_finder
        data["id"] = user_id

        r = requests.put(url='http://restapi.adequateshop.com/api/users/' + str(user_id), headers=token_taker,
                         data=json.dumps(data))
        assert r.status_code == 200

        r = requests.get(url='http://restapi.adequateshop.com/api/users/' + str(user_id), headers=token_taker)
        assert r.status_code == 200