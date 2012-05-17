#!/usr/bin/env python

import smtplib

import time

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from email.MIMEImage import MIMEImage

smtp_host = "smtp.gmail.com"
smtp_port = 587

username = "user@gmail.com"

password = "888999"

mail_list = "u1@gmail.com, u2@126.com"

subject = "Automatic Test Report"

def mail_report(report_name):
	time_str = time.strftime("%Y-%m-%d %H:%M:%S")
	msg = MIMEMultipart('related')
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = username
	msg['To'] = mail_list
	msg['Date'] = time_str

	msg_alt = MIMEMultipart('alternative')
	msg.attach(msg_alt)

	report_file = open(report_name, "r")
	content = report_file.read()
	report_file.close()

	msgText = MIMEText(content, 'html')
	msg_alt.attach(msgText)

	service = smtplib.SMTP(smtp_host, smtp_port)

	service.ehlo()
	service.starttls()
	service.ehlo()
	service.login(username, password)
	service.sendmail(username, msg['To'].split(','), msg.as_string())

	service.quit()
