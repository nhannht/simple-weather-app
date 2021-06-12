import sys

import requests
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask import flash
from model import key

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, unique=True, nullable=False)
    degree = db.Column(db.Float, nullable=False)
    state = db.Column(db.Integer, nullable=False)


db.create_all()


def fetch_from_openweather_and_insert_to_db(city):
    url = f'http://api.openweathermap.org/data/2.5/weather'

    arg = {'q': f'{city}',
           'appid': f'{key}'}
    req = requests.get(url, arg)
    status = req.ok
    if status:
        respond = req.json()
        degree = respond['main']['temp'] -275.13
        degree = round(degree,2)
        state = respond['weather'][0]['description']
        city = City(city=city, degree=degree, state=state)
        db.session.add(city)
        try:
            flash("The city doesn't exist!")
            db.session.commit()
        except IntegrityError:
            flash("The city has already been added to the list!")
            db.session.rollback()
    else:
        flash("The city doesn't exist!")

def fetch_all_data():
    out = City.query.all()
    return out


@app.route('/', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        city_name = request.form["city-name"]
        print(city_name)
        fetch_from_openweather_and_insert_to_db(city_name)
        cities = fetch_all_data()
        return render_template('index.html', cities=cities)
    elif request.method == 'GET':
        cities = fetch_all_data()

        return render_template('index.html', cities=cities)


@app.route('/delete/<id_city>', methods=['GET', 'POST'])
def delete(id_city):
    city = City.query.filter_by(id=id_city).first()
    if city is None:
        flash("The city doesn't exist")
        return redirect('/')
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


@app.errorhandler(500)
def internal_server_erro(error):
    return redirect('/')


@app.route('/login')
def log_in():
    return 'This is login page'


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port, debug=True)
    else:
        app.run()
