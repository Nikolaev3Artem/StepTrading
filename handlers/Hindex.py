from flask import render_template

def index_data(dbase):  
    coin_list = dbase.getCoin()
    coin_name = coin_list[len(coin_list)-1][3]
    last_coin_id = coin_list[len(coin_list)-1][0]
    coin = dbase.getCoin()
    coin.reverse()
    return render_template('index.html',
    coin = coin_name , 
    coins = coin[0:10],
    count_id = int(last_coin_id/2))
