

def cancel_last_order(client,symbol,orderId):
    client.cancel_order(
        symbol=symbol,
        orderId=int(orderId)
    )