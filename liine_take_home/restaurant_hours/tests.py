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

    def test_helper_functions(self):
        days_and_hours_fields = u.get_all_days_and_hours_fields()
        self.assertIsInstance(days_and_hours_fields, list)

        days_and_hours_mentions = u.get_all_days_and_hours_mentions()
        self.assertIsInstance(days_and_hours_mentions, list)

        days_mentions = u.get_all_days_mentions()
        self.assertIsInstance(days_mentions, list)

        hours_mentions = u.get_all_hours_mentions()
        self.assertIsInstance(hours_mentions, list)

    def check_split_days_mention(self, days_mention, split_days_mention_gt):
        split_days_mention = u.split_days_mention(days_mention)
        self.assertEqual(set(split_days_mention), set(split_days_mention_gt))

    def test_split_days_mention(self):
        self.check_split_days_mention("Sat", ["Sat"])

        self.check_split_days_mention("Mon-Thu, Sun", ["Mon-Thu", "Sun"])

        self.check_split_days_mention("Fri-Sat", ["Fri-Sat"])

        self.check_split_days_mention("Mon-Fri, Sat", ["Mon-Fri", "Sat"])

    def check_get_opening_days_from_days_mention(self, days_mention, opening_days_gt):
        opening_days = u.get_opening_days_from_days_mention(days_mention)
        self.assertEqual(set(opening_days), set(opening_days_gt))

    def test_get_opening_days_from_days_mention(self):
        self.check_get_opening_days_from_days_mention("Sat", ["Sat"])

        self.check_get_opening_days_from_days_mention(
            "Mon-Thu, Sun", ["Mon", "Tues", "Wed", "Thu", "Sun"]
        )

        self.check_get_opening_days_from_days_mention("Fri-Sat", ["Fri", "Sat"])

        self.check_get_opening_days_from_days_mention(
            "Mon-Fri, Sat", ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat"]
        )

    def test_is_single_day(self):
        self.assertTrue(u.is_single_day("Sat"))
        self.assertTrue(u.is_single_day("Mon"))
        self.assertFalse(u.is_single_day("Mon-Tues"))
        self.assertFalse(u.is_single_day("Mon-Fri"))

    def test_get_opening_days_from_day_range(self):
        self.assertEqual(
            set(u.get_opening_days_from_day_range("Mon-Fri")),
            set(["Mon", "Tues", "Wed", "Thu", "Fri"]),
        )
        self.assertEqual(
            set(u.get_opening_days_from_day_range("Mon-Thu")),
            set(["Mon", "Tues", "Wed", "Thu"]),
        )
        self.assertEqual(
            set(u.get_opening_days_from_day_range("Mon-Sun")),
            set(["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]),
        )
        self.assertEqual(
            set(u.get_opening_days_from_day_range("Mon-Tues")),
            set(["Mon", "Tues"]),
        )
        self.assertEqual(
            set(u.get_opening_days_from_day_range("Tues-Sun")),
            set(["Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]),
        )

    # def get_opening_days_from_day_range(self):
