import random

from django.core.mail import send_mail

from django.core.mail import send_mail
from ppyj_log import local_settings


def code_yan():
    return random.randint(1000,9999)

def send_register_email(to_email,code):

    # 标题
    subject = '捅萝卜官方网站'
    # 内容
    message = f'欢迎注册捅萝卜网站您的验证码是{code}'
    # 支持html格式
    html_message =( '#')
    # 用哪个邮箱发
    sender = local_settings.EMAIL_HOST_USER
    # 发送给谁
    receiver = [to_email]
    send_mail(subject, message, sender, receiver, html_message=message)



