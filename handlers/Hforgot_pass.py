from flask import request, render_template, flash

def forgot_pass(dbase):
    if request.method == 'POST':
        if dbase.getUserByEmail(request.form['email']):
            flash('Проверьте вашу почту')
        else:
            flash('Пользователя с таким емейл не найдено')
    
    return render_template('forgot-password.html')