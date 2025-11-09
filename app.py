# app.py
from flask import Flask, render_template,session,redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


# ---- CONFIG ----
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:Aaronica@localhost:5432/plp'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'A_VERY_SECRET_KEY_USED_TO_SIGN_SESSIONS_12345'

# Initialize SQLAlchemy
db = SQLAlchemy(app)
app.db = db

# Import model factory
from location import locationmodel
from main_item import main_item
from user_model import create_user_model as main_user
from amount_model import amount_model

# Create the Location model
LocationModel = locationmodel(db.Model)
ItemModel = main_item(db.Model)
User = main_user(db.Model)
Amount1= amount_model(db.Model)
# Import routes

from login import login_bp,register_users_model
from routes import location_bp, register_location_model
from item_route import main_item, register_item_model
from user_route import user_bp, register_user_model
from amount_route import amount_bp, register_amount_model
from get_location import get_location, register_get_location_model
from delete_location import delete_location_bp, delete_location_model
from delete_item import delete_item_bp, delete_item_model
from get_amount import get_amount_bp, register_get_amount_model 
from get_user import user_details_bp,register_user_details_model
from get_names import email_bp,register_email_model
from delet_user import delete_user_bp,delete_user_model


# Register the model with routes
register_location_model(LocationModel)
register_item_model(ItemModel)
register_user_model(User)
register_users_model(User)
register_amount_model(LocationModel, ItemModel,Amount1)
register_location_model(LocationModel)
register_get_location_model(LocationModel)
delete_location_model(LocationModel)
delete_item_model(ItemModel)
register_get_amount_model(Amount1)
register_user_details_model(User)
register_email_model(User)
delete_user_model(User)

# Register blueprint
app.register_blueprint(location_bp)
app.register_blueprint(main_item)
app.register_blueprint(user_bp)
app.register_blueprint(login_bp)
app.register_blueprint(amount_bp)
app.register_blueprint(get_location)
app.register_blueprint(delete_location_bp)
app.register_blueprint(delete_item_bp)
app.register_blueprint(get_amount_bp)
app.register_blueprint(user_details_bp)
app.register_blueprint(email_bp)
app.register_blueprint(delete_user_bp)


# Home route
@app.route('/')
def index():
    # Check if user is logged in via server-side session
        if 'user_id' in session:
            # If logged in, redirect to the main content page
            return render_template('dashboard.html')
        else:
            # If not logged in, render the login page
            return render_template('login1.html')
    

@app.route('/locations_page')
def locations_page():
    # Protect route: Check if user is logged in
    if 'user_id' not in session:
        return redirect('/')
    else:
      return  render_template('index.html')

@app.route('/item_page')
def item_page():
    # Protect route: Check if user is logged in
    if 'user_id' not in session:
        return redirect('/')
    else:
        return render_template('item.html')

@app.route('/statistics_page')
def statistics_page():
    # Protect route: Check if user is logged in
    if 'user_id' not in session:
        return redirect('/')
    else:
        return render_template('get_amount.html') 
# Create tables
with app.app_context():
    db.create_all()

@app.route('/register')
def users():
    return render_template('users.html')

@app.route('/back')
def back():
    return render_template('login1.html')


if __name__ == '__main__':
    app.run(debug=True)