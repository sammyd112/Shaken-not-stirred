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

os.system('dropdb shakennotstirred')
os.system('createdb shakennotstirred')

model.connect_to_db(app)
app.app_context().push()
model.db.create_all()


# """seeding for cocktails datatable"""
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
    model.db.session.add(cocktail)


# """Seeding for ingredients datatable"""
ingredients= set()
ingredients_in_db = []
names = []

for cocktail, key in cocktail_data.items():
    for attribute in key:
        name = attribute
        if name == 'Strength':
            continue
        elif name == 'Flavor':
            continue
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
            subtype = None
        elif name in categories.fruits:
            type = 'Fruit'
            subtype = None
        elif name in categories.cordials:
            type = 'Cordial'
            subtype = None
        elif name in categories.mixers:
            type = 'Mixer'
            subtype = None
        else:
            type = None
            subtype = None
        ingredients.add((name, type, subtype))

for ingredient in ingredients:
    name = ingredient[0]
    type = ingredient[1]
    subtype = ingredient[2]
    db_ingredient = crud.create_ingredient(name, type, subtype)
    ingredients_in_db.append(db_ingredient)

model.db.session.add_all(ingredients_in_db)
model.db.session.commit()

"""Seeding for Recipe"""
"""def create_recipe(cocktail_id, ingredient_id, part):"""
recipe_in_db = []
for cocktail, key in cocktail_data.items():
    name = cocktail
    for attribute, des in key.items():
        if attribute == 'Flavor' or attribute == 'Strength':
            continue
        part = des
        ingredient = crud.get_ingredient_by_name(attribute)
        cocktail = crud.get_cocktail_by_name(name)
        dbrecipe = crud.create_recipe(cocktail.cocktail_id, ingredient.ingredient_id, part)
        recipe_in_db.append(dbrecipe)

model.db.session.add_all(recipe_in_db)
model.db.session.commit()



"""Seeding for test Users"""

for n in range(10):
    fname = f'tester{n}'
    email = f'user{n}@test.com' 
    password = 'test'

    user = crud.create_user(fname, email, password)
    model.db.session.add(user)

model.db.session.commit()


