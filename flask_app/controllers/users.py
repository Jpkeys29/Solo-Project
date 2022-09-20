from flask import render_template, redirect, request, session,flash
from flask_app import app
from flask_app.models import user
from flask_app.models.user import User
from flask_app.models.stock import Stock

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_route():
    return render_template('login.html')

@app.route('/user/create', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    user_data ={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email':request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
    }
    session['user_id'] = User.create(user_data)
    return redirect('/portfolio')

@app.route('/login', methods=['POST'])
def login():
    #check if the user is in the db based on email in the form(making a call to our class method)
    user_from_db = user.User.get_by_email({'email': request.form['email']}) 
    #if email is in the db check the password from the form to the password for that user in the db
    if user_from_db and bcrypt.check_password_hash(user_from_db.password,request.form['password']):
    #if both the above statement are true I want to log them in( save their id in session)
        session['user_id'] = user_from_db.id 
        return redirect('/portfolio')
    else:
        flash("Invalid email/password", 'login')
        return redirect('/')    


@app.route('/portfolio')
def portfolio():
    if 'user_id' not in session:
        return redirect('/')
    user_diction ={
        'id':session['user_id']
    }
    return render_template('portfolio.html', user=User.get_by_id(user_diction), all_stocks=Stock.get_all_by_trader(user_diction))




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')




