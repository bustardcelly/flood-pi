import time
import argparse
import schedule

from floodpi.control.mcp3008 import ADC
from floodpi.control.mcp3008 import ADC2
from floodpi.service.notifier import SMTPNotifier

import RPi.GPIO as GPIO

# 5.5, 100ohm resister
MIN_THRESHOLD=300
MAX_THRESHOLD=500
CHECK_DELAY=30

READ_SLEEP=0.5

parser = argparse.ArgumentParser(description="Flood-Pi.")
parser.add_argument('-n', '--notify', default='bustardcelly@gmail.com', type=str, \
  help='Provide the email addresses to notify (comma-delimited).')

adc = None
notifier = None
notifiees = None

flood_adc = 0

class Unpack(object):
  pass

def check_flood():
  global adc
  global notifiees
  level = adc.readadc(flood_adc)
  if level > MIN_THRESHOLD and level < MAX_THRESHOLD:
    print "Detected flood... %r" % level
    notifier.run(notifiees, level)

def flood_watch(notify_list):
  global adc
  global notifier
  global notifiees

  running = True

  notifiees = notify_list
  
  adc = ADC2()
  adc.open()

  notifier = SMTPNotifier()

  schedule.every(CHECK_DELAY).minutes.do(check_flood)
  check_flood()
  
  while running:
    try:
      schedule.run_pending()
      time.sleep(1);
    except KeyboardInterrupt:
      running = False
      schedule.clear()
      adc.close()
      sys.exit('\nExplicit close.')

if __name__ == '__main__':
  GPIO.setmode(GPIO.BCM)
  notify_list = []
  unpack = Unpack()
  args = parser.parse_args(namespace=unpack)
  notify_list.append(args.notify.split(','))
  flood_watch(notify_list)