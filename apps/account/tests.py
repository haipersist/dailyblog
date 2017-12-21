# Create your tests here.
from django.test import TestCase,Client
from models import UserProfile
from django.contrib.auth.models import User
import selenium

# Create your tests here.


class UserProfileTestCase(TestCase):

    def setUp(self):
        User.objects.create(username='test',password='test')
        self.user = User.objects.get(username='test')
        UserProfile.objects.create(age=28,
                                   user=self.user,
                                   birthday='1989-03-25')

    def test_userprofile_creation(self):
        self.assertTrue(UserProfile.exist_user_profile(self.user))



class UserViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login(self):
       r = self.client.post('/account/login/',{'username':'hbnnlong','password':'NANAnana320'})
       self.assertEqual(r.status_code,200)
       self.assertEqual(1,2)

    def test_logout(self):
       r = self.client.post('/account/logout')
       self.assertEqual(r.status_code,401)

    def test_users_by_selenium(self):
	self.driver = selenium.webdriver.Firefox()
	self.driver.get('/api/users')
	self.assertIn('REST',driver.title)

    def tearDown(self):
	self.driver.close()

