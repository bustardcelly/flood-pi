import argparse
from ConfigParser import SafeConfigParser
from floodpi.service.notifier import SMTPNotifier

conf = SafeConfigParser()
conf.read('config.ini')

parser = argparse.ArgumentParser(description="Flood-Pi.")
parser.add_argument('-n', '--notify', type=str, \
  help='Provide the email addresses to notify (comma-delimited).')

class Unpack(object):
  pass

if __name__ == '__main__':
  notifier = SMTPNotifier(conf.get('smtp', 'user'), conf.get('smtp', 'password'))

  unpack = Unpack()
  args = parser.parse_args(namespace=unpack)
  notify_list = [] if args.notify== None else args.notify.split(',')
  notifier.run(notify_list, 80)