import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



import os
password = ''
sender_email = ""

def message(name,JobTitle):
 subject=f'Exciting Career Opportunity at QualTech – {JobTitle}'
 email_body =f"""
Dear {name},

I am a Recruiter at QualTech. I checked your profile  and was very impressed with your experience in [Mention a specific skill or project, e.g., cloud infrastructure management, leading software development teams].

QualTech is a leading provider of [mention your industry/what your company does, e.g., innovative quality assurance solutions for the tech industry], and we are currently expanding our [Department Name, e.g., Engineering] team. We are looking for a talented {JobTitle} to join us and contribute to [mention a key project or goal, e.g., developing our next-generation automation platform]. Your background in [mention their experience again] seems like a perfect match for the challenges and opportunities in this role.

I would like to know if you are currently open to exploring new career opportunities.

If this sounds interesting and you are open to a discussion, could you please share the following details? This will help us understand your current position better and see if we can create a mutually beneficial proposal.

Your updated CV/Resume

Current CTC (Cost to Company)

Expected CTC

Notice Period

Your availability for a brief introductory call next week

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,



QualTech

 """
 return [email_body,subject]







def send_email(receiver_email:str,text:str,subject:str):
  '''
  Objective of this function to send email to reciver.
  args:
  receiver_email:str
  text:str
  subject:str
  '''
  sender_email = "misbah2611hasan@yahoo.com"
  receiver_email = receiver_email

  password=os.getenv('YP')
  text=text
  message = MIMEMultipart("alternative")
  message["Subject"] = subject
  message["From"] = sender_email
  message["To"] = receiver_email
  part1 = MIMEText(text, "plain")
  message.attach(part1)
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
  return "Done"

def sendEmail(reciver_email:str,name:str,JobTitle:str):
  '''
  objective of this function to schedule interview.
  args:
  reciver_email:str (email id of reciver)
  name:str  (name of candidate)
  JobTitle:str (job title for which interview is scheduled)
  '''
  arr=message(name,JobTitle)
    
  return send_email(reciver_email,arr[0],arr[1])


import imaplib, email
import pandas as pd

user = sender_email
password = os.getenv('YP')
imap_url = 'imap.mail.yahoo.com'

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data

# Function to get the list of emails under this label
def get_emails(result_bytes):
    msgs = [] # all the email data are pushed inside an array
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)

    return msgs

con = imaplib.IMAP4_SSL(imap_url)

con.login(user, password)

con.select('Inbox')


def recived_emails(id:str):
  '''
  objective of this function to check recived emails from specific user.
  args:
  id:str email id of user
  '''
  user = "misbah2611hasan@yahoo.com"
  password = os.getenv('YP')
  imap_url = 'imap.mail.yahoo.com'
  con = imaplib.IMAP4_SSL(imap_url)

  con.login(user, password)

  con.select('Inbox')

  msgs = get_emails(search('FROM', id, con))

  email_list = []

  for msg_data in msgs[::-1]:
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            email_from = msg.get("From")
            email_subject = msg.get("Subject")
            email_date = msg.get("Date")

            # Extract email body and attachments
            body = None
            attachments = []
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                    elif "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            attachments.append({
                                "filename": filename,
                                "data": part.get_payload(decode=True)
                            })
            else:
                body = msg.get_payload(decode=True).decode()

            email_list.append({
                "From": email_from,
                "Subject": email_subject,
                "Date": email_date,
                "Body": body,

            })
          #  email_list.append({
          #       "From": email_from,
          #       "Subject": email_subject,
          #       "Date": email_date,
          #       "Body": body,
          #       "Attachments": attachments
          #   })
    df = pd.DataFrame(email_list).to_dict()
    return df

# msgs = get_emails(search('FROM', 'misbah2611hsn@gmail.com', con))