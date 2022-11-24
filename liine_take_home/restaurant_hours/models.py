from django.db import models


class WeeklyOpeningHours(models.Model):
    name = models.CharField(max_length=100, blank=False)

    days_of_the_week = [
        ("Mon", "Monday"),
        ("Tues", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat", "Saturday"),
        ("Sun", "Sunday"),
    ]

    day = models.CharField(max_length=4, choices=days_of_the_week, blank=False)
    open_time = models.TimeField()
    close_time = models.TimeField()
