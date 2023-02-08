from flask import render_template

def strategy(dbase, session):
    user = dbase.getUser(session['_user_id'])
    coin_list = dbase.getCoin()
    coin_name = coin_list[len(coin_list)-1][2]
    return render_template('strategy.html',coin = coin_name,balance = user['balance'])
