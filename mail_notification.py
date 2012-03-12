#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import time
import datetime
import getpass
import imaplib
import pynotify
from os import path

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

mail = imaplib.IMAP4_SSL(servername)
mail.login(username,password)

print "====++++  New Mail Waiting  ++++===="
maillist_length = 0

while True:
	mail.list()
	mail.select("Inbox")
	status,maillist = mail.search(None,"(UNSEEN)")
	maillist = maillist[0].split()
	if (status == "OK") and  (len(maillist) > 0) :
		if maillist_length < len(maillist):
			
			### get local time ###
			dtime = datetime.datetime.today()
			
			### print terminal ###
			print '[%s-%s-%s %s:%s:%s] : New Mail' % (dtime.year, dtime.month, dtime.day, dtime.hour, dtime.minute, dtime.second)

			### Python Notify ###
			pynotify.init( "New Mail" )
			image_dir ='{0}/{1}'.format( path.dirname( path.abspath( __file__ ) ), "images/mail.png")
			noti = pynotify.Notification("New Mail", "You got mail..", image_dir)
			noti.show()

		       	### maillist_length reset ###
			maillist_length = len(maillist)
	else:
		maillist_length = 0
	time.sleep(set_time)
