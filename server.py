from flask import (Flask, redirect, request, render_template, session, jsonify, flash)
from jinja2 import StrictUndefined
from pprint import pformat, pprint
import os
import requests
import crud
from data import categories
from model import connect_to_db, db
import random
import json


app = Flask(__name__)
app.secret_key = "SECRETSECRET"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    return render_template("homepage.html")

@app.route('/login', methods = ['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = crud.get_user_by_creds(email, password)
    if user == None:
        flash('User does not exist or wrong password. Try again, or create an account.')
        print('NO')
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.fname}!")
        print('YES')
    return render_template("homepage.html")
    

@app.route('/signup', methods = ['POST'])
def create_user():
    email = request.form['email']
    password = request.form['password']
    fname = request.form['fname']

    if crud.get_user_by_email(email):
        flash("You can't create an account with that email. Try again.")
        print("no")
    else:
        user = crud.create_user(fname, email, password)
        db.session.add(user)
        db.session.commit()
        session["user_email"] = user.email
        flash("Your account was created successfully!")
        print('yes')
    return render_template("homepage.html")

@app.route('/profile')
def show_profile():
    return render_template("profile.html")

@app.route('/logout')
def log_out():
    session.clear()
    return render_template("homepage.html")


@app.route('/goingout')
def show_out_selections():
    return render_template("goingout.html")

@app.route('/quizchoices')
def get_quiz():
    flavors = categories.flavors
    strengths = categories.strengths
    spirit_choice = categories.choices
    options = {'flavors' : flavors, 'strengths' : strengths, 'spirits' : spirit_choice}
    return options

@app.route('/random')
def get_random():
    cocktail = crud.get_random_cocktail()
    return jsonify(cocktail)

@app.route('/russian')
def get_russian_routlette():
    spirit = random.choice(categories.spirits)
    cordial = random.choice(categories.cordials)
    mixer = random.choice(categories.mixers)
    return jsonify({'spirit' : spirit, 'cordial' : cordial, 'ingredient' : mixer})

@app.route('/quiz', methods = ['POST'])
def get_answers():
    quiz_data = {}
    strengths = request.form.getlist('strengths')
    flavors = request.form.getlist('flavors')
    spirits = request.form.getlist('spirits')
    quiz_data['strengths'] = strengths
    quiz_data['flavors'] = flavors
    quiz_data['spirits'] = spirits
    print(quiz_data)
    return quiz_data

@app.route('/stayin')
def show_in_selections():
    return render_template("stayin.html")

@app.route('/stayin', methods = ["POST"])
def get_search():
    drink = (request.json['drink_input']).title()
    data = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink}")
    data = data.json()
    if data['drinks'] != None:
        drink_data = data['drinks'][0]
        final_data = crud.display_search(drink_data)
        return final_data
    if data['drinks'] == None:
        drink_search = crud.display_cocktail(drink)
        return drink_search
    
@app.route('/makechoices')
def make_choices():
    ingredients = sorted(categories.mixers)
    cordials = sorted(categories.cordials)
    spirits = categories.spirits_dic
    return {'ingredients': ingredients, 'cordials' : cordials, 'spirits' : spirits}

@app.route('/makesuggestions', methods = ['POST'])
def make_cocktail():
    make_data = []
    ingredients = request.form.getlist('ingred')
    make_data.append(ingredients)
    print(make_data)
    match_data = crud.create_cocktail_match(make_data)
    match_data = json.dumps(match_data)
    print(match_data)
    return match_data


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)