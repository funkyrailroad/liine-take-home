#! /bin/bash
sleep 1
python manage.py migrate
python manage.py load_csv_to_weekly_table
python manage.py runserver 0:8000
