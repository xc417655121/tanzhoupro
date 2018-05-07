# -*- coding: utf-8 -*-
from random import Random
from user.models import EmailVerify
from django.core.mail import send_mail
from tanzhoupro.settings import EMAIL_FROM

# 获取一个随机字符串方法
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlNnMmOoPpQqRrSsTtUuVvWwXxYyZz012346789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0,length)]
    return str

# 定义发送邮件方法
def send_register_email(email,send_type='register'):

    email_record = EmailVerify()
    code = random_str(16)

    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

# 设置邮箱发送信息
    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = u"在线注册激活链接"
        email_body = u"请点击下面的链接激活你的账号：http://127.0.0.1:8800/users/active/{0}".format(code)
        # 调用send_email方法发送邮件
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass



    if send_type == "forget":

        email_title = u"密码找回激活链接"
        email_body = u"请点击下面的链接找回你的密码：http://127.0.0.1:8800/users/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass