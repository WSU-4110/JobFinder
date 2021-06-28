# All Routing will be done here

# Import Dependecies for Validation, Authorization and routing
from flask import Blueprint
from flask import render_template, redirect
from flask import url_for, request
from flask import flash
from werkzeug.security import generate_password_hash 
from werkzeug.security import check_password_hash
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from .models import User
from .import db



Routing = Blueprint('Routing', __name__)



# Landing page when server starts running
@Routing.route('/')
def Welcome():
    return render_template('Welcome.html')

@Routing.route('/Home')
def Home():
    return render_template('Home.html')

#Routing for Users to Login to use platform
@Routing.route('/Login')
def Login():
    return render_template('Login.html')

@Routing.route('/Login', methods=['POST'])
def Get_Login_Up():

    Get_Email = request.form.get('email')
    Get_Password = request.form.get('password')
    Set_Remember = True if request.form.get('remember') else False



    Website_User = User.query.filter_by(email=Get_Email).first()

    #Validate Password, and check if the user data is in database
    if not Website_User or not check_password_hash(Website_User.password, Get_Password):
        flash('Check login information')
        return redirect(url_for('Routing.Login'))


    login_user(Website_User, remember=Set_Remember)
    return redirect(url_for('Routing.Home'))




#Routing for Users to signup to use platform
@Routing.route('/Signup')
def Signup():
    return render_template('Signup.html')

#We want to create a function that takes all the user information on the website (e.g: password) and encrpyt it and store in the database
@Routing.route('/Signup', methods=['POST'])
def Get_Sign_Up():

    Get_Email = request.form.get('email')
    Get_Name = request.form.get('name')
    Get_Password = request.form.get('password')

    Website_User = User.query.filter_by(email=Get_Email).first()


    # If user is already in in database re-route back to signup to re-attempt
    if Website_User:
        flash('Email address already exists') # Flag a error message when a user is not logged in
        return redirect(url_for('Routing.Signup'))

    # If no user in database, procedd to get all email and password data, also hash password before storing
    Website_New_User = User(email=Get_Email, name=Get_Name, password=generate_password_hash(Get_Password, method='sha256'))

# Storing New user in database, first we query the databse id to see if data already exist, if it doesn't we get the new data and store
    db.session.add(Website_New_User)
    db.session.commit()

# Upon successful sign-up, route to login so users can login using their credentials
    return redirect(url_for('Routing.Login'))


#ROuting for Attractions
@Routing.route('/Attractions')
def Attractions():
    return render_template('Attractions.html')

#Routing for Events
@Routing.route('/Events')
def Events():
    return render_template('Events.html')

@Routing.route('/Food')
def Food():
    return render_template('Food.html')

@Routing.route('/AboutUs')
def AboutUs():
    return render_template('AboutUs.html')

# ROuting for Users to view their profile
# We should also show the users information on this page so they know they are currently logged in
from flask_login import current_user
@Routing.route('/Profile')
def Profile():
    return render_template('Profile.html', name = current_user.name, email = current_user.email)


# Routing for Users loging out of platform
@Routing.route('/Logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('Routing.Welcome'))

