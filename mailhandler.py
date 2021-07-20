import webapp2
import jinja2
import cgi
import os
import smtplib
import json
import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import leads_mail
import leads_leavemail
import leads_reimmail
from google.appengine.api import mail


class sendMail():
	
	def sendLeadsDetails(self,to_id, contact_number,from_name,to_name,company_name,location,email,website,product,message_html,reply_to):
		message = mail.EmailMessage(sender = "Tracelay <saurabhsinha303@gmail.com>",
										subject = "New Lead")
		message.to = to_id
		message.html = 'Hi Admin You have received Lead of '+'_' + from_name +'_' +'having contact number'+ '_'+contact_number+'_'+'and company name is'+'_'+company_name+'situated at'+'_'+location+'website address'+'_'+website 
		message.send()
		print 'sendMail'

	def sendSubscription(self,to_id, text):
		message = mail.EmailMessage(sender = "Tracelay <saurabhsinha303@gmail.com>",
										subject = "Subscription")
		message.to = to_id
		message.html = 'Hi'+ text  
		message.send()
		print 'sendMail'




   