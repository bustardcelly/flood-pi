import sys
import time
import argparse
import schedule

from ConfigParser import SafeConfigParser

from floodpi.control.mcp3008 import ADC
from floodpi.control.mcp3008 import ADC2
from floodpi.detector.flood import FloodDetector
from floodpi.service.notifier import SMTPNotifier
from floodpi.service.notifier import RESTNotifier

import RPi.GPIO as GPIO

READ_SLEEP = 1
FLOOD_ADC_PIN = 0

conf = SafeConfigParser()
conf.read('config.ini')

parser = argparse.ArgumentParser(description="Flood-Pi.")
parser.add_argument('-n', '--notify', default='', type=str, \
  help='Provide the email addresses to notify (comma-delimited).')
parser.add_argument('-d', '--delay', default='15', type=int, \
  help='Provide the desired delay (in minutes) to schedule check of flood detection (default 15 minutes).')
# 300,500 min/max based on 5.5, 100ohm resister
parser.add_argument('-r', '--range', default='300,500', type=str, \
  help='Provide the comma-delimited min/max range that is considered within flood range (0-1024, default 300,500).')

adc = None
service = None
notifier = None
flood_detector = None

class Unpack(object):
  pass

def check_flood():
  global flood_detector
  level = adc.readadc(FLOOD_ADC_PIN)
  if flood_detector.detect(level):
    print "Detected flood... %r" % level
    notifier.notify(level)
  if not service is None:
    service.notify(level)

def flood_watch(range, notify_list, delay):
  global adc
  global service
  global notifier
  global flood_detector

  running = True

  adc = ADC2()
  adc.open()

  if conf.has_section('service'):
    base_url = conf.get('service', 'baseUrl')
    base_port = conf.get('service', 'basePort')
    endpoint = conf.get('service', 'postEndpoint')
    conf_endpoint = conf.get('service', 'confEndpoint')
    service = RESTNotifier(base_url, base_port, endpoint)
    service.post_configuration(conf_endpoint, delay, range)

  notifier = SMTPNotifier(conf.get('smtp', 'user'), conf.get('smtp', 'password'))
  notifier.add_notifiees(notify_list)

  flood_detector = FloodDetector(range)

  schedule.every(delay).minutes.do(check_flood)
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

  unpack = Unpack()
  args = parser.parse_args(namespace=unpack)

  delay = args.delay
  range_params = args.range.split(',')
  range = {'minimum': int(range_params[0]), 'maximum': int(range_params[1])}

  notify_list = []
  notify_list.append(args.notify.split(','))

  flood_watch(range, notify_list, delay)
