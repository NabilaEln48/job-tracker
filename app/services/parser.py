import mailbox
import re
from io import BytesIO

def extract_company_name(subject, sender):
    """
    Heuristic to find company name. 
    Mid-dev tip: Use domain extraction as a fallback.
    """
    # Pattern 1: "Application for [Company]"
    match = re.search(r"at\s+([A-Z][\w\s]+)", subject)
    if match:
        return match.group(1).strip()
    
    # Pattern 2: Extract from sender domain (e.g., jobs@google.com -> google)
    domain_match = re.search(r"@([\w-]+)\.", sender)
    if domain_match:
        return domain_match.group(1).capitalize()
    
    return "Unknown Company"

def parse_mbox_content(file_bytes):
    # Use BytesIO to treat raw bytes as a file for the mailbox library
    file_like = BytesIO(file_bytes)
    
    temp_name = "temp_process.mbox"
    with open(temp_name, "wb") as f:
        f.write(file_bytes)
    
    mbox = mailbox.mbox(temp_name)
    extracted_jobs = []

    for message in mbox:
        subject = str(message['subject'])
        sender = str(message['from'])
        body = ""

        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    body = str(part.get_payload(decode=True))
                    break
        else:
            body = str(message.get_payload(decode=True))

        # Status Inference Logic
        status = "Applied"
        if re.search(r"interview|schedule|call|on-site", body, re.I):
            status = "Interview"
        elif re.search(r"not moving forward|unfortunately|regret", body, re.I):
            status = "Rejected"
        elif re.search(r"offer|congratulations|contract", body, re.I):
            status = "Offer"

        extracted_jobs.append({
            "company": extract_company_name(subject, sender),
            "subject": subject,
            "status": status,
            "body_snippet": body[:200]
        })
    
    return extracted_jobs