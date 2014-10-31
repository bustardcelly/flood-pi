import argparse
from floodpi.control.mcp3008 import ADC
from floodpi.service.notifier import SMSNotifier

import RPi.GPIO as GPIO

MIN_THRESHOLD=400
MAX_THRESHOLD=700

READ_SLEEP=0.5

parser = argparse.ArgumentParser(description="Flood-Pi.")
parser.add_argument('-n', '--notify', default='bustardcelly@gmail.com', type=str, \
  help='Provide the email addresses to notify.')

adc = None
flood_adc = 0

class Unpack(object):
  pass

def check_flood():
  return adc.readadc(flood_adc)

def flood_watch(notifiees):
  running = True
  
  adc = ADC()
  adc.open()

  notifier = SMSNotifier()
  
  while running:
    try:
      level = check_flood()
      if level > MIN_THRESHOLD and level < MAX_THRESHOLD:
        notifier.run(notifies)
      time.sleep(READ_SLEEP))
    except KeyboardInterrupt:
      running = False
      adc.close()
      sys.exit('\nExplicit close.')

if __name__ == '__main__':
  notify_list = []
  unpack = Unpack()
  args = parser.parse_args(namespace=unpack)
  notify_list.append(args.notify)
  flood_watch(notify_list)