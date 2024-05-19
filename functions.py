import smtplib,os

def send_mail(user_mail,msg,name,surname):
    my_mail = os.environ.get('my_mail')
    my_receiver_mail=os.environ.get('receiver_mail')
    password = os.environ.get('password')
    #password = "kgumezrjsjnysscv"

    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(user=my_mail,password=password)
        connection.sendmail(from_addr=my_mail,
                            to_addrs=my_receiver_mail,
                            msg=f"Subject:YummyFood Feedback\n\n"
                                f"{msg}\n\n"
                                f"{name} {surname}\n"
                                f"{user_mail}")
