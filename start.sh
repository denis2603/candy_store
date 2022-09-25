#!/bin/bash

python manage.py runserver 0.0.0.0:$PORT &
python runbot.py

