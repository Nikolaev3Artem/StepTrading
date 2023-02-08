from flask import render_template
def admin(dbase, session):
    user = dbase.getUser(session['_user_id'])
    coin_list = dbase.getCoin()
    coin_name = coin_list[len(coin_list)-1][2]
    last_coin_id = coin_list[len(coin_list)-1][0]
    coin = dbase.getCoin()
    coin.reverse()
    return render_template('admin/index.html',username=user['username'], coin = coin_name.upper() , coins = coin[0:10],count_id = int(last_coin_id/2))
