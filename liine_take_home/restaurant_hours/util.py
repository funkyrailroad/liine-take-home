import csv
import re
from datetime import time

from django.conf import settings

BASE_DIR = settings.BASE_DIR


def clean_csv():
    pass


def clean_row():
    pass


def clean_hours_field():
    pass


def normalize_hours_mention():
    pass


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
        days_and_hours_mentions.extend(split_days_and_hours_field(days_and_hours_field))
    return days_and_hours_mentions


def get_opening_hours_from_days_and_hours_field(field):
    opening_hours = []
    days_and_hours_mentions = split_days_and_hours_field(field)
    for days_and_hours_mention in days_and_hours_mentions:
        opening_hours.extend(
            get_opening_hours_from_days_and_hours_mention(days_and_hours_mention)
        )
    return opening_hours


def get_opening_hours_from_days_and_hours_mention(days_and_hours_mention):
    days_mention, hours_mention = split_days_and_hours_mention(days_and_hours_mention)
    days = get_days_from_days_mention(days_mention)
    start, end = get_opening_hours_from_hours_mention(hours_mention)
    return [(day, start, end) for day in days]


def get_days_from_days_mention(days_mention):
    days = []
    days_or_day_ranges = split_days_mention(days_mention)
    for day_or_day_range in days_or_day_ranges:
        days.extend(get_opening_days_from_day_or_range(day_or_day_range))
    return days


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


def split_days_and_hours_field(days_and_hours_field):
    """Split and remove whitespace in hours field"""
    return [mention.strip() for mention in days_and_hours_field.split("/")]


def get_all_days_and_hours_fields():
    days_and_hours_fields = []
    with open(f"{BASE_DIR}/restaurant_hours/restaurants.csv") as file:
        reader = csv.reader(file)
        file.readline()  # skip first row
        for row in reader:
            days_and_hours_field = row[1]
            days_and_hours_fields.append(days_and_hours_field)
    return days_and_hours_fields


def get_opening_days_from_days_mention(days_mention):
    """day_mention is a split days_mention"""
    opening_days = []
    day_or_ranges = split_days_mention(days_mention)
    for day_or_range in day_or_ranges:
        days = get_opening_days_from_day_or_range(day_or_range)
        opening_days.extend(days)
    return opening_days


def get_opening_days_from_day_or_range(day_or_range):
    if is_single_day(day_or_range):
        return [day_or_range]
    return get_opening_days_from_day_range(day_or_range)


def is_single_day(day_mention):
    if day_mention in days_of_the_week:
        return True
    return False


def get_opening_days_from_day_range(day_range):
    day1, day2 = day_range.split("-")
    ind1 = days_of_the_week.index(day1)
    ind2 = days_of_the_week.index(day2)
    return days_of_the_week[ind1 : ind2 + 1]


def split_days_mention(days_mention):
    return [day_mention.strip() for day_mention in days_mention.split(",")]


days_of_the_week = [
    "Mon",
    "Tues",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun",
]


def get_opening_hours_from_hours_mention(hours_mention):
    start, end = split_hours_mention(hours_mention)
    start_t = convert_time_string_to_time_obj(start)
    end_t = convert_time_string_to_time_obj(end)
    return [start_t, end_t]


def split_hours_mention(hours_mention):
    start, end = [time.strip() for time in hours_mention.split("-")]
    return (start, end)


def convert_time_string_to_time_obj(time_string):
    """Time string is something like "11 am" or 10:30 pm"."""

    hour_min, suffix = time_string.split(" ")

    if ":" in hour_min:
        hour, min = [int(part) for part in hour_min.split(":")]
    else:
        hour, min = int(hour_min), 0

    if (hour == 12) and (suffix == "pm"):
        hour = 12
    elif (hour == 12) and (suffix == "am"):
        hour = 0
    elif suffix == "pm":
        hour += 12
    return time(hour=hour, minute=min)


def days_and_hours_mention_to_weekly_table_format(days_and_hours_mention):
    opening_hours = get_opening_hours_from_days_and_hours_mention(
        days_and_hours_mention
    )

    weekly_table_format_dicts = []
    for day, open_time, close_time in opening_hours:
        if open_time <= close_time:
            weekly_table_format_dicts.append(
                dict(
                    day=day,
                    open_time=open_time,
                    close_time=close_time,
                )
            )

        # this is to catch the case when the close time goes past midnight
        else:
            weekly_table_format_dicts.extend(
                [
                    dict(
                        day=day,
                        open_time=open_time,
                        close_time=time.max,
                    ),
                    dict(
                        day=get_next_day(day),
                        open_time=time.min,
                        close_time=close_time,
                    ),
                ]
            )

    return weekly_table_format_dicts


def get_next_day(day):
    day_ind = days_of_the_week.index(day)
    next_day_ind = (day_ind + 1) % len(days_of_the_week)
    return days_of_the_week[next_day_ind]


def csv_row_to_weekly_table_format(row):
    name, days_and_hours_field = row
    days_and_hours_mentions = split_days_and_hours_field(days_and_hours_field)
    weekly_table_format_dicts = []
    for days_and_hours_mention in days_and_hours_mentions:
        weekly_table_format_dicts.extend(
            days_and_hours_mention_to_weekly_table_format(days_and_hours_mention)
        )
    for weekly_table_format_dict in weekly_table_format_dicts:
        weekly_table_format_dict.update(dict(name=name))

    return weekly_table_format_dicts
