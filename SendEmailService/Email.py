from email.message import EmailMessage
import smtplib
from email.mime.text import MIMEText

from users.generatedID import UserId


class SendEmail:
    confirmation_code = UserId.generaterandom()

    def send_email(self):
        # important, you need to send it to a server that knows how to send e-mails for you
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # don't know how to do it without cleartexting the password and not relying on some json file that you dont git
        # control...
        server.login('waterloobanking@gmail.com', 'wlqsupewdaubsbjy')
        msg = EmailMessage()
        return msg, server

    def accountcreation(self, destination, firstname):
        msg, server = email.send_email()
        message = """Hello {0} , Thanks for opening an account with us. We hope you enjoy your banking experience. 
        Please click on this link <a href ="http://127.0.0.1:4100/confirmation/{1}/{2}">click here</a> to confirm 
        your account to confirm your email in the console. Thanks, WaterlooBank""".format(firstname, destination,
                                                                                          email.confirmation_code)

        msg = MIMEText(message, 'html')

        msg['Subject'] = 'Congratulations on Successfully opening an account'
        msg['From'] = 'waterloobanking@gmail.com'
        msg['To'] = destination
        server.send_message(msg)
        return True

    def deposit(self, destination, amount, firstname, sender):
        msg, server = email.send_email()
        message = """Hi {0}, the sum of {1} has been deposited into your account by {2}. Please <a 
        href="http://127.0.0.1:4100/login">click here</a> here to login and check your updated account balance""".format(
            firstname, amount, sender)

        msg = MIMEText(message, 'html')
        msg['Subject'] = 'Successful Deposit'
        msg['From'] = 'waterloobanking@gmail.com'
        msg['To'] = destination
        server.send_message(msg)
        return True

    def transfer(self, firstname, amount, destination, transferfirstname):
        msg, server = email.send_email()
        message = """Hi {0}, You have successfully transferred the sum of {1} to {2}.Please <a 
        href="http://127.0.0.1:4100/login">click here</a> here to login and check your updated account balance""".format(
            firstname, amount, transferfirstname)

        msg = MIMEText(message, 'html')
        msg['Subject'] = 'Successful Deposit'
        msg['From'] = 'waterloobanking@gmail.com'
        msg['To'] = destination
        server.send_message(msg)
        return True


email = SendEmail()
# email.accountcreation("tebere.chukwuka@gmail.com", "Jason")
# print(email.confirmation_code)
# email.accountcreation("thomasebere119@gmail.com", "James")
