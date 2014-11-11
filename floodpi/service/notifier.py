import requests
import smtplib

SUBJECT = 'Alert from FloodPi.'

class SMTPNotifier:

  def __init__(self, user, password):
    self.user = user
    self.password = password
    self.notifiees = []
    print "FROM service set with u/p, %r/%r" % (user, password)

  def add_notifiees(self, listing):
    self.notifiees.extend(listing)

  def notify(self, level):
    body = 'A flood detection of level %r has been detected.' % level
    message = 'Subject: %s\n\n%s' % (SUBJECT, body)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(self.user, self.password)
    for email in self.notifiees:
      print "Sending email to %r" % email
      server.sendmail(self.user, email, message)
    server.quit()

class RESTNotifier:

  def __init__(self, base_url, base_port, endpoint):
    self.base_url = base_url
    self.base_port = base_port
    self._post_endpoint = endpoint
    print "POST service set to %s:%d/%s" % (self.base_url, self.base_port, self._post_endpoint)

  def create_endpoint_url(self, endpoint):
    return "http://%s:%s/%s" % (self.base_url, self.base_port, endpoint)

  def post_configuration(self, endpoint, delay, range):
    url = self.create_endpoint_url(endpoint)
    data = {'delay': delay, 'range':range}
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    try:
      print "POSTing configuration to %s" % (url)
      r = requests.post(url, data=json.dumps(data), headers=headers)
    except requests.exceptions.HTTPError as e:
      print 'POST configuration Error: %s' % e.message

  def notify(self, level):
    url = self.create_endpoint_url(self.post_endpoint)
    data = {'level': level}
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    try:
      print "POSTing level reading to %s" % (url)
      r = requests.post(url, data=json.dumps(data), headers=headers)
    except requests.exceptions.HTTPError as e:
      print 'POST level notification Error: %s' % e.message

  @property
  def post_endpoint(self):
    return self._post_endpoint

  @post_endpoint.setter
  def post_endpoint(self, value):
    self._post_endpoint = value 
