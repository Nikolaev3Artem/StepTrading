from flask import request, render_template, flash, redirect, url_for
from models import FDataBase

def recover_pass(dbase,user_id):
    if request.method == 'POST':
        password1 = request.form['password1']
        password2 = request.form['password2']
        if password1 != password2:
            flash("Password must match")
        elif len(password1) <= 4:
            flash("Password must be longer than 4")
        else:
            if FDataBase.swap_pass(password1,user_id):
                return redirect(url_for('login'))
        

    return render_template('recover_pass.html')