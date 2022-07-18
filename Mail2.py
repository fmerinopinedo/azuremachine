import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "merinogrepolis@gmail.com"  # Enter your address
receiver_email = "fernando.merino@servexternos.gruposantander.com"  # Enter receiver address
password = "qbeeiuvtsqbrzmuu"
message = """\
Subject: Hi there

This message is sent from Python. Prueba"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)