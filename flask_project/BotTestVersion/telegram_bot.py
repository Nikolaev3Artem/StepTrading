from telethon import TelegramClient, sync,events
import sqlite3
import re
import asyncio
import threading

# Вставляем api_id и api_hash
api_id = 16113440
api_hash = '946119821f3bb097cd7ee44dd9d70ea8'

client = TelegramClient('telegram_parser', api_id, api_hash)   

from binance_parser_bot import run_order

client.connect()
client.start()

print("Connection success")
#создаем событие при получение нового сообщения
@client.on(events.NewMessage(chats='Binance'))
async def normal_handler(event):
    conn = sqlite3.connect('Steps.db')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS coin_info(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DATE TEXT,
    COIN TEXT,
    PAIR TEXT,
    BUY INTEGER,
    TARGET_1 INTEGER,
    TARGET_2 INTEGER,
    TARGET_3 INTEGER,
    TARGET_4 INTEGER,
    SL INTEGER,
    ACTIVE BOOLEAN,
    ARCHIVE BOOLEAN
    );
    """)
    conn.commit()


    orig_user_msg = ''
    orig_user_msg = event.message.to_dict()['message']
    orig_user_datetime = event.message.to_dict()['date']
    orig_user_msg = orig_user_msg.lower()
    words = orig_user_msg.split() 
    words = [word.strip('.,!;()[]') for word in words]
    text = ''

    for word in words:
        text += ' '+word
    try:
        keyword = re.findall(r"\d\d*",text)
    except:
       print("Error")

    coin = words[0].lstrip("#").upper()
    buy = keyword[1]
    target_1 = keyword[2]
    target_2 = keyword[4]
    target_3 = keyword[6]
    target_4 = keyword[8]
    sl = int(buy) - (int(buy) * 0.05)
    sl = int(sl)
    coin_pair = coin + "/BTC"
    active = True
    archieve = False
    print(words)

    msg = "Coin: "+coin+"\n"+"Buy: "+buy+"\n"+"target_1: "+target_1+"\n"+"target_2: "+target_2+"\n"+"Stop Lose: " + str(sl)

    data = [orig_user_datetime,coin,coin_pair,buy,target_1,target_2,target_3,target_4,sl,active,archieve]
    cur.execute("""INSERT INTO coin_info (DATE,COIN,PAIR,BUY,TARGET_1,TARGET_2,TARGET_3,TARGET_4,SL,ACTIVE,ARCHIVE) VALUES(?,?,?,?,?,?,?,?,?,?,?);""",data)

    conn.commit()
    conn.close()
    await client.send_message('bottest17174',''+msg)
    run_order()


client.run_until_disconnected()
