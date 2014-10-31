import smtplib

USER='bustardcelly@gmail.com'
PWD='!monty13'

FROM='bustardcelly@gmail.com'

class SMSNotifier:
  def __init__(self):
    pass

  def run(self, email_list):
    # TODO: debounce
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(USER, PWD)
    for email in email_list:
      server.sendmail(FROM, email, 'FLOOD!!')
    server.quit()
