'''CRUD operations.'''

from model import User, Loved_Cocktail, Cocktail, Recipe, Ingredient

def create_user(fname, email, password):
    """Create and return a new user."""

    user = User(fname = fname, email=email, password=password)

    return user

def create_loved_cocktail(user_id, cocktail_id, name):
    """Create and return a loved cocktail."""
    loved_cocktail = Loved_Cocktail(user_id = user_id, cocktail_id = cocktail_id, name = name)

    return loved_cocktail

def create_cocktail(name, strength, flavor, flavor2, flavor3):
    """Create and return a cocktail"""
    cocktail = Cocktail(name= name, strength = strength, flavor = flavor, flavor2 = flavor2, flavor3 = flavor3)

    return cocktail

def create_recipe(cocktail_id, ingredient_id, part):
    """Create and return a recipe"""
    recipe = Recipe(cocktail_id = cocktail_id, ingredient_id = ingredient_id, part = part)

    return recipe

def create_ingredient(name, type, subtype):
    """Create and return an ingredient"""
    ingredient = Ingredient(name = name, type= type, subtype = subtype)

    return ingredient
    
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


if __name__ == '__main__':
    from server import app
    connect_to_db(app)