import csv

import restaurant_hours.models as m
import restaurant_hours.util as u
from django.core.management.base import BaseCommand
from liine_take_home.settings import BASE_DIR


class Command(BaseCommand):
    help = "Import the data to "

    def handle(self, *args, **kwargs):
        weekly_table_format_dicts = []
        with open(f"{BASE_DIR}/restaurant_hours/restaurants.csv") as file:
            reader = csv.reader(file)
            file.readline()  # skip first row
            for row in reader:
                weekly_table_format_dicts.extend(u.csv_row_to_weekly_table_format(row))

        for data_dict in weekly_table_format_dicts:
            inst = m.WeeklyOpeningHours.objects.create(**data_dict)
            inst.save()
