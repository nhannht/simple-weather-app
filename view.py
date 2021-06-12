from flask import redirect
from flask import render_template
from flask import request
from function import *
from core import app
from model import User

db.drop_all()
db.create_all()


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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            flash("User already in db")
            db.session.rollback()
        return redirect('/')

@app.route('/delete/<id_city>', methods=['GET', 'POST'])
def delete(id_city):
    city = City.query.filter_by(id=id_city).first()
    if city is None:
        flash("The city doesn't exist in database")
        return redirect('/')
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


@app.errorhandler(500)
def internal_server_erro(error):
    return redirect('/')


@app.errorhandler(404)
def internal_server_erro(error):
    return redirect('/')

# don't change the following way to run flask:
