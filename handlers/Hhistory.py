from flask import render_template

def history(dbase):
    transactions = dbase.getUsers()
    return render_template('history.html', transactions = transactions)