from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from models.Users import UserLogin
from flask_login import login_user
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def login(dbase,session):
    session.clear()
    if request.method == 'POST':
        global user
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            if user['isAdmin'] == True:
                return redirect((url_for('admin')))
            else:
                return redirect(url_for('home'))


        flash('Incorrect email or password')
    return render_template('signin.html')