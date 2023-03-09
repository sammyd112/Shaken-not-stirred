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


if __name__ == '__main__':
    from server import app
    connect_to_db(app)