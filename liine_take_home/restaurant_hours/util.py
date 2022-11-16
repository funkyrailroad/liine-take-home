import csv

from django.conf import settings

BASE_DIR = settings.BASE_DIR


def clean_csv():
    pass


def clean_row():
    pass


def clean_hours_field():
    pass


def split_hours_field():
    pass


def normalize_hours_mention():
    pass


def get_all_hours_mentions():
    mentions = []

    with open(f"{BASE_DIR}/restaurant_hours/restaurants.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row[1])

    return mentions
