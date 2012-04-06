#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import time
import datetime
import getpass
import imaplib
import pynotify
import gnomekeyring as gk
import subprocess
from os import path


def ret_passwd_from_keyrings(keyring_name,servername):
	item_keys = gk.list_item_ids_sync(keyring_name)
	passwd = ''
	for key in item_keys:
		item_info = gk.item_get_info_sync(keyring_name,key)
		if item_info.get_display_name() == servername:
			passwd = item_info.get_secret()
	return passwd
def entry_passwd_to_keyrings(keyring_name,servername,username,passwd):
	atts = {
		'application' : 'Python mail notification',
		'username' : username,
		'server' : servername,
		}
	gk.item_create_sync(keyring_name, gk.ITEM_GENERIC_SECRET,
			    servername,atts,passwd,True)

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
parser.add_argument('-gk','--with-gnome-keyring', dest='gk',
		    action="store_true", default=False,
		    help="Using Gnome-Keyring (Save Password)")
parser.add_argument('-c','--command',default='',
		    metavar='<command>',
		    help="running command when mail notify")

args = parser.parse_args()
servername = args.servername[0]
username = args.username[0]
set_time = args.time[0]

## Get Password ##
if args.gk:
	password = ret_passwd_from_keyrings('login',servername)
	if password == '':
		password = getpass.getpass()
		entry_passwd_to_keyrings('login',servername,username,password)
else:
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
			print '[',dtime.strftime("%Y-%m-%d %H:%M:%S"),']  : New Mail'

			### Python Notify ###
			pynotify.init( "New Mail" )
			image_dir ='{0}/{1}'.format( path.dirname( path.abspath( __file__ ) ), "images/mail.png")
			noti = pynotify.Notification("New Mail", "You got mail..", image_dir)
			noti.show()

			### Running Command ###
			if (args.command != '') :
				subprocess.call(args.command, shell=True)
			

		       	### maillist_length reset ###
			maillist_length = len(maillist)
	else:
		maillist_length = 0
	time.sleep(set_time)
