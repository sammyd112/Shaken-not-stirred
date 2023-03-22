'''CRUD operations.'''

from model import User, Loved_Cocktail, Cocktail, Recipe, Ingredient, Personal_Cocktail, db, connect_to_db
import random 
from data import categories

def create_user(fname, email, password):
    """Create and return a new user."""

    user = User(
                fname=fname, 
                email=email, 
                password=password
                )

    return user

def get_user_by_email1(email):
    """Return a user by email."""
    return User.query.filter(User.email == email).first()

def get_user_by_creds(email, password):
    return User.query.filter(User.email ==email, User.password == password).first()

def get_user_by_email(email):
    user = User.query.filter(User.email == email).one()
    return user.user_id

def create_loved_cocktail(user_id, cocktail_id):
    """Create and return a loved cocktail."""
    loved_cocktail = Loved_Cocktail(user_id=user_id,
                                    cocktail_id=cocktail_id,)

    return loved_cocktail

def get_all_personal_cocktails(user_id):
    return Personal_Cocktail.query.filter(Personal_Cocktail.user_id == user_id).all()

def get_all_loved_cocktails_by_user(user_id):
    return Loved_Cocktail.query.filter(Loved_Cocktail.user_id == user_id).all()

def create_cocktail(name, strength, flavor, flavor2, flavor3):
    """Create and return a cocktail"""
    cocktail = Cocktail(name=name, 
                        strength=strength, 
                        flavor=flavor, 
                        flavor2=flavor2, 
                        flavor3=flavor3
                        )

    return cocktail

def create_personal_cocktail(name, user_id, ingredient1, ingredient2, ingredient3, ingredient4, ingredient5, ingredient6, ingredient7, notes):
    personal_cocktail = Personal_Cocktail(name = name,
                                          user_id = user_id,
                                          ingredient1 = ingredient1,
                                          ingredient2 = ingredient2,
                                          ingredient3 = ingredient3,
                                          ingredient4 = ingredient4,
                                          ingredient5 = ingredient5,
                                          ingredient6 = ingredient6,
                                          ingredient7 = ingredient7,
                                          notes = notes)
    return personal_cocktail

def get_cocktail_by_name(name):
    return Cocktail.query.filter(Cocktail.name == name).first()

def get_cocktail_by_id(id):
    return Cocktail.query.filter(Cocktail.cocktail_id == id).first()

def get_all_cocktails():
    return Cocktail.query.all()

def create_recipe(cocktail_id, ingredient_id, part):
    """Create and return a recipe"""
    recipe = Recipe(cocktail_id=cocktail_id,
                    ingredient_id=ingredient_id,
                    part=part)

    return recipe

def create_ingredient(name, type, subtype):
    """Create and return an ingredient"""
    ingredient = Ingredient(name=name,
                            type=type, 
                            subtype=subtype)

    return ingredient

def get_ingredient_by_name(name):
    return Ingredient.query.filter(Ingredient.name == name).first()

def get_ingredient_by_id(ingredient_id):
    return Ingredient.query.filter(Ingredient.ingredient_id == ingredient_id).first()
    
def display_search(drink):
    """Display Search"""
    name = drink["strDrink"]
    ingredients = []
    instructions = drink["strInstructions"]
    for n in range(1,15):
        ingredient = drink[f"strIngredient{n}"]
        measurement = drink[f"strMeasure{n}"]
        if ingredient or measurement != None:
            ingredients.append((ingredient, measurement))
    return {'name' : name, 'ingredients': ingredients, 'instruction': instructions}

def display_cocktail(name):
    cocktail = get_cocktail_by_name(name)
    if type(cocktail) != type(None):
        recipes =  Recipe.query.filter(Recipe.cocktail_id == cocktail.cocktail_id).all()
        instructions = []
        for recipe in recipes:
            ingredient = get_ingredient_by_id(recipe.ingredient_id)
            instructions.append((ingredient.name, recipe.part))
        return {'name' : cocktail.name, 'ingredients' : instructions}
    else:
        return {'Nothing' : name}

def get_random_cocktail():
    cocktails = get_all_cocktails()
    cocktail = random.choice(cocktails)
    return display_cocktail(cocktail.name)

dict={'strengths': ['strong', 'extrastrong'], 'flavors' : ['neutral', 'citrus'], 'spirits' : ['vodka']}

def match_cocktail_quiz(dict):
    matched_cocktails = []
    cocktails = get_all_cocktails()


def create_cocktail_with_ingredients():
    cocktails = get_all_cocktails()
    dbcocktails=[]
    for cocktail in cocktails:
        recipes =  Recipe.query.filter(Recipe.cocktail_id == cocktail.cocktail_id).all()
        ingredients = []
        for recipe in recipes:
            ingredient = get_ingredient_by_id(recipe.ingredient_id)
            if ingredient.name == 'enhancements':
                continue
            elif ingredient.name == 'Enhancements':
                continue
            else:
                ingredients.append(ingredient.name)
        dbcocktails.append({'name' : cocktail.name, 'ingredients' : ingredients})
    return dbcocktails
    
example_list = ['Vodka', 'Kahlua', 'Milk']
def create_cocktail_match(list):
    db_match = []
    dbcocktails = create_cocktail_with_ingredients()
    for dbcocktail in dbcocktails:
        total_ingredients = len(dbcocktail['ingredients'])
        matched_points = 0
        missing_ingredients = dbcocktail['ingredients']
        for items in list:
            for x in items:
                if x in dbcocktail['ingredients']:
                    matched_points += 1
                    missing_ingredients.remove(x)
        db_match.append((dbcocktail['name'], matched_points, total_ingredients, missing_ingredients))
    drink_match = []
    two_ingreds = []
    three_ingreds = []
    four_ingreds = []
    five_or_more = []
    for cocktail in db_match:
        if len(cocktail[3]) == 0:
            if cocktail[2] == 2:
                two_ingreds.append(cocktail)
            if cocktail[2] == 3:
                three_ingreds.append(cocktail)
            if cocktail[2] == 4:
                four_ingreds.append(cocktail)
            if cocktail[2] >= 5:
                five_or_more.append(cocktail)
    drink_match.extend(five_or_more)
    drink_match.extend(four_ingreds)
    drink_match.extend(three_ingreds)
    drink_match.extend(two_ingreds)
    two_ingreds1 = []
    three_ingreds1 = []
    four_ingreds1 = []
    five_or_more1 = []
    for cocktail in db_match:
        if len(cocktail[3]) == 1:
            if cocktail[2] == 2:
                two_ingreds1.append(cocktail)
            if cocktail[2] == 3:
                three_ingreds1.append(cocktail)
            if cocktail[2] == 4:
                four_ingreds1.append(cocktail)
            if cocktail[2] >= 5:
                five_or_more1.append(cocktail)
    drink_match.extend(five_or_more1)
    drink_match.extend(four_ingreds1)
    drink_match.extend(three_ingreds1)
    drink_match.extend(two_ingreds1)

    display_match = []
    for cocktail in drink_match:
        cocktail_dic = display_cocktail(cocktail[0])
        cocktail_dic['missing'] = cocktail[3]
        display_match.append(cocktail_dic)

    return display_match

def create_quiz_dict():
    dbcocktails = []
    cocktails = create_cocktail_with_ingredients()
    for cocktail in cocktails:
        dbcocktail = get_cocktail_by_name(cocktail['name'])
        add_to_cocktail = {'strength':dbcocktail.strength, 'flavors' : [dbcocktail.flavor, dbcocktail.flavor2, dbcocktail.flavor3]}
        cocktail.update(add_to_cocktail)
        dbcocktails.append(cocktail)
    return dbcocktails

def lower_list(list):
    new_list = []
    for string in list:
       n_string = string.lower()
       new_list.append(n_string)
    return new_list

def upper_list(list):
    new_list = []
    for string in list:
       n_string = string.upper()
       new_list.append(n_string)
    return new_list

test_list = {'strengths': ['weak', 'moderate'], 'flavors': ['creamy', 'tropical'], 'spirits': ['Vodka', 'Rum']}
def create_quiz_results(list):
    dbcocktails = create_quiz_dict()
    possible_matches = []
    possible_matches2 = []
    possible_matches3 = []
    vodkas = categories.vodkas
    whiskeys = categories.whiskey_like
    rums = categories.rums
    for cocktail in dbcocktails:
        for n in range(0, len(list['flavors'])):
            if list['flavors'][n] in cocktail['flavors']:
                possible_matches.append(cocktail)
    for cocktail in possible_matches:
        for n in range(0, len(list['spirits'])):
            if list['spirits'][n] == 'Vodka':
                for spirit in vodkas:
                    if spirit in cocktail['ingredients']:
                        possible_matches2.append(cocktail)
            elif list['spirits'][n] == 'Whiskey/Bourbon':
                for spirit in whiskeys:
                    if spirit in cocktail['ingredients']:
                        possible_matches2.append(cocktail)
            elif list['spirits'][n] == 'Rum':
                for spirit in rums:
                    if spirit in cocktail['ingredients']:
                        possible_matches2.append(cocktail)
            elif list['spirits'][n] in cocktail['ingredients']:
                possible_matches2.append(cocktail)
            elif cocktail['strength'] == 'weak':
                possible_matches2.append(cocktail)
            elif list['spirits'][n] == 'Im Not Particular':
                possible_matches2 = possible_matches
    for cocktail in possible_matches2:
        for n in range(0, len(list['strengths'])):
            if list['strengths'][n] == "so strong, it's a fancy way to pour liquor into a glass":
                list['strengths'][n] = 'extrastrong'
            elif list['strengths'][n] == cocktail['strength']:
                possible_matches3.append(cocktail)
    matches = []
    for x in possible_matches3:
        if possible_matches3.count(x) > 1 and x not in matches:
            matches.append(x)
    seco_tier_matches = []
    for cocktail in possible_matches3:
        if cocktail not in matches:
            matches.append(cocktail)
    return_dict = {'matches': matches}
    return return_dict



def display_loved_cocktails(user_id):
    loved_cocktails = get_all_loved_cocktails_by_user(user_id)
    personal_cocktails = get_all_personal_cocktails(user_id)
    favorites = []
    personal = []
    favorites_dic = {}
    for x in loved_cocktails:
        cocktail = get_cocktail_by_id(x.cocktail_id)
        cocktail_dic = display_cocktail(cocktail.name)
        favorites.append(cocktail_dic)
    for x in personal_cocktails:
        dic = {}
        dic['name'] = x.name
        dic['ingredients'] = [x.ingredient1, x.ingredient2, x.ingredient3, x.ingredient4, x.ingredient5, x.ingredient5, x.ingredient6, x.ingredient7]
        dic['notes'] = x.notes
        personal.append(dic)

    favorites_dic['favorites'] = favorites
    favorites_dic['personal'] = personal
    return favorites_dic
    

if __name__ == '__main__':
    from server import app
    connect_to_db(app)