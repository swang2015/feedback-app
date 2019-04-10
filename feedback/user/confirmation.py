from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.utils

from feedback import app


def generate_token(email):
	serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
	return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
	serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
	try:
		email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
	except:
		return False
	return email


def send_email(recipient_email, confirm_url):
	subject = 'Please confirm your email'
	body_text = "Please follow this link to activate your account:\n{confirm_url}"
	body_html = """<p>Please follow this link to activate your account:</p>
	<p><a href="{confirm_url}">{confirm_url}</a></p>"""

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = email.utils.formataddr((app.config['MAIL_DEFAULT_SENDERNAME'], app.config['MAIL_DEFAULT_SENDER']))
	msg['To'] = recipient_email
	part1 = MIMEText(body_text.format(confirm_url=confirm_url), 'plain')
	part2 = MIMEText(body_html.format(confirm_url=confirm_url), 'html')
	msg.attach(part1)
	msg.attach(part2)
	
	try:
		smtpserver = smtplib.SMTP(app.config['MAIL_SERVER'],app.config['MAIL_PORT'])
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo()
		smtpserver.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
		smtpserver.sendmail(app.config['MAIL_DEFAULT_SENDER'], recipient_email, msg.as_string())
	except Exception as e:
		print(str(e))
		return False
	return True