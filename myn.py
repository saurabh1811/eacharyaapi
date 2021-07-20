# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import json, urllib2, logging
import cloudDbHandler as dbhelper
import datetime
import json
import StringIO

import mailhandler
import random
from math import radians, cos, sin, asin, sqrt
import math
import ast
from time import gmtime, strftime
import cloudDbHandler as dbhelper
from sets import  Set
import unicodedata
import urllib
import urllib2



# from datetime import datetime


import googleapiclient.discovery
import googleapiclient.http
from google.appengine.api import urlfetch
from datetime import timedelta, date, datetime
from time import gmtime, strftime,time,localtime






app = Flask(__name__)

############################   Normal Function To calculate the Details   ###################################################

API_KEY = ['NkHb13BxRBiZ0JSyxLbAU','Hx1XU63ZThyFGsqfLeGu7']

def daterange(date1, date2):
	for n in range(int ((date2 - date1).days)+1):
		yield date1 + timedelta(n)

def haversine(lon1, lat1, lon2, lat2):
	"""
	Calculate the great circle distance between two points 
	on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	# haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
	km = 6367 * c


	return km



@app.after_request
def after_request(response):
	response.headers['Access-Control-Allow-Origin']='*'
	response.headers['Access-Control-Allow-Headers']='Content-Type, Authorization'
	response.headers['Access-Control-Allow-Methods']= 'GET, PUT, POST, DELETE'
	return response


# documents upload
@app.route('/myn/jobs/documents/',methods=['GET','POST'])
def mynadddocuments():
	if request.method=='POST':
		documents   = json.loads(request.data)


		mobile                = documents['mobile']
		aadharcard            = documents['aadharcard']
		epiccard              = documents['epiccard']
		highestqualification  = documents['highestqualification']
		pancard               = documents['pancard']
		passportsizephoto     = documents['passportsizephoto']

		Adduser = dbhelper.AddData().addclassdocuments(mobile,aadharcard,epiccard,highestqualification,pancard,passportsizephoto)
		if Adduser==0:
			d=0
		else:
			d=1
				
	resp = Response(json.dumps({"success": d}))
	return after_request(resp)
		




