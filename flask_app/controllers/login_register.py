from flask_app import app
from flask import render_template, redirect, session, request,flash
from flask_app.models.users import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.register(data)
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():

    users = User.check_database_for_email_by_email(request.form)
    if len(users) == 0:
        flash("That email doesn't exist")
        return redirect('/')

    user = users[0]

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password is incorrect')
        return redirect('/')

    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')