from django.test import TestCase

# Create your tests here.

from datetime import date
from models import Trip

class TripTestCase(TestCase):

    def setUp(self):

        Trip.objects.create(title='testtrip1',
                            abstract='testtrip1',
                            article_url='testtrip1',
                            trip_date=date.today())

        self.latest = Trip.objects.create(title='testtrip2',
                            abstract='testtrip2',
                            article_url='testtrip2',
                            trip_date=date.today())


    def test_trip_latest(self):
        self.assertEqual(self.latest,Trip.latest())


