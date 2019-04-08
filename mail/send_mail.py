import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_mail():
      # use qq mail host
      mail_host = "smtp.exmail.qq.com"; mail_port = 465
      mail_user = "angxing@mmtrix.com"; mail_pass = "ing"
      sender = 'angxing@mmtrix.com'; receivers = ['angxing@gosun.com']

      message = MIMEText("hi there...", 'plain', 'utf-8')
      message['From'] = Header(sender, 'utf-8')
      message['To'] =  Header(';'.join(receivers), 'utf-8')
      message['Subject'] = Header('test mail', 'utf-8')

      # if no ssl: smtplib.SMTP()
      smtpObj = smtplib.SMTP_SSL()
      smtpObj.connect(mail_host, mail_port)
      smtpObj.login(mail_user, mail_pass)
      smtpObj.sendmail(sender, receivers, message.as_string())

