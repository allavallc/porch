import smtplib, ssl
import os

class sendSMS():

    def __init__(self, port = 587, smtp_server = "smtp.gmail.com", sender_email = "adefilippo@gmail.com", receiver_email = "7133043238@txt.att.net",
                 password= os.environ["PASSWORD"], message = "A person walked by...", context = ssl.create_default_context()):
        self.port = port  # For starttls
        self.smtp_server = smtp_server
        self.sender_email = sender_email
        # receiver_email = "adefilippo@gmail.com"
        self.receiver_email = receiver_email
        # password = input("Type your password and press enter:")
        self.password = password
        self.message = message
        self.context = context

    def sendIt(self):
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=self.context)
            server.ehlo()  # Can be omitted
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, self.message)

def main():
    # port = 587  # For starttls
    # smtp_server = "smtp.gmail.com"
    # sender_email = "adefilippo@gmail.com"
    # # receiver_email = "adefilippo@gmail.com"
    # receiver_email = "7133043238@txt.att.net"
    # # password = input("Type your password and press enter:")
    # password = 'Ilovemuffsalot'
    # message = "Subject here..."
    # context = ssl.create_default_context()

    newText = sendSMS()
    newText.sendIt()

# the below says that if we are running the below alone it will just run the main function
if __name__ == "__main__":
    main()