from django.test import TestCase

# Create your tests here.

from django.contrib.auth import get_user_model
#from django.urls import reverse, resolve
#from .views import SignupPageView
#from .forms import CustomUserCreationForm
from .models import CustomUser

class CustomUserTests(TestCase):

    
    def test_create_user_custom(self):
        user = CustomUser(
            username='sample1',
            email='sample1@domain.com',
            password='linux2023'
        )
        self.assertEqual(user.username,'sample1')
        self.assertEqual(user.email,'sample1@domain.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='sampleadmin',
            email='sampleadmin@domain.com',
            password='linux2023'
        )
        self.assertEqual(user.username,'sampleadmin')
        self.assertEqual(user.email,'sampleadmin@domain.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


# class SignupPageTests(TestCase):
#     def setUp(self):
#         url = reverse('signup')
#         self.response = self.client.get(url)

#     def test_signup_template(self):
#         self.assertEqual(self.response.status_code, 200)
#         self.assertTemplateUsed(self.response,'registration/signup.html')
#         self.assertContains(self.response,'Sign Up')
#         self.assertNotContains(self.response,'Esto no deberia existir')

#     def test_signup_form(self):
#         form = self.response.context.get('form')
#         self.assertIsInstance(form,CustomUserCreationForm)
#         self.assertContains(self.response,'csrfmiddlewaretoken')

#     def test_signup_view(self):
#         view = resolve('/auth-legacy/signup/')
#         self.assertEqual(
#             view.func.__name__,
#             SignupPageView.as_view().__name__
#         )
