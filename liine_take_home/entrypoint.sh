#! /bin/bash
# sleep 1
python manage.py migrate
python manage.py runserver 0:8000
