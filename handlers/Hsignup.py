from flask import render_template, url_for, flash, redirect , request
from werkzeug.security import generate_password_hash

def signup(dbase):
    if request.method == 'POST':
        res = False
        balance = '0'
        if len(request.form['username']) > 4 and len(request.form['email']) > 4 and len(request.form['password']) > 4 and request.form['password'] == request.form['password2']:
            hash = generate_password_hash(request.form['password'])
            res = dbase.addUser(username = request.form['username'],balance = balance,email = request.form['email'],hpsw = hash,isAdmin = False)
        elif len(request.form['username']) < 4:
            flash('Username must be more than 4 characters')
        elif len(request.form['email']) < 4:
            flash('Email must be more than 4 characters')
        elif len(request.form['password']) < 4:
            flash('Password must be more than 4 characters')
        elif request.form['password'] != request.form['password2']:
            flash('Passwords do not match')
        elif request.form['email'] == dbase.getUserByEmail(request.form['email']):
            flash('User with this email already exists')
        if res:
            return redirect(url_for('login'))

    return render_template('signup.html')