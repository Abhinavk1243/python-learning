import imaplib
import email
from email.header import decode_header
import os
from library import read_config
logger=read_config.logger()

## INBOX              - select inbox directory
## [Gmail]/All Mail    - select All Mail directory
## [Gmail]/Drafts     - select Drafts directory
## [Gmail]/Sent Mail  - select sent Mail directory
## [Gmail]/Spam       - select spam Mail directory
## [Gmail]/Starred    - select starred Mail directory
## [Gmail]/Trash      - select trash Mail directory


# status, messages = imap_session.search(None, 'FROM "googlealerts-noreply@google.com"')
# status, messages = imap.search(None, 'SINCE "01-JAN-2020"')
# # to get mails before a specific date
# # status, messages = imap.search(None, 'BEFORE "01-JAN-2020"')
# status, messages = imap.search(None, 'SUBJECT "Thanks for Subscribing to our Newsletter !"')

def del_mail(imap_session,msg):
    imap_session.store(msg, "+FLAGS", "\\Deleted")
    imap_session.expunge()

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def email_scrapping(username,password,mail_no):
    imap_session= imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    try:
        imap_session.login(username, password)
        logger.debug("loged in successfully")
        
        status, no_of_messages = imap_session.select('"[Gmail]/Sent Mail"')
        print(no_of_messages)
        no_of_messages = int(no_of_messages[0])
        
        res, msg = imap_session.fetch(str(mail_no), "(RFC822)")
        logger.debug("get part of msg as res")

        for response in msg:
            
            if isinstance(response,tuple):
                
                mail= email.message_from_bytes(response[1])
                subject, encoding = decode_header(mail["Subject"])[0]
                
                # check if mail-subject is bytes and if true then decode subject
                if isinstance(subject,bytes):
                    subject=subject.decode(encoding)
            
                logger.debug("get subect of mail_no : {i}")
                
                sender, encoding = decode_header(mail["From"])[0]
                receiver,encoding = decode_header(mail["To"])[0]
                
                # check if mail-sender is bytes and if true then decode subject
                if isinstance(sender,bytes):
                    sender=sender.decode(encoding)
                print("=="*50)
                
                print(f"From : {sender}")
                
                print(f"TO : {receiver}")
                
                print(f"Subject : {subject}")
                
                logger.debug("get mail and subject and sender") 
                
                if mail.is_multipart():
                    for part in mail.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part["Content-Disposition"])
                        logger.debug("content_type and content disposition")
                        try:
                            # get the email body
                            body = part.get_payload(decode=True)
                            
                            if body != None:
                                body=body.decode()
                            
                            
                        except Exception as error:
                            pass
                        if content_type=="text/plain" and "attachment" not in content_disposition:
                            print("--"*50)
                            print(f"body :{body}")
                            print("--"*50)
                            
                            logger.debug("body")
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            logger.debug(f"get attachment file :{filename}")
                            if filename:
                                folder_name = os.path.join(os.path.expanduser("~"),'flask-learning\\files\\email_scrap\\email_attachments')
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                                print("attachment file saved at loc :{folder_name}")
                            
                        else:
                            # content_type=mail.get_content_type()
                            # print(content_type)
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            
                            if content_type == "text/plain":
                                # print only text email parts
                                print("--"*50)
                                print(f"body :{body}")
                                print("--"*50)
                                
                                
                            if content_type== "text/html":
                                file_name=clean(subject)
                                file_path = os.path.join(os.path.expanduser("~"),f'flask-learning\\files\\email_scrap\\email_html\\{file_name}.html')
                                open(file_path, "w").write(body)
                                print(f"html file saved at loc :{file_path}")
                                # webbrowser.open(file_path)
        # print(type(msg))
        # imap_session.store(res,  '+FLAGS', '\\Deleted')
        # imap_session.expunge()
        print("=="*50)
        imap_session.close()
        imap_session.logout()

    except Exception as error:
        print(error)
    
    logger.debug("---- email scrapping completed ----")
def main():
    username=read_config.get_config("email","sender")
    password=read_config.get_config("email","password")
    email_scrapping(username,password,241)
    
if __name__=="__main__":
    main()