import smtplib

def send_mail(email, password, FROM, TO, msg):
    server = smtplib.SMTP(host="smtp.office365.com", port=587)
    server.starttls()
    server.login(email, password)
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()
    
