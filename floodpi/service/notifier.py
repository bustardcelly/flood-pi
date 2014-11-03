import smtplib

USER='bustardcelly@gmail.com'
PWD='!monty13'

SUBJECT='Message from FloodPi'
FROM='bustardcelly@gmail.com'


class SMTPNotifier:
  def __init__(self):
    pass

  def run(self, email_list, level):
    # TODO: debounce
    body = 'A flood detection of level %r has been detected.' % level
    message = 'Subject: %s\n\n%s' % (SUBJECT, body)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(USER, PWD)
    for email in email_list:
      print "Sending email to %r" % email
      server.sendmail(FROM, email, message)
    server.quit()
