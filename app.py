import sqlite3
import os
from flask import Flask, g, session, render_template, redirect, request, url_for
from flask_login import LoginManager , login_required, login_user
from flask_session import Session
from tempfile import mkdtemp
import flask_admin as admin
from models.Users import UserLogin
from models.Coins import Coins
from handlers import Hindex, \
    Hhome, Hhistory, Hlogin, Hsettings, \
    Hsignup, Hforgot_pass, Hcoin_db, Huser_db,\
    Hadmin,Hinvoice, Hstrategy, Hprofile, Hrecover_pass, \
    Hloginbygoogle, Hgooglelogincallback
import os
from dotenv import load_dotenv, find_dotenv
import requests
import json

load_dotenv(find_dotenv())
app = Flask(__name__)
login_manager = LoginManager(app)

app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')
app.config["SESSION_FILE_DIR"] = os.getenv('SESSION_FILE_DIR')
app.config["SESSION_PERMANENT"] = os.getenv('SESSION_PERMANENT')
app.config["SESSION_TYPE"] = os.getenv('SESSION_TYPE')
app.config['FLASK_ADMIN_SWATCH'] = os.getenv('FLASK_ADMIN_SWATCH')
app.config['RECAPTCHA_OPTIONS'] = os.getenv('RECAPTCHA_OPTIONS')
app.config['OAUTHLIB_INSECURE_TRANSPORT'] = os.getenv('OAUTHLIB_INSECURE_TRANSPORT')
DATABASE = os.getenv('DATABASE')
DEBUG = os.getenv('DEBUG')

app.config.from_object(__name__)

Session(app)
user_id = ""

@login_manager.user_loader
def load_user(user_id):
    user_id = user_id
    user = UserLogin().fromDB(user_id,dbase)

    return user

#DataBase connect
def connect_db():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
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
    dbase = Coins(db)

login_manager.login_view = '/login'


#Managing route
@app.route('/',methods = ['GET','POST'])
def index():
    return Hindex.index_data(dbase)


@app.route('/home',methods=['GET','POST'])
def home():
    return Hhome.home(dbase, session)


@app.route('/history', methods = ['GET','POST'])
@login_required
def history():
    return Hhistory.history(dbase)
    
@app.route('/login',methods = ['GET','POST'])
def login():
    return Hlogin.login(dbase,session)

@app.route('/settings',methods = ['GET', 'POST'])
@login_required
def settings():
    return Hsettings.settings()

@app.route('/loginbygoogle',methods = ['GET', 'POST'])
def loginbygoogle():
    return Hloginbygoogle.loginbygoogle()

@app.route('/loginbygoogle/callback',methods = ['GET', 'POST'])
def callback():
    return Hgooglelogincallback.callback(dbase)

@app.route('/signup', methods = ['GET','POST'])
def signup():
    return Hsignup.signup(dbase)

@app.route('/forgot-password', methods = ['GET','POST'])
def forgot_pass():
    return Hforgot_pass.forgot_pass(dbase)

@app.route('/recover-password',methods = ['GET','POST'])
def recover_pass():
    return Hrecover_pass.recover_pass(dbase)

@app.route('/coin_db', methods = ['GET','POST'])
@login_required
def coin_db():
    return Hcoin_db.coin_db(dbase, session)

@app.route('/user_db', methods = ['GET','POST'])
@login_required
def user_db():
    return Huser_db.user_db(dbase, session)

@app.route('/admin', methods = ['GET','POST'])
@login_required
def admin():
    return Hadmin.admin(dbase, session)

@app.route('/invoice',methods = ['GET', 'POST'])
@login_required
def invoice():
    return Hinvoice.invoice(dbase, session)

@app.route('/strategy',methods=['GET','POST'])
@login_required
def strategy():
    return Hstrategy.strategy(dbase, session)

@app.route('/profile',methods = ['GET','POST'])
@login_required
def profile():
    return Hprofile.profile(dbase, session)

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
        
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('error-page.html',title='Page not found'), 404


if __name__ == '__main__':
    app.run(debug=True)
