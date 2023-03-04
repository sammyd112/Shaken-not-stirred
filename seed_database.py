"""Script to seed database."""

import os
from random import choice, randint
import crud
import model
import ast
from server import app
from pprint import pprint

### the database pulled from
from data.dict import cocktail_data
from data import categories

os.system("dropdb cocktails")
os.system("createdb cocktails")


cocktails_in_db= []
for cocktail, key in cocktail_data.items():
    name = cocktail
    for attribute, value in key.items():
        if attribute == 'Strength':
            strength = value
        if attribute == 'Flavor':
            if len(value) == 3:
                flavor = value[0]
                flavor2 = value[1]
                flavor3 = value[2]
            if len(value) == 2:
                flavor = value[0]
                flavor2 = value[1]
                flavor3 = None
            if len(value) == 1:
                flavor = value[0]
                flavor2 = None
                flavor3 = None
            
    cocktail = crud.create_cocktail(name, strength, flavor, flavor2, flavor3)
    cocktails_in_db.append(cocktail) 


ingredients_in_db= set()

for cocktail, key in cocktail_data.items():
    for attribute in key:
        name = attribute
        if name in categories.spirits:
            type = 'Spirit'
            if name in categories.vodkas:
                subtype = 'Vodka'
            elif name in categories.whiskey_like:
                subtype = 'Whiskey-like'
            elif name in categories.rums:
                subtype = 'Rum'
            elif name == 'Gin':
                subtype = 'Gin'
            elif name == 'Tequila':
                subtype = 'Tequila'
            else:
                subtype = 'None'
        elif name in categories.wines:
            type = 'Wine'
            subtype = None
        elif name in categories.beer:
            type = 'Beer'
        elif name in categories.fruits:
            type = 'Fruit'
        elif name in categories.cordials:
            type = 'Cordial'
            subtype = None
        elif name in categories.mixers:
            type = 'Mixer'
            subtype = None
        else:
            type = None
            subtype = None
        ingredient = crud.create_ingredient(name, type, subtype)  
        ingredients_in_db.append(ingredient)
        
        





with app.app_context():
    model.connect_to_db(app)
    model.db.create_all()
    model.db.session.add_all(cocktails_in_db, ingredients_in_db)
    model.db.session.commit()
