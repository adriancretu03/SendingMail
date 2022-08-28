import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from templates import Template

username = '<your email>'
password = '<your password>'

class Emailer():
    subject = ""
    context = {}
    to_emails = []
    from_email  = 'your name <your email>'
    template_name = None
    
    def __init__(self, subject="", template_name = None, context={}, to_emails=None):
        if template_name == None:
            raise Exception("You must set a template")
        assert isinstance(to_emails, list)
        self.to_emails = to_emails
        self.subject = subject
        self.context = context
        self.template_name = template_name
    
    def format_msg(self):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.from_email
        msg['To'] = ", ".join(self.to_emails)
        msg['Subject'] = self.subject
        if self.template_name != None:
            tmpl_str = Template(template_name=self.template_name, context=self.context)
            txt_part = MIMEText(tmpl_str.render(), 'plain')
            msg.attach(txt_part)
        msg_str = msg.as_string()
        return msg_str

    def send(self):
        msg = self.format_msg()
        # login to my smtp server
        did_send = False
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as server:
            server.ehlo()
            server.starttls()
            server.login(username, password)
            try:
                server.sendmail(self.from_email, self.to_emails, msg)
                did_send = True
            except:
                did_send = False
        return did_send

if __name__ == '__main__':
    
    obj = Emailer(subject = "Python Project", template_name = "hello.txt", context = {'name': "<your name>"}, to_emails= ['<your list of emails>'] )
    print(obj.send())

