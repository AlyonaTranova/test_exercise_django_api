from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from .models import Flat, RentOrder, Build


class CommonTestCase(TestCase):
	def test_registration(self):
		self.user = get_user_model().objects.create_user(
			email='babalaev@gmail.com',
			username="balal",
			password1='password',
			password2='password',
			first_name='Igor',
			last_name='Balalaev',
			birthday='1990-01-01',
			phone='9099581234',
			age='31',
			language='en',
			status='owner'
		)
		self.user.save()

	def test_correct(self):
		user = authenticate(email='babalaev@gmail.com', password='password')
		self.assertTrue((user is not None) and user.is_authenticated)

	def test_building(self):
		self.build = Build.objects.create(
			name="residential buildings 'Romashka'",
			address="Moscow, Sovetskaya st.,5",
			description="description",
		)
		self.build.save()

	def test_flat_create(self):
		self.flat = Flat.objects.create(
			building="residential buildings 'Romashka'",
			price="100000",
			owner="babalaev@gmail.com",
			room_count='3',
			type='apartment'
		)
		self.flat.save()

	def test_order_create(self):
		self.order = RentOrder.objects.create(
			date_from='2021-07-01',
			date_to='2021-07-30',
			total_price='10000',
			renter='babalaev@gmail.com',
			flat_id_for='1'
		)

	def test_index(self):
		urls = [
			'/api/v1/register',
			'/api/v1/users',
			'/api/v1/users/1',
			'/api/v1/flats',
			'/api/v1/flats/1',
			'/api/v1/order',
			'flats/1/rooms/1'
		]
		for points in urls:
			response = self.client.get(points)
			self.assertEqual(response.status_code, 200)

	def test_flat(self):
		response = self.client.get('/flats/1/')
		self.assertEqual(response.data, {
			'id': '1',
			'building': "residential buildings 'Romashka'",
			'price': "100000",
			'owner': "babalaev@gmail.com",
			'room_count': '3',
			'type': 'apartment',
		})

	def test_order(self):
		response = self.client.get('/order/1/')
		self.assertEqual(response.data, {
			'date_from': '2021-07-01',
			'date_to': '2021-07-30',
			'total_price': '10000',
			'renter': 'babalaev@gmail.com',
			'flat_id_for': '1'
		})