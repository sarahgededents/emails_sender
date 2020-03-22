from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
import smtplib
import csv
######create your id.txt file with email and password in it#######

with open('id.txt', 'r', encoding='utf-8') as ids:
    idt = ids.read()
    MY_ADDRESS = idt.split(',')[0]
    PASSWORD = idt.split(',')[1]


def domain_name(email):
    _, second_part = email.rsplit('@', 1)
    domain_name, _ = second_part.split('.', 1)
    return domain_name

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    
    names = []
    emails = []
    with open(filename, 'r', encoding='utf-8') as contacts_file:
        
        for a_contact in csv.reader(contacts_file):
            name, email = a_contact
            emails.append(email)
            names.append(name)
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main(file_contact, msg_file, subject):
    count = 1
    names, emails = get_contacts(file_contact) # read contacts
    message_template = read_template('message-email/' + msg_file)

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587) #Change with your host
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())

        # Prints out the counter and recipients for our sake
        print(str(count) + ': ', email)
        
        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']=open('message-email/' + subject, 'r').read()
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        count = count + 1
    # Terminate the SMTP session and close the connection
    s.quit()

if __name__ == '__main__':
    main('to_foreign1.csv', 'msg.txt', 'subject.txt')
