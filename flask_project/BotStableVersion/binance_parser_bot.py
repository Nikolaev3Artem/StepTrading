import sqlite3
from binance import Client
import time
import datetime
import math
from binance import AsyncClient, BinanceSocketManager
from buy_sell_market import buy_sell_market
from buy_sell_limit import buy_sell_limit
from binance.exceptions import BinanceAPIException, BinanceOrderException




api_key = 'BMDCLx1D0I3tpgKXr12oXVvabAsV5LHesm2vM1XViUSQ0qeh3ulYcbLroso3z37V'
api_secret = 'LpBFHz4DjVNRm5BvFPXsjLqaE5LleSVbfbQamQ817ubQGtyogBkIdUpvmf523zLM'
#api_key = '1nCiyrKWXGzQ4HFMGd3a69iYA2NBJFZz2aed7vzcvYHYpBq4pxR90fFigi0OIyjS'
#api_secret = 'gelaomfSv0SrMGrRewcNpUbVO32XlmGYcja5shVeJX0n15OudKO7s58usWQGwqNK'
client = Client(api_key, api_secret)

def run_order():
    conn = sqlite3.connect('Steps.db')
    cursor = conn.cursor()
    sql_select_query = """SELECT * from coin_info"""
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    coin_list = []
    
    for row in records:
        coin_list.append(row)


    base_currency = coin_list[len(coin_list)-1][2].upper()
    quote_currency = 'BTC'
    pair = base_currency + quote_currency

    base_buy_price = coin_list[len(coin_list)-1][4]
    base_sell_price = coin_list[len(coin_list)-1][5]

    base_buy_price = '{:.8f}'.format(base_buy_price)
    base_sell_price = '{:.8f}'.format(base_sell_price)

    pair_price = client.get_symbol_ticker(symbol=pair)['price']

    pair_price = str(pair_price)

    print(f'Coin: {base_currency} | Pair: {pair} | Buy price: {base_buy_price} | Sell price: {base_sell_price}')
    print('-----------------------------------------------')
    pair_price = float(client.get_symbol_ticker(symbol=pair)['price'])
    

    try:
        free_quote_currency = float(client.get_asset_balance(asset='BTC')['free'])
        coins_amount = free_quote_currency/float(base_buy_price)
        coin_amount = int(0.99 * (float(coins_amount)))
        coin_amount = int(coin_amount/2)
        #if pair_price - float(base_sell_price) >= 3:
        buy_sell_market(client, symbol=pair,side='BUY', quantity=coin_amount)
    except BinanceAPIException as e:
        print(e)

    while True:
        coin_amount_bought = round(float(client.get_asset_balance(asset=base_currency)['free']))
        if coin_amount_bought >= coin_amount:
            buy_sell_limit(client, pair, 'SELL', coin_amount, base_sell_price)
            break
        elif buy==False:
            print('waiting for the next coin')
            break

        #elif pair_price == base_sl_price:
        #    i=0
        #    try:
        #        while i <= len(client.get_all_orders(symbol=pair)):
        #            if client.get_all_orders(symbol=pair)[i]['status'] == 'NEW':
        #                all_orders = client.get_all_orders(symbol=pair)[i]
        #                oID = all_orders['orderId']
        #                cOrderId = all_orders['clientOrderId']
        #                cancel_last_order(client,symbol=pair,orderId=oID)
        #            i+=1
        #    except:
        #        pass
        #    break
    with open(f"Coins/{base_currency}-{date}.txt", "w") as f:
        f.write("Buy: " + str('{:.8f}'.format(pair_price)) + "\n" + "Sell: " + str(base_sell_price) + "\n") 

    cursor.close()
    conn.close()