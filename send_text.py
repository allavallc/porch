import smtplib, ssl
from decouple import config

class sendSMS():

    def __init__(self, port = config('PORT'), smtp_server = "smtp.gmail.com", sender_email = config('USER_EMAIL'), receiver_email = config('PHONE') + config('ATT_EMAIL_TO_TEXT'),
                 password = config('PASSWORD'), message = "A person walked by...", context = ssl.create_default_context()):
        self.port = port  # For starttls
        self.smtp_server = smtp_server
        self.sender_email = sender_email
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

    newText = sendSMS()
    newText.sendIt()

# the below says that if we are running the below alone it will just run the main function
if __name__ == "__main__":
    main()