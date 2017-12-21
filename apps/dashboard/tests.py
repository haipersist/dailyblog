from django.test import TestCase,Client



# Create your tests here.


class DashboardCaseTest(TestCase):
   
    def setUp(self):
	self.client = Client()

    def test_401_permission(self):
	r = self.client.get('/dashboard')
	self.assertEqual(r.status_code,401)


