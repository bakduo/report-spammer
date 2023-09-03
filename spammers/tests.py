from django.test import TestCase
from django.utils import timezone
from .models import SpamIp, SpamMessage
import datetime


class SpamMessageTests(TestCase):

    #Con test and set
    @classmethod
    def setUpTestData(cls):

        cls.smessage = SpamMessage.objects.create(message='mensaje de test',
                domain='www.google.com',
                email='sample@gmail.com',
                description='testing description',
                time=datetime.date(2023, 8, 26))
        
        cls.smip = SpamIp(email_id=cls.smessage.id,ip='4.4.4.4')
    
    def test_spammessage_content(self):
        self.assertEqual(self.smessage.message,'mensaje de test')
        self.assertEqual(self.smessage.domain,'www.google.com')
        self.assertEqual(self.smessage.email,'sample@gmail.com')
        self.assertEqual(self.smessage.description,'testing description')
        self.assertEqual(self.smessage.time,datetime.date(2023, 8, 26))
        self.assertEqual(self.smip.email_id,self.smessage.id)
        self.assertEqual(self.smip.ip,'4.4.4.4')
    
    #Clasico
    # def test_spam_message(self):
    #     smessage = SpamMessage.objects.create(message='mensaje de test',
    #             domain='www.google.com',
    #             email='sample@gmail.com',
    #             description='testing description',
    #             time=datetime.date(2023, 8, 26))
        
    #     smip = SpamIp(email_id=smessage.id,ip='4.4.4.4')

    #     self.assertEqual(smessage.message,'mensaje de test')
    #     self.assertEqual(smessage.domain,'www.google.com')
    #     self.assertEqual(smessage.email,'sample@gmail.com')
    #     self.assertEqual(smessage.description,'testing description')
    #     self.assertEqual(smessage.time,datetime.date(2023, 8, 26))

    #     self.assertEqual(smip.email_id,smessage.id)
    #     self.assertEqual(smip.ip,'4.4.4.4')