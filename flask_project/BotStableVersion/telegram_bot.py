from telethon import TelegramClient, sync,events
import sqlite3
from binance_parser_bot import run_order

api_id = 16113440
api_hash = '946119821f3bb097cd7ee44dd9d70ea8'
#api_id = 10160782
#api_hash = '1cab37704561bed382e3668af70c4a84'

client = TelegramClient('telegram_parser', api_id, api_hash) 

client.connect()
client.start()

print("Connection success")
#создаем событие при получение нового сообщения
@client.on(events.NewMessage(chats='HIRN PREMIUM ALTS'))
async def normal_handler(event):
    conn = sqlite3.connect('Steps.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS coin_info(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DATE TEXT,
    COIN TEXT,
    PAIR TEXT,
    BUY INTEGER,
    SELL INTEGER,
    PROFIT INTEGER,
    ACTIVE BOOLEAN,
    ARCHIVE BOOLEAN
    );
    """)
    conn.commit()

    orig_user_msg = ''
    orig_user_msg = event.message.to_dict()['message']
    orig_user_datetime = event.message.to_dict()['date']
    orig_user_datetime = orig_user_datetime.strftime("%Y/%m/%d, %H:%M")
    orig_user_msg = orig_user_msg.lower()
    words = orig_user_msg.split() 
    words = [word.strip('.,!;()[]') for word in words]
    text = ''

    coin_pair = words[2].lstrip('#')
    coin = ''
    buy = float(words[6])
    sell = float(words[10])
    buy = '{:.8f}'.format(buy)
    sell = '{:.8f}'.format(sell)
    active = True
    archieve = False
    for i in coin_pair:
        coin += i
        if i == '/':
            break

    coin = coin.rstrip('/')
    print(coin_pair,buy,sell,coin)
    
    
    
    profit = 0
    data = [orig_user_datetime[0:18],coin,coin_pair,buy,sell,profit,active,archieve]
    cur.execute("""INSERT INTO coin_info (DATE,COIN,PAIR,BUY,SELL,PROFIT,ACTIVE,ARCHIVE) VALUES(?,?,?,?,?,?,?,?);""",data)
    msg = ("Coin: "+coin+"\n"+"Coin Pair: " + coin_pair + "\n" + "Buy: " + buy +"\n" + "Sell:" + sell + "\n")
    
    #await client.send_message('TestOrdersRequest',''+msg)
    #await client.send_message('bottest17174',''+msg)

    conn.commit()
    conn.close()
    run_order()

client.run_until_disconnected()