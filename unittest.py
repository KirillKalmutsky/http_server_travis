import unittest
import random
import requests
import json


class TestServerMethods(unittest.TestCase):

    url = 'http://localhost:65432'
    key = random.randint(0, 100)
    value_1 = random.randint(0, 100)
    value_2 = ''.join([chr(random.randint(1, 110000)) for i in range(random.randint(1, 10))])

    def test_wrong_json(self):
        not_json_data = {'key' : self.key,
                         'value' : self.value_1}
        
        response = requests.post(self.url + '/post', data=not_json_data)
        self.assertEqual(response.status_code, 400)

    def test_post(self):
        json_data = {'key': self.key, 
                     'value': self.value_1}
        json_data = json.dumps(json_data)

        response = requests.post(self.url + '/post', data=json_data)
        self.assertEqual(response.status_code, 200)

        response = requests.post(self.url + '/post', data=json_data)
        self.assertEqual(response.status_code, 208)

    def test_get_and_to_cache(self):
        json_data = {'key' : self.key, 'no-cache' : False}
        json_data = json.dumps(json_data)
        
        response = requests.get(self.url + '/get', data=json_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['value'], self.value_1)

    def test_get_not_exist(self):
        json_data = {'key': random.randint(-100, -10), 'no-cache' : False}
        json_data = json.dumps(json_data)
        
        response = requests.get(self.url + '/get', data=json_data)

        self.assertEqual(response.status_code, 404)

    def test_put(self):
        json_data = {'key': self.key,
                     'value': self.value_2}
        json_data = json.dumps(json_data)

        response = requests.put(self.url + '/put', data=json_data)

        self.assertEqual(response.status_code, 200)

    def test_get_from_cache(self):
        json_data = {'key': self.key, 'no-cache': False}
        json_data = json.dumps(json_data)
        
        response = requests.get(self.url + '/get', data=json_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['value'], self.value_1)

    def test_get_from_base_no_change(self):
        json_data = {'key': self.key, 'no-cache': True}
        json_data = json.dumps(json_data)
        
        response = requests.get(self.url + '/get', data=json_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['value'], self.value_2)

        json_data = {'key': self.key, 'no-cache': False}
        json_data = json.dumps(json_data)

        response = requests.get(self.url + '/get', data=json_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['value'], self.value_1)

    def test_del_idempotent(self):
        json_data = {'key' : self.key}
        json_data = json.dumps(json_data)
        
        response = requests.delete(self.utl + '/delete',
                                   data=json_data)

        self.assertEqual(response.status_code, 205)

        response = requests.delete(self.utl + '/delete',
                                   data={'key': self.key})

        self.assertEqual(response.status_code, 205)

    def test_del_no_exist(self):
        json_data = {'key': self.key, 'no-cache': False}
        json_data = json.dumps(json_data)
        
        response = requests.get(self.url + '/get', data=json_data)

        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()