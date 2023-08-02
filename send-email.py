#!/usr/local/bin/python

import argparse
import sys

import base64
import mimetypes
import os

from sendgrid.helpers.mail import (
    Attachment, Category, Content, CustomArg, Email, Mail, MailSettings, Personalization, SandBoxMode,
)

import markdown
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

parser = argparse.ArgumentParser()
parser.add_argument(
    "--to",
    dest="to_email",
    type=str,
    nargs="+",
    action="extend",
    required=True,
    help="Email address to send the notification to",
)
parser.add_argument("--subject", type=str, required=True, help="Subject of the email")
parser.add_argument(
    "--markdown-body", type=str, required=True, help="Body of the email"
)
parser.add_argument(
    "--from",
    dest="from_email",
    type=str,
    required=True,
    help="Email address to send the notification from",
)
parser.add_argument("--api-key", type=str, required=True, help="SendGrid API key")
#parser.add_argument("--attachments", dest="attachments", type=str, nargs="+", required=False, help="attachments")
parser.add_argument("--attachments", type=str, dest="attachments",default='', nargs="+", required=False, help="attachments")

if __name__ == "__main__":

    args = parser.parse_args()

    message = Mail(
        from_email=args.from_email,
        to_emails=args.to_email,
        subject=args.subject,
        html_content=markdown.markdown(args.markdown_body),
    )

    
    A = [path for item in args.attachments for path in item.split(" ")]
    print("attachments entries:")
    print(A)
    #---------------------------
    # TODO 
    # Evaluate to use glob
    # https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python
    # >>> import glob
    # >>> glob.glob('./*.txt')
    # https://www.geeksforgeeks.org/how-to-use-glob-function-to-find-files-recursively-in-python/
    if len(A):
        # Add email attachment.
        #print(os.getcwd())
        print(args.attachments)
        
        #print("Directory contents:")
        #for f in os.listdir():
        #    print(f)
        
        for fname in args.attachments:
            basename = os.path.basename(fname)
            print("fname:")
            print(fname)
            print("basename:")
            print(basename)
            with open(fname, "rb") as file:
                #content = base64.b64encode(file.read()).decode('utf-8')
                content = base64.b64encode(file.read()).decode()
    
            attachment = Attachment(
                file_content=content,
                file_type=mimetypes.guess_type(basename)[0],
                file_name=basename,
                disposition="attachment",
                content_id=f"<{basename}>"
            )
    
            message.add_attachment(attachment)
      

    
    try:
        sg = SendGridAPIClient(args.api_key)
        response = sg.send(message)
        print(response)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as exp:
        sys.stderr.write(f"{exp}\n")
        
        exit(1)
