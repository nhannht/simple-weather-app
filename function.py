import requests
from flask import flash
from sqlalchemy.exc import IntegrityError

from core import db
from core import key
from model import City


def fetch_from_openweather_and_insert_to_db(city):
    url = f'https://api.openweathermap.org/data/2.5/weather'

    arg = {'q': f'{city}',
           'appid': f'{key}'}
    req = requests.get(url, arg)
    status = req.ok
    if status:
        respond = req.json()
        degree = respond['main']['temp'] - 275.13
        degree = round(degree, 2)
        state = respond['weather'][0]['description']
        city = City(city=city, degree=degree, state=state)
        db.session.add(city)
        try:
            db.session.commit()
        except IntegrityError:
            flash("The city has already been added to the list!")
            db.session.rollback()
    else:
        flash("The city doesn't exist in the world!")


def fetch_all_data():
    out = City.query.all()
    return out
