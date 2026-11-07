from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from restaurant.models import Booking, Menu


class MenuModelTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(
            name='IceCream',
            price=80,
            menu_item_description='Vanilla ice cream',
        )
        self.assertEqual(item.get_item(), 'IceCream : 80')
        self.assertEqual(str(item), 'IceCream')


class BookingModelTest(TestCase):
    def test_str(self):
        booking = Booking.objects.create(
            first_name='Ada',
            reservation_date='2026-11-08',
            reservation_slot=18,
        )
        self.assertEqual(str(booking), 'Ada')


class StaticPagesTest(TestCase):
    def test_home_page_is_served_by_django(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Little Lemon')


class MenuAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item = Menu.objects.create(
            name='Greek Salad',
            price=12,
            menu_item_description='Fresh salad',
        )

    def test_list_menu(self):
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Greek Salad')

    def test_create_update_and_delete_menu_item(self):
        created = self.client.post(
            '/api/menu/',
            {
                'name': 'Bruschetta',
                'price': 8,
                'menu_item_description': 'Grilled bread',
            },
            format='json',
        )
        self.assertEqual(created.status_code, 201)
        item_id = created.data['id']

        updated = self.client.put(
            f'/api/menu/{item_id}/',
            {
                'name': 'Bruschetta',
                'price': 9,
                'menu_item_description': 'Grilled bread with tomato',
            },
            format='json',
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.data['price'], 9)

        deleted = self.client.delete(f'/api/menu/{item_id}/')
        self.assertEqual(deleted.status_code, 204)
        self.assertFalse(Menu.objects.filter(pk=item_id).exists())


class AuthAndBookingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration_returns_token(self):
        response = self.client.post(
            '/api/registration/',
            {
                'username': 'guest',
                'password': 'LittleLemon#2026',
                'email': 'guest@littlelemon.com',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('auth_token', response.data)
        self.assertTrue(User.objects.filter(username='guest').exists())

    def test_login_returns_token(self):
        User.objects.create_user(username='ada', password='LittleLemon#2026')
        response = self.client.post(
            '/api/token/login/',
            {'username': 'ada', 'password': 'LittleLemon#2026'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.data)

    def test_booking_requires_token_and_supports_crud(self):
        locked = self.client.get('/api/bookings/')
        self.assertEqual(locked.status_code, 401)

        user = User.objects.create_user(username='ada', password='LittleLemon#2026')
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        created = self.client.post(
            '/api/bookings/',
            {
                'first_name': 'Ada',
                'reservation_date': '2026-11-08',
                'reservation_slot': 18,
            },
            format='json',
        )
        self.assertEqual(created.status_code, 201)
        booking_id = created.data['id']

        listed = self.client.get('/api/bookings/')
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(len(listed.data), 1)

        updated = self.client.put(
            f'/api/bookings/{booking_id}/',
            {
                'first_name': 'Ada Lovelace',
                'reservation_date': '2026-11-09',
                'reservation_slot': 19,
            },
            format='json',
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.data['reservation_slot'], 19)

        deleted = self.client.delete(f'/api/bookings/{booking_id}/')
        self.assertEqual(deleted.status_code, 204)
        self.assertFalse(Booking.objects.filter(pk=booking_id).exists())
