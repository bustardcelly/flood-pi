import time
import argparse
import schedule

from ConfigParser import SafeConfigParser

from floodpi.control.mcp3008 import ADC
from floodpi.control.mcp3008 import ADC2
from floodpi.service.notifier import SMTPNotifier

import RPi.GPIO as GPIO

# 5.5, 100ohm resister
MIN_THRESHOLD = 300
MAX_THRESHOLD = 500
CHECK_DELAY = 15

READ_SLEEP = 1

conf = SafeConfigParser()
conf.read('config.ini')

parser = argparse.ArgumentParser(description="Flood-Pi.")
parser.add_argument('-n', '--notify', default='bustardcelly@gmail.com', type=str, \
  help='Provide the email addresses to notify (comma-delimited).')
parser.add_argument('-d', '--delay', default='15', type=int, \
  help='Provide the desired delay (in minutes) to schedule check of flood detection (default 15 minutes).')

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

  notifier = SMTPNotifier(conf.get('smtp', 'user'), conf.get('smtp', 'password'))

  schedule.every(CHECK_DELAY).minutes.do(check_flood)
  check_flood()

  while running:
    try:
      schedule.run_pending()
      time.sleep(READ_SLEEP)
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
