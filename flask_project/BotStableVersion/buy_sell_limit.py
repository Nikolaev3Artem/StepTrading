def buy_sell_limit(client,symbol,side,quantity,price):
    order = client.create_order(
        symbol=symbol,
        side=side ,
        type='LIMIT',
        timeInForce = 'GTC',
        quantity=round(quantity),
        price = price)
    return order