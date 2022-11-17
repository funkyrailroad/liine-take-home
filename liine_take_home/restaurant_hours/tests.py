# Create your tests here.
from pprint import pprint

from django.test import TestCase

import restaurant_hours.util as u


class DataCleaningTests(TestCase):
    def check_split_opening_days_and_hours(
        self, days_and_hours_mention, days_gt, hours_gt
    ):
        days_mention, hours_mention = u.split_days_and_hours_mention(
            days_and_hours_mention
        )
        self.assertEqual(days_mention, days_gt)
        self.assertEqual(hours_mention, hours_gt)

    def test_split_opening_days_and_hours(self):
        self.check_split_opening_days_and_hours(
            "Sun 12 pm - 10 pm",
            "Sun",
            "12 pm - 10 pm",
        )

        self.check_split_opening_days_and_hours(
            "Sat-Sun 5 pm - 10 pm",
            "Sat-Sun",
            "5 pm - 10 pm",
        )

        self.check_split_opening_days_and_hours(
            "Mon-Thu, Sun 11:30 am - 10 pm",
            "Mon-Thu, Sun",
            "11:30 am - 10 pm",
        )
