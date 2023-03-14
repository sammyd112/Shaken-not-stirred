'''CRUD operations.'''

from model import User, Loved_Cocktail, Cocktail, Recipe, Ingredient, db, connect_to_db
import random 

def create_user(fname, email, password):
    """Create and return a new user."""

    user = User(
                fname=fname, 
                email=email, 
                password=password
                )

    return user

def get_user_by_email(email):
    """Return a user by email."""
    return User.query.filter(User.email == email).first()

def get_user_by_creds(email, password):
    return User.query.filter(User.email ==email, User.password == password).first()

def create_loved_cocktail(user_id, cocktail_id, name):
    """Create and return a loved cocktail."""
    loved_cocktail = Loved_Cocktail(user_id=user_id,
                                    cocktail_id=cocktail_id,
                                    name=name)

    return loved_cocktail

def create_cocktail(name, strength, flavor, flavor2, flavor3):
    """Create and return a cocktail"""
    cocktail = Cocktail(name=name, 
                        strength=strength, 
                        flavor=flavor, 
                        flavor2=flavor2, 
                        flavor3=flavor3
                        )

    return cocktail

def get_cocktail_by_name(name):
    return Cocktail.query.filter(Cocktail.name == name).first()

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
        print(dbcocktail)
        add_to_cocktail = {'strength':dbcocktail.strength, 'flavors' : [dbcocktail.flavor, dbcocktail.flavor2, dbcocktail.flavor3]}
        cocktail.update(add_to_cocktail)
        dbcocktails.append(cocktail)
    return dbcocktails

test_list = {'strengths': ['Weak', 'Moderate'], 'flavors': ['bitter', 'creamy', 'tropical'], 'spirits': ['Vodka', 'Rum']}
def create_quiz_results(list):
    dbcocktails = create_quiz_dict
    




if __name__ == '__main__':
    from server import app
    connect_to_db(app)