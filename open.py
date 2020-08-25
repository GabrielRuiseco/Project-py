import time

import digitalio
import board

from Adafruit_IO import Client, Feed, RequestError

ADAFRUIT_IO_KEY = 'aio_tXoj04DOsQ9igwzy9DSWOvyY7n5l'

ADAFRUIT_IO_USERNAME = 'gabriel_rc'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try:
    digital = aio.feeds('digital')
except RequestError:
    feed = Feed(name="digital")
    digital = aio.create_feed(feed)

out_d = digitalio.DigitalInOut(board.D5)
out_d.direction = digitalio.Direction.OUTPUT

while True:
    data = aio.receive(digital.key)
    if int(data.value) == 1:
        print('received <- ON\n')
    elif int(data.value) == 0:
        print('received <- OFF\n')

    out_d.value = int(data.value)
    time.sleep(0.5)