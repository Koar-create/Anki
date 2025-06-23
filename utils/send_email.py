#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from load_config import load_config
from datetime import datetime
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# extract color constant
config   = load_config()
colors   = config['colors']
gold     = colors['gold']
red      = colors['red']
green    = colors['green']
yellow   = colors['yellow']
blue     = colors['blue']
purple   = colors['purple']
aquablue = colors['aquablue']
gray     = colors['gray']
reset    = colors['reset']

def send_email(SUBJECT='FINISHED', content='', receiver='1', attach=''):
    HOST = 'smtp.163.com'
    receiver_email = 'yimu01439@gmail.com' if receiver == '1' else ('yangzhx28@mail2.sysu.edu.cn' if receiver == '2' else '')
    sender_email = 'serverheadsup4096@163.com'
    password = 'LNADFRHGZGZIGPMC'
    text = f"Grabbing script glitched. Check it on Linux server ASAP.\n Content: {content}" if 'Error' in SUBJECT else content
    
    # create mail content
    msg = MIMEMultipart()
    msg['From'] = f'Email Bot <{sender_email}>'
    msg['To'] = f'<Z. Yang {receiver_email}>'
    msg['Subject'] = SUBJECT
    # add content to mail
    body = text
    msg.attach(MIMEText(body, 'plain'))

    if len(attach) != 0:
        try:
            with open(attach, 'rb') as attachment:
                part = MIMEBase('application',  'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {attach}',
                )
                msg.attach(part)
        except Exception as e:
            print(f"failed to load attachment: {e}")
            sys.stdout.flush()
            return
    
    try:
        server = SMTP()
        server.connect(HOST, 25)
        # server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"{gold}Successfully sent mail!{reset}")
        sys.stdout.flush()

    except Exception as e:
        print(f"{red}failed to send mail: {e}{reset}")
        sys.stdout.flush()

if __name__ == '__main__':
    send_email(SUBJECT='Nothing', content='nothing...', receiver='2', attach='')
    