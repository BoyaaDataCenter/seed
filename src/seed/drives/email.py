import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate


email_conf = {
    'smtpHost': 'mail.boyaa.com',
    'smtpPort': '587',
    'sslPort': 465,
    'fromMail': 'd_alert@boyaa.com',
    'username': 'd_alert',
    'password': 'D@12!zy$34',
}


def send_email(email_list, title, message, message_type='plain', cc_email_list=[]):
    """
    email_list list 邮件列表
    title 标题
    message 内容
    message_type 内容类型
    message_type = 'html', 'plain'

    通过email方式发送报警信息
    #连接smtp服务器，明文/SSL/TLS三种方式，根据你使用的SMTP支持情况选择一种
    #普通方式，通信过程不加密
    # smtp = smtplib.SMTP(smtpHost,smtpPort)
    # smtp.ehlo()
    # smtp.login(username,password)
    #-----------------------------------------------
    #-----------------------------------------
    #纯粹的ssl加密方式，通信过程加密，邮件数据安全
    # smtp = smtplib.SMTP_SSL(smtpHost,sslPort)
    # smtp.ehlo()
    # smtp.login(username,password)
    #-------------------------------------
    #tls加密方式，通信过程加密，邮件数据安全，使用正常的smtp端口
    """
    result = True
    if not email_list:
        return result
    try:
        to_mail = ";".join(email_list)
        cc_mail = ",".join(cc_email_list)
        subject = title  # 邮件标题和内容
        body = message
        encoding = 'utf-8'  # 初始化邮件
        mail = MIMEText(body.encode(encoding), message_type, encoding)
        mail['Subject'] = Header(subject, encoding)
        mail['From'] = email_conf['fromMail']
        mail['To'] = to_mail
        mail['Cc'] = cc_mail
        mail['Date'] = formatdate()
        smtp = smtplib.SMTP(email_conf['smtpHost'], email_conf['smtpPort'])
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(email_conf['username'], email_conf['password'])
        # 发送邮件
        email_list.extend(cc_email_list)
        smtp.sendmail(email_conf['fromMail'], email_list, mail.as_string())
        smtp.close()
        # print 'send mail succeed'
    except Exception as e:
        print(e)
        result = False

    return result
