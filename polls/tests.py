from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status

from polls.models import Poll


class PollsTests(TestCase):
    def test_create_poll(self):
        url = '/polls/'
        c = Client()
        response = c.post(url, {
            'name': 'Test',
            'description': 'test_description',
            'end_date': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = c.post(url, {
            'name': 'Test',
            'description': 'test_description',
            'start_date': timezone.now() - timezone.timedelta(seconds=1),
            'end_date': timezone.now() + timezone.timedelta(days=2)
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = c.post(url, {
            'name': 'Test',
            'description': 'test_description',
            'start_date': timezone.now() + timezone.timedelta(seconds=1),
            'end_date': timezone.now() + timezone.timedelta(seconds=1)
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = c.post(url, {
            'name': 'Test',
            'description': 'test_description',
            'start_date': timezone.now() + timezone.timedelta(days=1),
            'end_date': timezone.now() + timezone.timedelta(days=2)
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # self.assertEqual(user.username, 'Jenya')
        # self.assertEqual(user.email, 'normal@user.com')
        # self.assertFalse(user.is_active)
        # self.assertFalse(user.is_superuser)
        #
        # with self.assertRaises(TypeError):
        #     User.objects.create_user()
        # with self.assertRaises(TypeError):
        #     User.objects.create_user(username='')
        # with self.assertRaises(TypeError):
        #     User.objects.create_user(email='')
        # with self.assertRaises(ValueError):
        #     User.objects.create_user(username='', email='', password="foo")
