from flask import render_template

def index_data(dbase):  
    user_count = dbase.getUsers()
    user_count = user_count[-1][0]
        
    coin_list = dbase.getCoin()

    coin_name = coin_list[len(coin_list)-1][3]
    last_coin_id = coin_list[len(coin_list)-1][0]

    coin_list.reverse()

    AllProfit = float()
    for onecoin in coin_list:
        if onecoin['profit'] != None:
            AllProfit += onecoin['profit']
    return render_template('index.html',
    coin = coin_name, 
    coins = coin_list[0:10],
    count_id = int(last_coin_id),
    Profit = AllProfit,
    user_count = user_count
    )
