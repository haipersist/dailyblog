# Create your tests here.
from django.test import TestCase
from models import UserProfile
from django.contrib.auth.models import User

# Create your tests here.


class UserProfileTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.get(username='hbnnlong')
        UserProfile.objects.create(age=28,
                                   user=self.user,
                                   birthday='1989-03-25')

    def test_userprofile_creation(self):
        self.assertTrue(UserProfile.exist_user_profile(self.user))


