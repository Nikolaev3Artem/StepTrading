from flask import request, render_template, flash
from scripts.gmail import send_mail
from dotenv import load_dotenv, find_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from bs4 import BeautifulSoup as bs

load_dotenv(find_dotenv())

def forgot_pass(dbase):
    if request.method == 'POST':
        if dbase.getUserByEmail(request.form['email']):
            msg = MIMEMultipart("alternative")
            msg["From"] = os.getenv('email')
            msg["To"] = request.form['email']
            msg["Subject"] = "StepTrading.online Password recovery"

            html = """
            <h1>We have an request from your account for password recovery</h1><br>
            <h1>Here are a link that you can use to recover your password</h1><br>
            http://127.0.0.1:5000/recover-password
            <h1>If it was not you please don`t use this link</h1><br>
            """
            text = bs(html, "html.parser").text

            text_part = MIMEText(text, "plain")
            html_part = MIMEText(html, "html")
            msg.attach(text_part)
            msg.attach(html_part)
            send_mail(os.getenv('email'), os.getenv('password'), os.getenv('email'), request.form['email'], msg)
            flash('Проверьте вашу почту')
    
    return render_template('forgot-password.html')