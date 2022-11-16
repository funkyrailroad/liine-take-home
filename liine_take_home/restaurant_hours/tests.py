# Create your tests here.
from django.conf import settings
from django.test import TestCase

import restaurant_hours.util as u

class DataCleaningTests(TestCase):

    # def test_1(self):
    #     import csv
    #     BASE_DIR = settings.BASE_DIR

    #     with open(f"{BASE_DIR}/restaurant_hours/restaurants.csv") as file:
    #         reader = csv.reader(file)
    #         for row in reader:
    #             print(", ".join(row))


    def test_normalize_hours_mention(self):
        mention = "Sat-Sun 5 pm - 10 pm"
        mentions = u.get_all_hours_mentions()
        print(mentions)
