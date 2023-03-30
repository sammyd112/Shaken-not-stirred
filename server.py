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
app.secret_key = "secretsecretsecret"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['GOOGLE_KEY']


@app.route('/')
def show_homepage():
    return render_template("homepage.html")

@app.route('/login', methods = ['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = crud.get_user_by_creds(email, password)
    if user == None:
        flash('Account does not exit or incorrect email/password', 'warning')
    else:
        session["user_email"] = user.email
        session["fname"] = user.fname
        flash(f"Welcome back, {session['fname']}", "success")
    return render_template("homepage.html")

@app.route('/getage', methods = ['POST'])
def add_age_to_session():
    age = request.json['age']
    print(age)
    if age == 'I am 21':
        session["age"] = 'True'
    return {"message": ["success", "It's the beginning of the end, but at least you can drink! Enjoy!"]}

@app.route('/addfavorite', methods = ['POST'])
def add_favorite():
    cocktail_name = request.json['drink_name']
    print(cocktail_name)
    if 'user_email' in session:
        email = session['user_email']
        user_id = crud.get_user_by_email(email)
        if crud.get_cocktail_by_name(cocktail_name):
            cocktail = crud.get_cocktail_by_name(cocktail_name)
            Loved_Cocktail = crud.create_loved_cocktail(user_id, cocktail.cocktail_id)
            db.session.add(Loved_Cocktail)
            db.session.commit()
            return {'message': ['success', f'{cocktail_name} was added to your favorites!']}
        else:
            data = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/search.php?s={cocktail_name}")
            data = data.json()
            drink_data = data['drinks'][0]
            data_d = crud.display_search(drink_data)
            print(data_d)
            cocktail = crud.create_personal_cocktail(data_d['name'], user_id, data_d['ingredients'][0], data_d['ingredients'][1], data_d['ingredients'][2], data_d['ingredients'][3], data_d['ingredients'][4], data_d['ingredients'][5], 'database', data_d['instruction'])
            db.session.add(cocktail)
            db.session.commit()
            return {'message': ['success', f'{cocktail_name} was added to your favorites!']}
    else:
        return {'message': ['warning', 'Please login/sign up to add favorite']}

    
@app.route('/signup', methods = ['POST'])
def create_user():
    email = request.form['email']
    password = request.form['password']
    fname = request.form['fname']
    print(email)
    print(fname)
    if crud.get_user_by_email1(email):
        flash('Email is already being used by another account', 'warning')
    elif len(password) < 6:
        flash('Password must be at least 6 characters long', 'warning')
    elif password.isalpha():
        flash('Password must contain at least one number', 'warning')
    elif fname == '':
        flash('Please make sure to fill all required fields', 'warning')
    elif email == '':
        flash('Please make sure to fill all required fields', 'warning')
    else:
        user = crud.create_user(fname.title(), email, password)
        db.session.add(user)
        db.session.commit()
        session["user_email"] = user.email
        session["fname"] = user.fname
        flash(f'Account has been successfully created, {session["fname"]}', 'success')
    return render_template('homepage.html')

@app.route('/showfavorites')
def show_favorites():
    if 'user_email' in session:
        email = session['user_email']
        user_id = crud.get_user_by_email(email)
        return crud.display_loved_cocktails(user_id)
    
@app.route('/addownfavorite', methods=["POST"])
def add_own_favorite():
    name = request.form['name']
    ingredient1 = request.form['ingredient1']
    ingredient2 = request.form['ingredient2']
    ingredient3 = request.form['ingredient3']
    ingredient4 = request.form['ingredient4']
    ingredient5 = request.form['ingredient5']
    ingredient6 = request.form['ingredient6']
    ingredient7 = request.form['ingredient7']
    notes = request.form['notes']
    email = session['user_email']
    print(name, ingredient1, ingredient2, ingredient3, ingredient4, ingredient5, ingredient6, ingredient7, notes)
    user_id = crud.get_user_by_email(email)
    cocktail = crud.create_personal_cocktail(name.title(), user_id, ingredient1.title(), ingredient2.title(), ingredient3.title(), ingredient4.title(), ingredient5.title(), ingredient6.title(), ingredient7.title(), notes.title())
    db.session.add(cocktail)
    db.session.commit()
    return redirect("/profile")

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
    flavors = crud.lower_list(flavors)
    strengths = crud.lower_list(strengths)
    quiz_data['strengths'] = strengths
    quiz_data['flavors'] = flavors
    quiz_data['spirits'] = spirits
    print(quiz_data)
    result = crud.create_quiz_results(quiz_data)
    print(result)
    return result

@app.route('/stayin')
def show_in_selections():
    return render_template("stayin.html")

@app.route('/stayin', methods = ["POST"])
def get_search():
    drink = (request.json['drink_input']).title()
    data = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink}")
    data = data.json()
    if crud.get_cocktail_by_name(drink):
        drink_search = crud.display_cocktail(drink)
        print(drink_search)
        return drink_search
    elif data['drinks'] != None:
        drink_data = data['drinks'][0]
        final_data = crud.display_search(drink_data)
        print(final_data)
        return final_data
    else:
        return {'nope': 'try again'}
        
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

@app.route('/deletefav', methods = ['POST'])
def delete_fav():
    name = request.json['drink_name']
    print(name)
    user_id = crud.get_user_by_email(session['user_email'])
    if crud.get_cocktail_by_name(name):
        cocktail = crud.get_cocktail_by_name(name)
        loved_cocktail = crud.get_loved_cocktail_by_creds(user_id, cocktail.cocktail_id)
        db.session.delete(loved_cocktail)
        db.session.commit() 
    else:
        personal_cocktail = crud.get_personal_cocktail_by_creds(user_id, name)
        print(personal_cocktail)
        db.session.delete(personal_cocktail)
        db.session.commit() 
    return redirect('/profile')

@app.route('/gout')
def get_map():
    return render_template('maps.html', API_KEY = API_KEY)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)