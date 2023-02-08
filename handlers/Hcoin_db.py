from flask import render_template

def coin_db(dbase, session):
    user = dbase.getUser(session['_user_id'])
    coin = dbase.getCoin()
    if user['isAdmin']:
        return render_template('coin_db.html', coins = coin,balance = user['balance'])
    else:
        return render_template('error-page.html' )