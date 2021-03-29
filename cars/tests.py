import pdb
import json
import unittest

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Car, Service
from .facades.db_facades import CarFacade, ServiceFacade
#from users.forms import CustomUserCreationForm

class CarsViewApiTest(TestCase):

    def add_user_and_few_cars_to_db(self):

        client = APIClient()
        client.post('/cars/add_car_api', {"brand": "Fiat_1", "model": "Panda_1", "year": "2001"}, format='json')
        client.post('/cars/add_car_api', {"brand": "Fiat_2", "model": "Panda_2", "year": "2002"}, format='json')
        client.post('/cars/add_car_api', {"brand": "Fiat_3", "model": "Panda_3", "year": "2003"}, format='json')
        client.post('/cars/add_car_api', {"brand": "Fiat_4", "model": "Panda_4", "year": "2004"}, format='json')

    def test_add_car_api(self):
        self.add_user_and_few_cars_to_db()

        car = {
            "brand": "bbbb", 
            "model": "mmmm"
        }

        client = APIClient()
        #client.login(username="gabriel", password="a")
        response = client.post('/cars/add_car_api', car, format='json')
        client.logout()        

        self.assertEqual(201, response.status_code)
        self.assertTrue("car_id" in json.loads(response.content))

        car_id = json.loads(response.content)["car_id"]

        # raises exception if car does not exist in db
        Car.objects.get(id=car_id)
        
    
    def test_get_user_cars_api(self):
        self.add_user_and_few_cars_to_db()

        client = APIClient()
        #client.login(username="gabriel", password="a")
        response = client.get('/cars/get_user_cars_api', format='json')

        response_data = json.loads(response.content)

        #pdb.set_trace()
        self.assertEqual(200, response.status_code)
        self.assertEqual(4, len(response_data))
        self.assertTrue('brand' in response_data[0])
        self.assertTrue('model' in response_data[1])
        self.assertTrue('year' in response_data[2])
        self.assertTrue('vin' in response_data[3])

    @unittest.skip("not ready")
    def test_edit_car_api(self):
        self.add_user_and_few_cars_to_db()

        car_db = Car.objects.first()

        #car_to_change.brand = "new brand"
        #car_to_change.model = "new model"

        car_changed = {
            "brand": "new brand",
            "model": "new model",
            "car_id": car_db.id
        }

        client = APIClient()
        #client.login(username="gabriel", password="a")
        response = client.post('/cars/edit_car_api', car_changed, format='json')

        car_db_after = Car.objects.get(id=car_db.id)

        self.assertEqual(200, response.status_code)
        self.assertEqual("new brand", car_db_after.brand)
        self.assertEqual("new model", car_db_after.model)
        self.assertEqual(car_db.year, car_db_after.year)
        self.assertEqual(car_db.vin, car_db_after.vin)


    @unittest.skip("not ready")
    def test_edit_car_api_no_car(self):
        self.add_user_and_few_cars_to_db()

        car_db = Car.objects.last()

        car_changed = {
            "brand": "new brand",
            "model": "new model",
            "car_id": car_db.id+100
        }

        client = APIClient()
        #client.login(username="gabriel", password="a")
        response = client.post('/cars/edit_car_api', car_changed, format='json')

        self.assertEqual(400, response.status_code)


    @unittest.skip("not ready")
    def test_delete_car_api(self):
        self.add_user_and_few_cars_to_db()

        car_db = Car.objects.last()

        client = APIClient()
        #client.login(username="gabriel", password="a")
        response = client.delete('/cars/delete_car_api/{}'.format(car_db.id), format='json')

        self.assertEqual(200, response.status_code)

        with self.assertRaises(Car.DoesNotExist):
            del_car = Car.objects.get(id=car_db.id)


    @unittest.skip("not ready")    
    def test_delete_car_api__car_not_exist(self):
        self.add_user_and_few_cars_to_db()

        car_db = Car.objects.last()

        client = APIClient()
        #client.login(username="gabriel", password="a")
        response = client.delete('/cars/delete_car_api/{}'.format(car_db.id+100), format='json')

        self.assertEqual(404, response.status_code)
