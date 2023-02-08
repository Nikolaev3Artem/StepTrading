from flask import render_template

def profile(dbase, session):
    user = dbase.getUser(session['_user_id'])
    return render_template('profile.html',username=user['username'],email=user['email'],balance = user['balance'], fullname = user['name'], btcvallet = 'Nein')
