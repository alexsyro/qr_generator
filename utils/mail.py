from django.core import mail


class Email:
    '''This class sends emails and prints info to celery or django console'''

    def __init__(self, email_adress, content) -> None:
        self.connection = mail.get_connection()
        self.email_adress = email_adress
        self.content = content

    def send(self):
        self.connection.open()
        email = mail.EmailMessage(
            'You zip with QR codes is ready',
            self.content,
            'from@qrgenerator.com',
            [self.email_adress],
            connection=self.connection,
        )
        self.connection.send_messages([email])
        self.connection.close()
