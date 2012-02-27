#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import time
import getpass
import imaplib

parser = argparse.ArgumentParser(description='Mail Notification for Ubuntu.')
parser.add_argument('-s','--servername', nargs=1,
		    metavar='<servername>',
		    help='IMAP server address',
		    required=True)
parser.add_argument('-u','--username', nargs=1,
		    metavar='<userID>',
		    help='your user ID',
		    required=True)
parser.add_argument('-t','--time', nargs=1, default=[60], type=int,
		    metavar='<Sleep Time>',
		    help='Sleep Time ( default = 60 sec )')

args = parser.parse_args()
servername = args.servername[0]
username = args.username[0]
set_time = args.time[0]
password = getpass.getpass()

print "IMAP Server        : ",servername
print "IMAP User Name     : ",username
print "Refresh Time [sec] : ",set_time

print "====++++  New Mail Waiting  ++++===="

mail = imaplib.IMAP4_SSL(servername)
mail.login(username,password)

while True:
	mail.list()
	mail.select("Inbox")
	status,maillist = mail.search(None,"(UNSEEN)")
	if status == "OK":
		if maillist[0] is not '':
			print "New Mail"
	time.sleep(set_time)
