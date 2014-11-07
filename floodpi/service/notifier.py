import smtplib

SUBJECT = 'Message from FloodPi'

class SMTPNotifier:

  def __init__(self, user, password):
    self.user = user
    self.password = password
    print "FROM service set with u/p, %r/%r" % (user, password)

  def run(self, email_list, level):
    body = 'A flood detection of level %r has been detected.' % level
    message = 'Subject: %s\n\n%s' % (SUBJECT, body)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(self.user, self.password)
    for email in email_list:
      print "Sending email to %r" % email
      server.sendmail(self.user, email, message)
    server.quit()
