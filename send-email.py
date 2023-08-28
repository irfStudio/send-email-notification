#!/usr/local/bin/python

import argparse
import base64
import glob
import mimetypes
import os
import sys

import markdown
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    Category,
    Content,
    CustomArg,
    Email,
    Mail,
    MailSettings,
    Personalization,
    SandBoxMode,
)

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
parser.add_argument("--markdown-body", type=str, required=True, help="Body of the email")
parser.add_argument(
    "--from",
    dest="from_email",
    type=str,
    required=True,
    help="Email address to send the notification from",
)
parser.add_argument("--api-key", type=str, required=True, help="SendGrid API key")

parser.add_argument(
    "--attachments", type=str, dest="attachments", default="", nargs="+", required=False, help="attachments"
)

if __name__ == "__main__":
    args = parser.parse_args()
    print("to_email:")
    print(args.to_email)
    to = [e for item in args.to_email for e in item.split(" ")]

    print("to:")
    print(to)

    message = Mail(
        from_email=args.from_email,
        to_emails=to,
        subject=args.subject,
        html_content=markdown.markdown(args.markdown_body),
    )

    A = [path for item in args.attachments for path in item.split(" ")]
    print("attachments entries:")
    print(A)

    if len(A):
        for fname in A:
            for f in glob.iglob(fname):  # generator, search immediate subdirectories 
                print("fname:")
                print(f)
                basename = os.path.basename(f)
               
                print("basename:")
                print(basename)
                with open(f, "rb") as file:
                    content = base64.b64encode(file.read()).decode()
        
                attachment = Attachment(
                    file_content=content,
                    file_type=mimetypes.guess_type(basename)[0],
                    file_name=basename,
                    disposition="attachment",
                    content_id=f"<{basename}>",
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
