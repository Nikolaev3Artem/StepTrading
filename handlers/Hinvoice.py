from flask import render_template

def invoice(dbase,session):
    user = dbase.getUser(session['_user_id'])
    return render_template('invoice.html',username=user['username'],email = user['email'],balance = user['balance'])
