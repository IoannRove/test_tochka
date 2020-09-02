import json
from pprint import pprint

import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Account


class AccountTests(APITestCase):
    def setUp(self):
        self.test_account = Account.objects.create(
            fio='Test Test Test', balance=500, hold=200, status=True
        )

    def test_get_account_status(self):
        url = reverse('status', kwargs={'pk': self.test_account.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'balance': 500, 'status': True})

    def test_add_account_balance(self):
        url = reverse('add', kwargs={'pk': self.test_account.uuid})
        data = {'balance': 500}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'balance': 1000})
        self.assertEqual(Account.objects.get().balance, 1000)

    def test_add_possible_account_hold(self):
        url = reverse('subtract', kwargs={'pk': self.test_account.uuid})
        data = {'hold': 100}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'hold': 300})
        self.assertEqual(Account.objects.get().hold, 300)

    def test_add_impossible_account_hold(self):
        url = reverse('subtract', kwargs={'pk': self.test_account.uuid})
        data = {'hold': 500}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('errors', {}).get('code'), 'hold_over_balance')
        self.assertEqual(Account.objects.get().hold, 200)

    def tearDown(self):
        self.test_account.delete()
