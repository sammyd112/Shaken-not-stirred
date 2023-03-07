from flask import Flask, redirect, request, render_template, session, jsonify
from jinja2 import StrictUndefined
from pprint import pformat, pprint
import os
import requests
import json
import urllib.request
import crud
from data import categories


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    
    return render_template("homepage.html")

@app.route('/goingout')
def show_out_selections():
    return render_template("goingout.html")

@app.route('/goingout', methods = ['POST'])
def get_quiz():
    flavors = categories.flavors
    strengths = categories.strengths
    spirit_choice = categories.choices
    options = {'flavors' : flavors, 'strengths' : strengths, 'spirits' : spirit_choice}
    return options

@app.route('/stayin')
def show_in_selections():
    return render_template("stayin.html")

@app.route('/stayin', methods = ["POST"])
def get_search():
    drink = request.json['drink_input']
    print(drink)
    data = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink}")
    if data != None:
        data = data.json()
        drink_data = data['drinks'][0]
        final_data = crud.display_search(drink_data)
        return final_data
    if data == None:
        drink_search = crud.display_cocktail(drink)
        return drink_search



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)