#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

parser = argparse.ArgumentParser(description='Mail Notification for Ubuntu.')
parser.add_argument('-s','--servername', nargs=1,
		    metavar='<servername>',
		    help='IMAP server address',
		    required=True)
parser.add_argument('-u','--username', nargs=1,
		    metavar='<userID>',
		    help='your user ID',
		    required=True)

args = parser.parse_args()
servername = args.servername[0]
username = args.username[0]

print(servername)
print(username)

mail = imaplib.IMAP4_SSL(servername)
mail.login(username,password)
mail.list()
mail.select("Inbox")
status,maillist = mail.search(None,"(UNSEEN)")

if status == "OK":
        if maillist[0] is not '':
            print "New Mail"
