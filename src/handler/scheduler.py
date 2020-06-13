"""Implementation of the mail scheduler."""
from src.handler.visualisation import visualisation
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from src.utils import conf
import os
import schedule
import time
import yaml
from src.utils.constants import YAMLPATH
stream = open(YAMLPATH, 'r')
data = yaml.load(stream)
subject = data['subject']
sender = data['sender']
receiver = data['receiver']
sender_password = data['sender_password']
server = data['server']


class scheduler:
    def mail_scheduler(self):
        """
        Implementation of the mail scheduler.
        """
        visualisation(self)
        print("Mail sent")
        img_data = open('./src/graphs/plot.png', 'rb').read()

        Port = 587
        Server = conf.server

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver
        UserName = sender
        UserPassword = sender_password
        text = MIMEText("Plot showing number of booking versus date ---- From Team cab9leaps")
        msg.attach(text)
        image = MIMEImage(img_data, name=os.path.basename('./src/graphs/plot.png'))
        msg.attach(image)
        s = smtplib.SMTP(Server, Port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(UserName, UserPassword)
        s.sendmail(msg['From'], msg['To'], msg.as_string())

    def main(self):
        """
        Function to send the mails.
        """
        schedule.every(1).minutes.do(scheduler().mail_scheduler)

        while True:
            schedule.run_pending()
            time.sleep(1)


scheduler().main()
