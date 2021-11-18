import smtplib, ssl
import time
import imaplib
import email
import datetime

from utils import motor

email_debounce = False

sys_admin_email = 'iotvanier.smarthome@gmail.com'
sys_admin_pw = 'banana123!'
client_email = 'iotvanier.smarthome@gmail.com' #change to client email
client_pw = 'banana123!' #change to client pw

def send_email(e_subject, e_text):
    global email_debounce
    if (not email_debounce):
        email_debounce = True

        sender = sys_admin_email
        pw = sys_admin_pw

        receiver = client_email
        port = 465

        subject = e_subject
        text = e_text
        
        message = 'Subject: {}\n\n{}'.format(subject, text)

        context = ssl.create_default_context()

        print("Sending")

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, pw)
            server.sendmail(sender, receiver, message)
            
        print("Sent to ", receiver)
        
        email_debounce = False

def email_reader():
    global sent_fan_on

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(client_email, client_pw)
    mail.list()
    mail.select('inbox')
    result, data = mail.uid('search', None, "UNSEEN") # (ALL/UNSEEN)
    i = len(data[0].split())

    for x in range(i): 
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        # result, email_data = conn.store(num,'-FLAGS','\\Seen') 
        # this might work to set flag to seen, if it doesn't already
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        # Header Details
        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
        
        email_from = ""
        email_to = ""
        subject = ""
        
        if email_message['From']:
            email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        if email_message['To']:
            email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
        if email_message['Subject']:
            subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

        if (email_to == ""):
            email_to = email_from

        # Body details
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)   
                body = body.decode('utf-8').split("\r\n")[0].strip().lower()
                if body[0:3] == "yes":
                    if 'Enable Fan' in subject:
                        motor.change_motor_state(True)
                        # sent_fan_on = False

            else:
                continue