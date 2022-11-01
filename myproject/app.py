import sqlite3
import os
from flask import Flask, render_template, url_for, g, flash, abort, redirect , request, session
from werkzeug.security import generate_password_hash, check_password_hash
import time
import math
import re
import datetime
from flask_login import LoginManager , login_user , login_required
from flask_session import Session
from tempfile import mkdtemp
import flask_admin as admin
from flask_admin.contrib.sqla import ModelView
from FDataBase import FDataBase
from UserLogin import UserLogin



DEBUG = True

app = Flask(__name__)

login_manager = LoginManager(app)

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcNCy8hAAAAALXfxtTxotKJdaOSDiH47dkW9WCI'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcNCy8hAAAAAErgcAsRV3SFzwfEn8L__Y7qM78V'
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}
Session(app)


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id,dbase)

#DataBase connect
def connect_db():
    conn = sqlite3.connect("/var/www/steptrading.online/html/flask_project/BotStableVersion/Steps.db")
    #conn = sqlite3.connect("C:/Users/artni/Desktop/Stable/BotStableVersion/Steps.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql',mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

#Managing route

@app.route('/',methods = ['GET','POST'])
def index():
    coin_list = dbase.getCoin()
    coin_name = coin_list[len(coin_list)-1][3]
    last_coin_id = coin_list[len(coin_list)-1][0]
    coin = dbase.getCoin()
    coin.reverse()
    return render_template('index.html',coin = coin_name.upper() , coins = coin[0:10],count_id = int(last_coin_id/2))


@app.route('/home',methods=['GET','POST'])
@login_required
def home():
    coin_list = dbase.getCoin()
    coin_name = coin_list[len(coin_list)-1][3]
    coin = dbase.getCoin()
    last_coin_id = coin_list[len(coin_list)-1][0]
    coin.reverse()
    return render_template('home.html',username=user['username'],coin=coin_name.upper(),balance = user['balance'], coins = coin[0:10],count_id = int(last_coin_id/2))


@app.route('/history', methods = ['GET','POST'])
@login_required
def history():
    transactions = dbase.getUsers()
    return render_template('history.html', transactions = transactions)

@app.route('/login',methods = ['GET','POST'])
def login():
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

@app.route('/settings',methods = ['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')


@app.route('/signup', methods = ['GET','POST'])
def signup():
      
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

        if res:
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/forgot-password', methods = ['GET','POST'])
def forgot_pass():
    if request.method == 'POST':
        if dbase.getUserByEmail(request.form['email']):
            flash('Проверьте вашу почту')
        else:
            flash('Пользователя с таким емейл не найдено')

    return render_template('forgot-password.html')

@app.route('/coin_db', methods = ['GET','POST'])
@login_required
def coin_db():
    user = dbase.getUser(session['_user_id'])
    coin = dbase.getCoin()
    if user['isAdmin']:
        return render_template('coin_db.html', coins = coin,balance = user['balance'])
    else:
        return render_template('error-page.html' )

@app.route('/user_db', methods = ['GET','POST'])
@login_required
def user_db():
    user = dbase.getUser(session['_user_id'])
    users = dbase.getUsers()
    print(user)
    if user['isAdmin']:
        return render_template('user_db.html', users = users,balance = user['balance'])
    else:
        return render_template('error-page.html')

@app.route('/admin', methods = ['GET','POST'])
@login_required
def admin():
    coin_list = dbase.getCoin()
    coin_name = coin_list[len(coin_list)-1][3]
    last_coin_id = coin_list[len(coin_list)-1][0]
    coin = dbase.getCoin()
    coin.reverse()
    return render_template('admin/index.html',username=user['username'], coin = coin_name.upper() , coins = coin[0:10],count_id = int(last_coin_id/2))

@app.route('/invoice',methods = ['GET', 'POST'])
@login_required
def invoice():
    return render_template('invoice.html',username=user['username'],email = user['email'],balance = user['balance'])

@app.route('/strategy',methods=['GET','POST'])
@login_required
def strategy():
    coin_list = dbase.getCoin()
    coin_name = coin_list[len(coin_list)-1][2]
    return render_template('strategy.html',coin = coin_name,balance = user['balance'])

@app.route('/profile',methods = ['GET','POST'])
@login_required
def profile():
    return render_template('profile.html',username=user['username'],email=user['email'],balance = user['balance'])



@app.route("/logout")
@login_required
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'link_db'):
        g.link_db.close()
        
if __name__ == '__main__':
    create_db()
    app.run(debug=True)