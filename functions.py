import smtplib,os
from dotenv import load_dotenv

load_dotenv()
def send_mail(user_mail,msg,name,surname):
    my_mail = os.environ.get('my_mail')
    my_receiver_mail=os.environ.get('receiver_mail')
    password = os.environ.get('password')

    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(user=my_mail,password=password)
        connection.sendmail(from_addr=my_mail,
                            to_addrs=my_receiver_mail,
                            msg=f"Subject:YummyFood Feedback\n\n"
                                f"{msg}\n\n"
                                f"Full Name : {name} {surname}\n"
                                f"User's Mail Address {user_mail}")
