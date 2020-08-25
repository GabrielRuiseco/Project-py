# Doorbell pin
DOORBELL_PIN = 21
# Enables email notifications
ENABLE_EMAIL = True
# Email you want to send the notification from (only works with gmail)
FROM_EMAIL = 'gabriel.ruiseco.utt@gmail.com'
# You can generate an app password here to avoid storing your password in plain text
# this should also come from an environment variable
# https://support.google.com/accounts/answer/185833?hl=en
FROM_EMAIL_PASSWORD = 'ygepfbvmhpqxuyaa'
# Email you want to send the update to
TO_EMAIL = '19170012@utt.edu.com'

#############
# Program
#############

import time
import Ultrasonic
import mongodb
import pymongo
import bson
import os
import signal
import subprocess
import smtplib
import uuid

mCon = mongodb.MongoConect()
DB = mCon.CLIENT['adonismongo']
directorios = DB['directorios']

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO. This is probably because you need superuser. Try running again with 'sudo'.")


class NewObject:
    def __init__(self, _id, fileName, imgsrc_route, idu):
        self._id = _id
        self.fileName = fileName
        self.imgsrc_route = imgsrc_route
        self.idu = idu


def save_new_object():
    id = bson.objectid.ObjectId()
    name = str(id)
    imgsr = name + ".jpg"
    idu = 1
    o = NewObject(id, name, imgsr, idu)
    mongodb.MongoConect.create(mCon, directorios, o.__dict__)


def send_email_notification():
    if ENABLE_EMAIL:
        sender = EmailSender(FROM_EMAIL, FROM_EMAIL_PASSWORD)
        email = Email(
            sender,
            'Video Doorbell',
            'Notification: A visitor is waiting',
            'A new visitant is added to your gallery'
        )
        email.send(TO_EMAIL)


def ring_doorbell(pin):
    send_email_notification()
    save_new_object()


class EmailSender:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class Email:
    def __init__(self, sender, subject, preamble, body):
        self.sender = sender
        self.subject = subject
        self.preamble = preamble
        self.body = body

    def send(self, to_email):
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = self.subject
        msgRoot['From'] = self.sender.email
        msgRoot['To'] = to_email
        msgRoot.preamble = self.preamble

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        msgText = MIMEText(self.body)
        msgAlternative.attach(msgText)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(self.sender.email, self.sender.password)
        smtp.sendmail(self.sender.email, to_email, msgRoot.as_string())
        smtp.quit()


class Doorbell:
    def __init__(self, doorbell_button_pin):
        self._doorbell_button_pin = doorbell_button_pin

    def run(self):
        try:
            print("Starting Doorbell...")
            self._setup_gpio()
            print("Waiting for doorbell rings...")
            self._wait_forever()

        except KeyboardInterrupt:
            print("Safely shutting down...")

        finally:
            self._cleanup()

    def _wait_forever(self):
        while True:
            time.sleep(0.1)

    def _setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._doorbell_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self._doorbell_button_pin, GPIO.RISING, callback=ring_doorbell, bouncetime=2000)

    def _cleanup(self):
        GPIO.cleanup(self._doorbell_button_pin)


if __name__ == "__main__":
    doorbell = Doorbell(DOORBELL_PIN)
    doorbell.run()
    try:
        while True:
            dist = Ultrasonic.distance
            print("Measured Distance = %.1f cm" % dist)
            if dist < 5:
                ring_doorbell(DOORBELL_PIN)
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

