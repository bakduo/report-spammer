from django.test import TestCase

# Create your tests here.

from django.urls import reverse

from rest_framework import status

from rest_framework.test import APITestCase

import datetime

from spammers.models import SpamMessage,SpamIp

class APITests(APITestCase):

    @classmethod
    def setUpTestData(cls):
         cls.smessage = SpamMessage.objects.create(message='mensaje de test',
                domain='www.google.com',
                email='sample@gmail.com',
                description='testing description',
                time=datetime.date(2023, 8, 26))
         
         cls.smip = SpamIp(email_id=cls.smessage.id,ip='4.4.4.4')
         
    def test_api_listspam(self):
         response = self.client.get(reverse('spammessage_list'))
         self.assertEqual(response.status_code,status.HTTP_200_OK)
         self.assertEqual(SpamMessage.objects.count(),1)
         self.assertEqual(self.smip.email,self.smessage)
         self.assertContains(response,self.smessage)

    def test_api_detailspam(self):
         response = self.client.get(reverse('spammessage_detail',kwargs={"pk":self.smessage.id}),format="json")
         self.assertEqual(response.status_code,status.HTTP_200_OK)
         self.assertEqual(SpamMessage.objects.count(),1)
         self.assertContains(response,"google")