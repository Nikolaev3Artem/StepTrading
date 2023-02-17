from flask import render_template

def home(dbase, session): 
    user = dbase.getUser(session['_user_id'])
    user_count = dbase.getUsers()
    user_count = user_count[-1][0]
    coin_list = dbase.getCoin()
    coin_name = coin_list[-1][2]
    last_coin_id = coin_list[-1][0]
    coin_list.reverse()
    result_profit = 0
    AllProfit = float()
    for onecoin in coin_list:
        if onecoin['profit'] != None:
            AllProfit += onecoin['profit']
    
    return render_template('home.html',
    username=user['username'],
    coin=coin_name,
    balance = user['balance'], 
    coins = coin_list[0:10],
    count_id = int(last_coin_id),
    Profit = AllProfit,
    user_count = user_count
    )