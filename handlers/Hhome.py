from flask import render_template

def home(dbase, session): 
    user = dbase.getUser(session['_user_id'])
    coin_list = dbase.getCoin()
    coin_name = coin_list[len(coin_list)-1][2]
    coin = dbase.getCoin()
    last_coin_id = coin_list[len(coin_list)-1][0]
    coin.reverse()
    result_profit = 0
    AllProfit = float()
    for onecoin in coin:
        if onecoin['profit'] != None:
            AllProfit += onecoin['profit']
    
    
    user_count = 0

    return render_template('home.html',
    username=user['username'],
    coin=coin_name,
    balance = user['balance'], 
    coins = coin[0:10],
    count_id = int(last_coin_id/2),
    Profit = AllProfit,
    user_count = user_count
    )