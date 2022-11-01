import sqlite3
from binance import Client
import time
import datetime
import math
from binance import AsyncClient, BinanceSocketManager
from buy_sell_order import buy_sell_order
from binance.exceptions import BinanceAPIException, BinanceOrderException





api_key = '1nCiyrKWXGzQ4HFMGd3a69iYA2NBJFZz2aed7vzcvYHYpBq4pxR90fFigi0OIyjS'
api_secret = 'gelaomfSv0SrMGrRewcNpUbVO32XlmGYcja5shVeJX0n15OudKO7s58usWQGwqNK'
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


    base_currency = coin_list[len(coin_list)-1][2]
    quote_currency = 'BTC'
    pair = base_currency + quote_currency

    base_buy_price = coin_list[len(coin_list)-1][4]+2
    base_sell_price = coin_list[len(coin_list)-1][5]
    base_sl_price = coin_list[len(coin_list)-1][9]

    pair_price = client.get_symbol_ticker(symbol=pair)['price']

    pair_price = pair_price.lstrip('0')
    pair_price = str(pair_price)
    z=0

    for i in range(len(pair_price)):
        if pair_price[i] == '0':
            z+=1
        elif pair_price[i] == '.':
            continue
        elif int(pair_price[i]) > 0:
            break

    base_buy_price = '0.' + (z*'0') + str(base_buy_price)
    base_sell_price = '0.' + (z*'0') + str(base_sell_price)
    base_sl_price = '0.' + (z*'0') + str(base_sl_price)

    print(f'Coin: {base_currency} | Pair: {pair} | Buy price: {base_buy_price} | Sell price: {base_sell_price} | Sl price: {base_sl_price}')
    print('-----------------------------------------------')
    pair_price = float(client.get_symbol_ticker(symbol=pair)['price'])
    
    

    try:
        free_quote_currency = float(client.get_asset_balance(asset='BTC')['free'])
        coins_amount = free_quote_currency/float(base_buy_price)
        coin_amount = int(0.99 * (float(coins_amount)))
        coin_amount = int(coin_amount/2)
        print(float(base_buy_price))
        buy_sell_order(client, symbol=pair,side='BUY', quantity=coin_amount, price=base_buy_price)
    except BinanceAPIException as e:
        print(e)

    while True:
        coin_amount_bought = round(float(client.get_asset_balance(asset=base_currency)['free']))
        if coin_amount_bought == coin_amount:
            buy_sell_order(client, pair, 'SELL', coin_amount_bought, base_sell_price)
            break

        elif pair_price == base_sl_price:
            i=0
            try:
                while i <= len(client.get_all_orders(symbol=pair)):
                    if client.get_all_orders(symbol=pair)[i]['status'] == 'NEW':
                        all_orders = client.get_all_orders(symbol=pair)[i]
                        oID = all_orders['orderId']
                        cOrderId = all_orders['clientOrderId']
                        cancel_last_order(client,symbol=pair,orderId=oID)
                    i+=1
            except:
                pass
            break
        else:
            strip = '-------------------------------------------------------'
            print(f'{datetime.datetime.now()}\nCoin amount on your balance: {coin_amount_bought} waiting for {base_buy_price}\n{strip}')
        time.sleep(2)
    cursor.close()
    conn.close()