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


def get_all_days_and_hours_mentions():
    mentions = []

    with open(f"{BASE_DIR}/restaurant_hours/restaurants.csv") as file:
        reader = csv.reader(file)
        file.readline()  # skip first row
        for row in reader:
            hours_field = row[1]
            mentions.extend(split_hours_field(hours_field))

    return mentions


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
