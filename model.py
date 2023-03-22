from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String) 

    def __repr__(self):
        return f'<User fname={self.fname} email={self.email}>'

    
class Loved_Cocktail(db.Model):
    """A loved cocktail"""

    __tablename__ = 'loved_cocktails'

    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key = True,)
    user_id = db.Column(db.Integer, 
                       db.ForeignKey('users.user_id'))
    cocktail_id = db.Column(db.Integer,
                            db.ForeignKey('cocktails.cocktail_id'))
    
    def __repr__(self):
        return f'<Loved Cocktail id={self.id} user_id={self.user_id} cocktail_id={self.cocktail_id}>'
    
class Cocktail(db.Model):
    """A cocktail""" 

    __tablename__ = 'cocktails'

    cocktail_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    name = db.Column(db.String)
    strength = db.Column(db.String)
    flavor = db.Column(db.String)
    flavor2 = db.Column(db.String)
    flavor3 = db.Column(db.String)
    recipe = db.relationship("Recipe", back_populates="cocktail")

    def __repr__(self):
        return f'<Cocktail cocktail_id={self.cocktail_id} name={self.name}>'

class Recipe(db.Model):
    """Cocktail Ingredients"""

    __tablename__ = 'recipe'

    id = db.Column(db.Integer,
                   autoincrement = True,
                   primary_key = True)
    cocktail_id = db.Column(db.Integer,
                      db.ForeignKey('cocktails.cocktail_id'))
    ingredient_id = db.Column(db.Integer,
                               db.ForeignKey('ingredients.ingredient_id'))
    part = db.Column(db.String)
    
    cocktail = db.relationship("Cocktail", back_populates="recipe")
    ingredient = db.relationship("Ingredient", back_populates="recipe")
    
    def __repr__(self):
        return f'<Recipe id={self.id} cocktail_id={self.cocktail_id} ingredient_id={self.ingredient_id}'


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    ingredient_id = db.Column(db.Integer,
                              autoincrement = True,
                              primary_key = True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    subtype = db.Column(db.String)

    recipe = db.relationship("Recipe", back_populates="ingredient")

    def __repr__(self):
        return f'<Recipe ingredient_id={self.ingredient_id} name={self.name}'
    
class Personal_Cocktail(db.Model):
    __tablename__ = 'personal_cocktails'

    personal_id = db.Column(db.Integer,
                              autoincrement = True,
                              primary_key = True)
    user_id = db.Column(db.Integer, 
                       db.ForeignKey('users.user_id'))
    name = db.Column(db.String)
    ingredient1 = db.Column(db.String)
    ingredient2 = db.Column(db.String)
    ingredient3 = db.Column(db.String)
    ingredient4 = db.Column(db.String)
    ingredient5 = db.Column(db.String)
    ingredient6 = db.Column(db.String)
    ingredient7 = db.Column(db.String)
    notes = db.Column(db.String)
    
    def __repr__(self):
        return f'<Personal_Cocktail user_id={self.user_id} name={self.name}'


def connect_to_db(flask_app, db_uri="postgresql:///shakennotstirred", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    with app.app_context():
        connect_to_db(app)