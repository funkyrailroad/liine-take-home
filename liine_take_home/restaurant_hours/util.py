import csv
import re

from django.conf import settings

BASE_DIR = settings.BASE_DIR


def clean_csv():
    pass


def clean_row():
    pass


def clean_hours_field():
    pass


def split_hours_field(hours_field):
    """Split and remove whitespace in hours field"""
    return [mention.strip() for mention in hours_field.split("/")]


def normalize_hours_mention():
    pass


def split_days_and_hours_mention(mention):
    """Opening days are the first part of the string and can potentially be:

    - a single day
    - multiple consecutive days
    - multiple non-consecutive days
    - or any combination thereof

    A reliable split seems to be the first number in the string
    """
    split_index = re.search(r"\d", mention).start()
    days, hours = mention[:split_index], mention[split_index:]
    return days.strip(), hours.strip()


def get_all_days_mentions():
    days_mentions = []
    days_and_hours_mentions = get_all_days_and_hours_mentions()
    for days_and_hours_mention in days_and_hours_mentions:
        days_mention, _ = split_days_and_hours_mention(days_and_hours_mention)
        days_mentions.append(days_mention)
    return days_mentions


def get_all_hours_mentions():
    hours_mentions = []
    days_and_hours_mentions = get_all_days_and_hours_mentions()
    for days_and_hours_mention in days_and_hours_mentions:
        _, hours_mention = split_days_and_hours_mention(days_and_hours_mention)
        hours_mentions.append(hours_mention)
    return hours_mentions


def get_all_days_and_hours_mentions():
    days_and_hours_mentions = []
    days_and_hours_fields = get_all_days_and_hours_fields()
    for days_and_hours_field in days_and_hours_fields:
        days_and_hours_mentions.extend(split_hours_field(days_and_hours_field))
    return days_and_hours_mentions


def get_all_days_and_hours_fields():
    days_and_hours_fields = []
    with open(f"{BASE_DIR}/restaurant_hours/restaurants.csv") as file:
        reader = csv.reader(file)
        file.readline()  # skip first row
        for row in reader:
            days_and_hours_field = row[1]
            days_and_hours_fields.append(days_and_hours_field)
    return days_and_hours_fields


def split_days_mention(days_mention):
    return [day_mention.strip() for day_mention in days_mention.split(",")]


def get_opening_days_from_days_mention(days_mention):
    """day_mention is a split days_mention"""
    opening_days = []
    day_or_ranges = split_days_mention(days_mention)

    for day_or_range in day_or_ranges:
        if is_single_day(day_or_range):
            opening_days.append(day_or_range)
            continue
        days = get_opening_days_from_day_range(day_or_range)
        opening_days.extend(days)
    return opening_days


days_of_the_week = [
    "Mon",
    "Tues",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun",
]


def is_single_day(day_mention):
    if day_mention in days_of_the_week:
        return True
    return False


def get_opening_days_from_day_range(day_range):
    day1, day2 = day_range.split("-")
    ind1 = days_of_the_week.index(day1)
    ind2 = days_of_the_week.index(day2)
    return days_of_the_week[ind1 : ind2 + 1]
