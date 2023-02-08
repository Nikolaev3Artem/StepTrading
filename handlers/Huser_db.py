from flask import render_template

def user_db(dbase, session):
    user = dbase.getUser(session['_user_id'])
    users = dbase.getUsers()
    if user['isAdmin']:
        return render_template('user_db.html', users = users,balance = user['balance'])
    else:
        return render_template('error-page.html')