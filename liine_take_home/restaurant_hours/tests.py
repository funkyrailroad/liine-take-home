# Create your tests here.
from datetime import time
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

    def test_get_opening_hours_from_hours_mention(self):

        [
            "11 am - 10 pm",
            "11 am - 10:30 pm",
            "10 am - 9:30 pm",
            "9:30 am - 9:30 pm",
            "11 am - 12 am",
            "12 pm - 2 am",
            "11 am - 9 pm",
            "5 pm - 9 pm",
            "11:30 am - 10 pm",
            "5:30 pm - 10 pm",
            "11 am - 10 pm",
            "11 am - 11 pm",
            "11 am - 10 pm",
            "5 pm - 10 pm",
        ]

        self.assertEqual(
            u.get_opening_hours_from_hours_mention("11 am - 10 pm"),
            [time(11), time(22)],
        )

        self.assertEqual(
            u.get_opening_hours_from_hours_mention("10 am - 10 pm"),
            [time(10), time(22)],
        )

        self.assertEqual(
            u.get_opening_hours_from_hours_mention("12 am - 12 pm"),
            [time(0), time(12)],
        )

        self.assertEqual(
            u.get_opening_hours_from_hours_mention("12:30 am - 12:30 pm"),
            [time(0, 30), time(12, 30)],
        )

        self.assertEqual(
            u.get_opening_hours_from_hours_mention("12:30 pm - 12:30 am"),
            [time(12, 30), time(0, 30)],
        )

    def test_convert_time_string_to_time_obj(self):
        self.assertEqual(u.convert_time_string_to_time_obj("5 pm"), time(17))
        self.assertEqual(u.convert_time_string_to_time_obj("5:30 pm"), time(17, 30))
        self.assertEqual(u.convert_time_string_to_time_obj("1 am"), time(1))
        self.assertEqual(u.convert_time_string_to_time_obj("1:30 am"), time(1, 30))
        self.assertEqual(u.convert_time_string_to_time_obj("12 am"), time(0))
        self.assertEqual(u.convert_time_string_to_time_obj("12 pm"), time(12))
        self.assertEqual(u.convert_time_string_to_time_obj("12:30 pm"), time(12, 30))
        self.assertEqual(u.convert_time_string_to_time_obj("12:30 am"), time(0, 30))

    def test_get_opening_hours_from_days_and_hours_field(self):
        "Sun 3 pm - 11:30 pm"
        "Mon-Fri 11 am - 10 pm  / Sat-Sun 5 pm - 10 pm"
        "Mon-Sat 11 am - 10 pm  / Sun 12 pm - 10 pm"

        self.assertEqual(
            u.get_opening_hours_from_days_and_hours_field("Sun 3 pm - 11:30 pm"),
            [("Sun", time(15), time(23, 30))],
        )

        self.assertEqual(
            u.get_opening_hours_from_days_and_hours_field(
                "Mon-Fri 11 am - 10 pm  / Sat-Sun 5 pm - 10 pm"
            ),
            [
                ("Mon", time(11), time(22)),
                ("Tues", time(11), time(22)),
                ("Wed", time(11), time(22)),
                ("Thu", time(11), time(22)),
                ("Fri", time(11), time(22)),
                ("Sat", time(17), time(22)),
                ("Sun", time(17), time(22)),
            ],
        )

    def test_get_opening_hours_from_days_and_hours_mention(self):
        "Sun 3 pm - 11:30 pm"
        "Mon-Fri 11 am - 10 pm  / Sat-Sun 5 pm - 10 pm"
        "Mon-Sat 11 am - 10 pm  / Sun 12 pm - 10 pm"

        self.assertEqual(
            u.get_opening_hours_from_days_and_hours_mention("Fri-Sun 3 pm - 11:30 pm"),
            [
                ("Fri", time(15), time(23, 30)),
                ("Sat", time(15), time(23, 30)),
                ("Sun", time(15), time(23, 30)),
            ],
        )

        self.assertEqual(
            u.get_opening_hours_from_days_and_hours_mention("Sun 3 pm - 11:30 pm"),
            [("Sun", time(15), time(23, 30))],
        )


class DataLoadingTests(TestCase):
    def test_days_and_hours_mention_to_weekly_table_format(self):
        self.assertEqual(
            u.days_and_hours_mention_to_weekly_table_format("Sun 3 pm - 11:30 pm"),
            [dict(day="Sun", open_time=time(15), close_time=time(23, 30))],
        )

        self.assertEqual(
            u.days_and_hours_mention_to_weekly_table_format("Thu-Fri, Sun 3 pm - 12:30 am"),
            [
                dict(day="Thu", open_time=time(15), close_time=time.max),
                dict(day="Fri", open_time=time.min, close_time=time(0, 30)),
                dict(day="Fri", open_time=time(15), close_time=time.max),
                dict(day="Sat", open_time=time.min, close_time=time(0, 30)),
                dict(day="Sun", open_time=time(15), close_time=time.max),
                dict(day="Mon", open_time=time.min, close_time=time(0, 30)),
            ],
        )

    def test_get_next_day(self):
        self.assertEqual(u.get_next_day("Mon"), "Tues")
        self.assertEqual(u.get_next_day("Tues"), "Wed")
        self.assertEqual(u.get_next_day("Wed"), "Thu")
        self.assertEqual(u.get_next_day("Thu"), "Fri")
        self.assertEqual(u.get_next_day("Fri"), "Sat")
        self.assertEqual(u.get_next_day("Sat"), "Sun")
        self.assertEqual(u.get_next_day("Sun"), "Mon")
