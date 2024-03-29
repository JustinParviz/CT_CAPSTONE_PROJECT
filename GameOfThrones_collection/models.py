from werkzeug.security import generate_password_hash #generates a unique password hash for extra security 
from flask_sqlalchemy import SQLAlchemy #this is our ORM (Object Relational Mapper)
from flask_login import UserMixin, LoginManager #helping us load a user as our current_user 
from datetime import datetime #put a timestamp on any data we create (Users, Products, etc)
import uuid #makes a unique id for our data (primary key)
from flask_marshmallow import Marshmallow


#internal imports
from .helpers import get_character


#instantiate all our classes
db = SQLAlchemy() #make database object
login_manager = LoginManager() #makes login object 
ma = Marshmallow() #makes marshmallow object


#use login_manager object to create a user_loader function
@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id) #this is a basic query inside our database to bring back a specific User object

#think of these as admin (keeping track of what products are available to sell)
class User(db.Model, UserMixin): 
    #CREATE TABLE User, all the columns we create
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow) #this is going to grab a timestamp as soon as a User object is instantiated


    #INSERT INTO User() Values()
    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email 
        self.password = self.set_password(password) 



    #methods for editting our attributes 
    def set_id(self):
        return str(uuid.uuid4()) #all this is doing is creating a unique identification token
    

    def get_id(self):
        return str(self.user_id) #UserMixin using this method to grab the user_id on the object logged in
    
    
    def set_password(self, password):
        return generate_password_hash(password) #hashes the password so it is secure (aka no one can see it)
    

    def __repr__(self):
        return f"<User: {self.username}>"
    

class Character(db.Model): #db.Model helps us translate python code to columns in SQL 
    character_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    family = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String)
    description = db.Column(db.String(300))
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    #eventually we need to connect this to orders 


    def __init__(self, first_name, last_name, full_name, title, family, image, description=""):
        self.character_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name  
        self.title = title
        self.family = family
        self.image = image
        self.description = description

    
    def set_id(self):
        return str(uuid.uuid4())
    

    def __repr__(self):
        return f"<Character: {self.full_name}>"
    













#ADD THIS
# creating our Schema class (Schema essentially just means what our data "looks" like, and our 
# data needs to look like a dictionary (json) not an object)


class ProductSchema(ma.Schema):

    class Meta:
        fields = ['character_id', 'first_name', 'last_name', 'full_name', 'title', 'family', 'image', 'description']

    
#instantiate our ProductSchema class so we can use them in our application
product_schema = ProductSchema() #this is 1 singular product
products_schema = ProductSchema(many=True) #bringing back all the products in our database & sending to frontend


