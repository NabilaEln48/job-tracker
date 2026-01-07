import mailbox
from email.message import EmailMessage

def create_fake_mbox():
    mbox = mailbox.mbox('test_data.mbox')
    
    emails = [
        {"from": "hr@google.com", "sub": "Application at Google", "body": "Thanks for applying!"},
        {"from": "recruiter@meta.com", "sub": "Interview with Meta", "body": "We want to schedule a call for an interview."},
        {"from": "jobs@amazon.com", "sub": "Update on Amazon Role", "body": "Unfortunately, we are not moving forward."}
    ]

    for e in emails:
        msg = EmailMessage()
        msg['From'] = e['from']
        msg['Subject'] = e['sub']
        msg.set_content(e['body'])
        mbox.add(msg)
    
    mbox.flush()
    print("Created test_data.mbox successfully.")

if __name__ == "__main__":
    create_fake_mbox()