import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(email):
    """  发送邮件  """
    # 定义邮件消息内容
    message = MIMEText('<h2>温馨提醒：</h2><p>' + email['message'] + '</p>', 'html', _charset='utf-8')
    # 添加邮件主题
    message['Subject'] = Header(email['subject'], 'utf-8')
    message['From'] = Header(email['sender'], 'utf-8')
    # 创建SMTP对象
    smtp = smtplib.SMTP(email['host'], 25)
    # 登录邮箱
    smtp.login(email['sender_account'], email['password'])
    # 发送邮件
    smtp.sendmail(email['sender_account'], email['receiver'], message.as_string())
