def buy_sell_market(client,symbol,side,quantity):
    order = client.create_order(
        symbol=symbol,
        side=side ,
        type='MARKET',
        quantity=round(quantity))
    return order