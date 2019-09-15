import unittest
from django.test import Client, TestCase
import json
import codecs
import random
P1 = {
            "first_name" : "ممد",
            "last_name" : "عارف زاده",
            "phone_number" : "09905773099",
            "birth_year" : "1376",
            "gender" : "male",
            "medical_info" : "normal",
            "person_id" : "5040306938"
}

P2 = {
            "first_name" : "عارف",
            "last_name" : "عارف زاده",
            "phone_number" : "09905773099",
            "birth_year" : "1376",
            "gender" : "male",
            "medical_info" : "normal",
            "person_id" : "5040306937"
}

P3 = {
            "first_name" : "حسن",
            "last_name" : "عارف زاده",
            "phone_number" : "09905773099",
            "birth_year" : "1376",
            "gender" : "male",
            "medical_info" : "normal",
            "person_id" : "5040306936"
}

P4 = {
            "first_name" : "نقی",
            "last_name" : "عارف زاده",
            "phone_number" : "09905773099",
            "birth_year" : "1376",
            "gender" : "male",
            "medical_info" : "normal",
            "person_id" : "5040306935"
}

toycar = {
    'time': '1111111',
    'ac_x': '21452397',
    'ac_y': '1231212', 
    'ac_z': '12312312', 
    'encode1': '1295953',
    'encode2': '12312311'
}

def random_data(toydata):
    for key in toydata:
        toydata[key] = int(random.getrandbits(16))

class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tokens = {}

    def test_scenario1(self):
        self.signup(P1, 201)
        self.signup(P1, 400)
        self.signup(P2, 201)
        self.signup(P3, 201)
        self.login(P1['person_id'], 200)
        self.login(P2['person_id'], 400)
        self.login(P4['person_id'], 401)
        self.login(P1['person_id'], 200)
        self.logout('something', 400)
        self.logout(self.tokens[P1['person_id']], 200)
        self.logout(self.tokens[P1['person_id']], 400)
        self.login(P2['person_id'], 200)
        self.signup(P4, 201)
        self.logout(self.tokens[P2['person_id']], 200)
        self.logout(self.tokens[P2['person_id']], 400)
        self.login(P4['person_id'], 200)

    def test_car(self):
        pass
        """
        random_data(toycar)
        self.car_data(toycar, 403)
        random_data(toycar)
        self.car_data(toycar, 403)
        self.signup(P1, 201)
        self.login(P1['person_id'], 200)
        self.car_data(toycar, 201)
        random_data(toycar)
        self.car_data(toycar, 201)
        random_data(toycar)
        self.car_data(toycar, 201)
        random_data(toycar)
        self.car_data(toycar, 201)
        self.logout(self.tokens[P1['person_id']], 200)
        random_data(toycar)
        self.car_data(toycar, 403)
        random_data(toycar)
        self.car_data(toycar, 403)
        """

    
    def test_notloggedin(self):
        random_data(toycar)
        self.car_data(toycar, 403)
        self.start_game('notoken', 403)
        self.start_wheel('notoken', 403)
        self.start_parrot('notoken', 403)
        self.stop_parrot('notoken', 403)
        # self.new_session('notoken', 403)
    
    def test_stages(self):
        self.signup(P1, 201)
        self.signup(P2, 201)
        self.login(P1['person_id'], 200)
        self.start_wheel(self.tokens[P1['person_id']], 403)
        self.start_parrot(self.tokens[P1['person_id']], 403)
        self.stop_parrot(self.tokens[P1['person_id']], 403)
        # self.new_session(self.tokens[P1['person_id']], 403)
        random_data(toycar)
        self.car_data(toycar, 403)

        self.start_game(self.tokens[P1['person_id']], 200)

        self.start_parrot(self.tokens[P1['person_id']], 403)
        self.stop_parrot(self.tokens[P1['person_id']], 403)
        # self.new_session(self.tokens[P1['person_id']], 403)

        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)

        self.start_wheel(self.tokens[P1['person_id']], 200)

        self.stop_parrot(self.tokens[P1['person_id']], 403)
        # self.new_session(self.tokens[P1['person_id']], 403)
        self.start_game(self.tokens[P1['person_id']], 403)

        random_data(toycar)
        self.car_data(toycar, 403)
        self.start_parrot(self.tokens[P1['person_id']], 200)
        
        self.start_wheel(self.tokens[P1['person_id']], 403)
        # self.new_session(self.tokens[P1['person_id']], 403)
        self.start_game(self.tokens[P1['person_id']], 403)

        random_data(toycar)
        self.car_data(toycar, 403)

        self.stop_parrot(self.tokens[P1['person_id']], 200)

        self.start_wheel(self.tokens[P1['person_id']], 403)
        self.start_parrot(self.tokens[P1['person_id']], 403)
        self.stop_parrot(self.tokens[P1['person_id']], 403)
        self.end_session(self.tokens[P1['person_id']], 403)
        self.start_game(self.tokens[P1['person_id']], 200)

        # self.new_session(self.tokens[P1['person_id']], 200)

        # self.new_session(self.tokens[P1['person_id']], 403)
        self.start_parrot(self.tokens[P1['person_id']], 403)
        self.stop_parrot(self.tokens[P1['person_id']], 403)
        self.start_wheel(self.tokens[P1['person_id']], 200)
        self.start_parrot(self.tokens[P1['person_id']], 200)
        self.stop_parrot(self.tokens[P1['person_id']], 200)



    def test_multi_users(self):
        self.signup(P1, 201)
        self.signup(P2, 201)
        self.login(P1['person_id'], 200)
        self.start_wheel(self.tokens[P1['person_id']], 403)
        self.start_parrot(self.tokens[P1['person_id']], 403)
        self.stop_parrot(self.tokens[P1['person_id']], 403)
        # self.new_session(self.tokens[P1['person_id']], 403)
        random_data(toycar)
        self.car_data(toycar, 403)

        self.start_game(self.tokens[P1['person_id']], 200)

        self.start_parrot(self.tokens[P1['person_id']], 403)
        self.stop_parrot(self.tokens[P1['person_id']], 403)
        # self.new_session(self.tokens[P1['person_id']], 403)


        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)


        self.logout(self.tokens[P1['person_id']], 200)
        self.logout(self.tokens[P1['person_id']], 400)

        self.login(P2['person_id'], 200)

        self.start_wheel(self.tokens[P2['person_id']], 403)
        self.start_parrot(self.tokens[P2['person_id']], 403)
        self.stop_parrot(self.tokens[P2['person_id']], 403)
        # self.new_session(self.tokens[P2['person_id']], 403)
        random_data(toycar)
        self.car_data(toycar, 403)

        self.start_game(self.tokens[P2['person_id']], 200)

        self.start_parrot(self.tokens[P2['person_id']], 403)
        self.stop_parrot(self.tokens[P2['person_id']], 403)
        # self.new_session(self.tokens[P1['person_id']], 403)

        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)


        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)

        self.login(P1['person_id'], 400)

        self.logout(self.tokens[P1['person_id']], 400)
        self.logout(self.tokens[P2['person_id']], 200)

        self.login(P1['person_id'], 200)

        self.start_game(self.tokens[P1['person_id']], 200)

        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)

        self.start_wheel(self.tokens[P1['person_id']], 200)

        self.stop_parrot(self.tokens[P1['person_id']], 403)
        # self.new_session(self.tokens[P1['person_id']], 403)
        self.start_game(self.tokens[P1['person_id']], 403)

        random_data(toycar)
        self.car_data(toycar, 403)
        self.start_parrot(self.tokens[P1['person_id']], 200)
        
        self.start_wheel(self.tokens[P1['person_id']], 403)
        # self.new_session(self.tokens[P1['person_id']], 403)
        self.start_game(self.tokens[P1['person_id']], 403)

        random_data(toycar)
        self.car_data(toycar, 403)

        self.stop_parrot(self.tokens[P1['person_id']], 200)

        self.start_wheel(self.tokens[P1['person_id']], 403)
        self.start_parrot(self.tokens[P1['person_id']], 403)
        self.stop_parrot(self.tokens[P1['person_id']], 403)
        
        self.end_session(self.tokens[P1['person_id']] ,403)
        self.end_session(self.tokens[P1['person_id']] ,403)

        self.start_game(self.tokens[P1['person_id']], 200)

        # self.new_session(self.tokens[P1['person_id']], 200)

        # self.new_session(self.tokens[P1['person_id']], 403)
        self.start_parrot(self.tokens[P1['person_id']], 403)
        self.stop_parrot(self.tokens[P1['person_id']], 403)
        self.start_wheel(self.tokens[P1['person_id']], 200)
        self.start_parrot(self.tokens[P1['person_id']], 200)
        self.stop_parrot(self.tokens[P1['person_id']], 200)

        self.logout(self.tokens[P1['person_id']], 200)
        self.login(P2['person_id'], 200)
        self.start_game(self.tokens[P2['person_id']], 200)

        random_data(toycar)
        self.car_data(toycar, 201)

        random_data(toycar)
        self.car_data(toycar, 201)

        self.start_wheel(self.tokens[P2['person_id']], 200)

        self.stop_parrot(self.tokens[P2['person_id']], 403)
        # self.new_session(self.tokens[P2['person_id']], 403)
        self.start_game(self.tokens[P2['person_id']], 403)

        random_data(toycar)
        self.car_data(toycar, 403)
        self.start_parrot(self.tokens[P2['person_id']], 200)
        
        self.start_wheel(self.tokens[P2['person_id']], 403)
        # self.new_session(self.tokens[P2['person_id']], 403)
        self.start_game(self.tokens[P2['person_id']], 403)

        random_data(toycar)
        self.car_data(toycar, 403)
        self.stop_parrot(self.tokens[P2['person_id']], 200)

        self.start_wheel(self.tokens[P2['person_id']], 403)
        self.start_parrot(self.tokens[P2['person_id']], 403)
        self.stop_parrot(self.tokens[P2['person_id']], 403)
        self.end_session(self.tokens[P2['person_id']], 403)
        self.start_game(self.tokens[P2['person_id']], 200)

        # self.new_session(self.tokens[P2['person_id']], 200)

        # self.new_session(self.tokens[P2['person_id']], 403)
        self.start_parrot(self.tokens[P2['person_id']], 403)
        self.stop_parrot(self.tokens[P2['person_id']], 403)
        self.start_wheel(self.tokens[P2['person_id']], 200)
        self.start_parrot(self.tokens[P2['person_id']], 200)
        self.stop_parrot(self.tokens[P2['person_id']], 200)


    def start_game(self, token, expected_status):
        response = self.client.generic('GET', '/api/stage/game/start/', HTTP_TOKEN = token)
        if response.status_code != expected_status:
            print('start_game failed', response.content)
        self.assertEqual(response.status_code, expected_status)

    def start_wheel(self, token, expected_status):
        response = self.client.generic('GET', '/api/stage/wheel/start/', HTTP_TOKEN = token)
        self.assertEqual(response.status_code, expected_status)

    def start_parrot(self, token, expected_status):
        response = self.client.generic('GET', '/api/stage/parrot/start/', HTTP_TOKEN = token)
        self.assertEqual(response.status_code, expected_status)
    
    def stop_parrot(self, token, expected_status):
        response = self.client.generic('GET', '/api/stage/parrot/stop/', HTTP_TOKEN = token)
        self.assertEqual(response.status_code, expected_status)

    def car_data(self, data, expected_status):
        response = self.client.generic('POST', '/api/toycar', content_type='application/json', data= json.dumps(data))
        self.assertEqual(response.status_code, expected_status)


    def login(self, id, expected_status):
        response = self.client.generic('POST', '/api/auth/login', json.dumps({'person_id': id}))
        self.assertEqual(response.status_code, expected_status)
        if (expected_status == 200):
            data=json.loads(codecs.decode(response.content,'utf-8'))
            self.tokens[id] = (data['token'])

    def logout(self, token, expected_status):
        response = self.client.generic('POST', '/api/auth/logout', HTTP_TOKEN = token)
        self.assertEqual(response.status_code, expected_status)

    def signup(self, body, expected_status):
        response = self.client.post('/api/user/', body)
        if response.status_code != expected_status:
            print( response.content)
        self.assertEqual(response.status_code, expected_status)

    def end_session(self, token, expected_status):
        response = self.client.generic('GET', '/api/session/stop/', HTTP_TOKEN= token)
        self.assertEqual(response.status_code, expected_status)