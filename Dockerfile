FROM python:3
MAINTAINER Zheltikov Denis <den.ari@yandex.ru>

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

RUN python manage.py makemigrations
RUN python manage.py migrate

CMD python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

CMD python manage.py runserver 0.0.0.0:8000
#CMD python runbot.py
