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
from datetime import date, timedelta
import seminarcloudDbHandler as dbhelper
import create_cert



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



# login
@app.route('/seminar/user/login/', methods=['GET','POST'])
def ApiUserLoginNew():
	if request.method  == 'POST':
		user_data =json.loads(request.data)
		mobile = user_data['mobile']
		otp  = user_data['otp']
		print otp
		User= dbhelper.GetData().getUserLoginStatusNew(mobile)
		print User
		if len(User)>0:
			name = User[0][1]
			email = User[0][2]
			mobile=User[0][3]
			image= User[0][26]
			imageUrl='https://storage.googleapis.com/seminar-efe78.appspot.com/registration/'
		
			text =" Welcome+to+SEMINAR. Your+Login+OTP+is+ %s."%(str(otp))
			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=INOBIN&mobile=%s&msg=%s'%(str(mobile),text)
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})
			db={'message':'User Exist',"confirmation":1,"name":name,"mobile":mobile,"otp":otp, "email":email}
		else:
			db={'message': 'User Not Exist', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)


@app.route('/seminar/resend/otp/', methods=['GET','POST'])
def ApiResendOtp():
	if request.method  == 'POST':
		user_data =json.loads(request.data)
		mobile = user_data['mobile']
		otp  = user_data['otp']
		print otp
		
		
		text =" Welcome+to+SEMINAR. Your+Login+OTP+is+ %s."%(str(otp))
		url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=INOBIN&mobile=%s&msg=%s'%(str(mobile),text)
		urlfetch.set_default_fetch_deadline(45)
		resp = urlfetch.fetch(url=url,
			method=urlfetch.GET,
			headers={'Content-Type': 'text/html'})
		db={'message':'User Exist',"confirmation":1,"mobile":mobile,"otp":otp}
		
		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)





# signup

@app.route('/seminar/add/user/',methods=['GET','POST'])
def APiadduser():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		name= userInfo['name']
		email = userInfo['email']
		mobile = userInfo['mobile']
		dob= userInfo['dob']
		try:
			designation1 = userInfo['designation1']
			designation2 = userInfo['designation2']
			designation3 = userInfo['designation3']
			designation4 = userInfo['designation4']
			designationYear1 = userInfo['designationYear1']
			designationYear2 = userInfo['designationYear2']
			designationYear3 = userInfo['designationYear3']
			designationYear4 = userInfo['designationYear4']
			qualification1 = userInfo['qualification1']
			qualification2 = userInfo['qualification2']
			qualification3 = userInfo['qualification3']
			qualification4 = userInfo['qualification4']
			qualificationYear1 = userInfo['qualificationYear1']
			qualificationYear2 = userInfo['qualificationYear2']
			qualificationYear3 = userInfo['qualificationYear3']
			qualificationYear4 = userInfo['qualificationYear4']
			affiliations1 = userInfo['affiliations1']
			affiliations2 = userInfo['affiliations2']
			affiliations3 = userInfo['affiliations3']
			affiliations4 = userInfo['affiliations4']
			imageName = userInfo['imageName']
			registrationNo=userInfo['registrationNo']

		except:
			designation1 = ''
			designation2 = ''
			designation3 = ''
			designation4 = ''
			designationYear1 = ''
			designationYear2 = ''
			designationYear3 = ''
			designationYear4 = ''
			qualification1 = ''
			qualification2 = ''
			qualification3 = ''
			qualification4 = ''
			qualificationYear1 = ''
			qualificationYear2 = ''
			qualificationYear3 = ''
			qualificationYear4 = ''
			affiliations1 = ''
			affiliations2 = ''
			affiliations3 = ''
			affiliations4 = ''
			imageName =''
			registrationNo=''

		gender= userInfo['gender']
		
		
		otp      = userInfo['otp']
		user_status =dbhelper.GetData().getUserStatus(mobile)
		print user_status
		if user_status==True:
			db={'message':'User Already Exist',"confirmation":0}    
			resp = Response(json.dumps({"response": db}))
			return after_request(resp)
		else:
			AddUser = dbhelper.AddData().addUser(name,email,mobile,dob,designation1,designation2,designation3,designation4,designationYear1,designationYear2,designationYear3,designationYear4,qualification1,qualification2,qualification3,qualificationYear1,qualificationYear2,qualificationYear3,qualificationYear4,qualification4,affiliations1,affiliations2,affiliations3,affiliations4,gender,imageName,registrationNo)

			db={'message':'User Added',"confirmation":1,"mobile":mobile,"name":name,"email":email,"otp":otp}

			text ="User+has+been+registered+successfully.Your+Login+OTP+is+ %s."%(str(otp))

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=idwealth1&pwd=api@idwealth1&sender=INOBIN&mobile=%s&msg=%s'%(str(mobile),text)
			print url
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})
			respp = Response(json.dumps({"response": db}))
			return after_request(respp)

# create Event
@app.route('/seminar/add/user/list/',methods=['GET','POST'])
def APiadduserlist():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		seminarName=userinfo['seminarName']
		seminarDate=userinfo['seminarDate']
		location=userinfo['location']
		seminarCode=userinfo['seminarCode']
		image=userinfo['image']
		mobile=userinfo['mobile']
		email=userinfo['email']
		endDate=userinfo['endDate']
		userId=userinfo['userId']


		
		
		AddUser = dbhelper.AddData().addUserlist(seminarName,seminarDate,location,seminarCode,mobile,image,email,endDate,userId)
		AddUser2 = dbhelper.AddData().addUserhelp(mobile,email,seminarCode,userId)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)

# fcm token
@app.route('/seminar/add/token/',methods=['GET','POST'])
def ApiAddToken():
	if request.method=='POST':
		query_data = json.loads(request.data)
		mobile = query_data['mobile']
		fcmToken= query_data['fcmToken']
	   
		update              =dbhelper.DeleteData().deleteToken(mobile)

		last                =dbhelper.AddData().addToken(mobile,fcmToken)
		if last:
			db={'message':'Token Added',"confirmation":1}
		else:
			db={'message': 'Token not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)




# Add Question
@app.route('/seminar/add/question/',methods=['GET','POST'])
def APiaddquestion():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		lastId   =dbhelper.GetData().getLastIDNew()[0][0]
		if lastId:
			newid=str(123+lastId)
		else:
			newid=str(123)
		seminarId = userInfo['seminarId']
		questionId = 'QUE' + newid
		question  = userInfo['question']
		option1  = userInfo['option1']
		option2     = userInfo['option2']
		option3      = userInfo['option3']
		option4 = userInfo['option4']
		questionType = userInfo['questionType']
		userId = userInfo['userId']
		
		
		AddQuestion = dbhelper.AddData().addQuestion(seminarId,questionId,question,option1,option2,option3,option4,questionType,userId)
		if AddQuestion==0:
			d=0
		else:
			d=1
				
	resp = Response(json.dumps({"success": d}))
	return after_request(resp)
# Add QUiz
@app.route('/seminar/add/question/two/',methods=['GET','POST'])
def APiaddquestion2():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		lastId   =dbhelper.GetData().getLastIDNew()[0][0]
		if lastId:
			newid=str(123+lastId)
		else:
			newid=str(123)
		seminarId = userInfo['seminarId']
		questionId = 'QUE' + newid
		question  = userInfo['question']
		option1  = userInfo['option1']
		option2     = userInfo['option2']
		option3      = userInfo['option3']
		option4 = userInfo['option4']
		questionType = userInfo['questionType']
		correct = userInfo['correct']
		imageName = userInfo['imageName']
		userId = userInfo['userId']
		
		
		AddQuestion = dbhelper.AddData().addQuestion2(seminarId,questionId,question,option1,option2,option3,option4,questionType,correct,imageName,userId)
		if AddQuestion==0:
			d=0
		else:
			d=1
				
	resp = Response(json.dumps({"success": d}))
	return after_request(resp)

# Document Upload
@app.route('/seminar/mtrack/file/upload/',methods=['GET','POST'])
def apiMtrackFileUpload():
	if request.method=='POST':
		file_object = request.files['file']
		
		BUCKET_NAME = 'mtrac-b56ab.appspot.com'
		storage = googleapiclient.discovery.build('storage', 'v1')
		
		print '**',file_object, type(file_object)
		GCS_UPLOAD_FOLDER = 'Profile' 
		
		filename = file_object.filename.replace(" ","_")
		file_object.filename=file_object.filename.replace(" ","_")
		string_io_file = StringIO.StringIO(file_object.stream.read())

		fullName = GCS_UPLOAD_FOLDER + '/'+ filename
		print fullName
		body = {
			'name': fullName,
		}

		
		

		req = storage.objects().insert(bucket=BUCKET_NAME, body=body, media_body=googleapiclient.http.MediaIoBaseUpload(string_io_file, 'application/pdf'))
		response = req.execute()
		resp = Response(json.dumps({"success": True, "datasets": 'Yahoo'}))
		return after_request(resp) 


@app.route('/seminar/file/upload/',methods=['GET','POST'])
def apiSeminarUpload():
	if request.method=='POST':
		dataLst          = tripInfo['data']
		for request.files in dataLst:
			file_object = request.files['file']
			
			BUCKET_NAME = 'mtrac-b56ab.appspot.com'
			storage = googleapiclient.discovery.build('storage', 'v1')
			
			print '**',file_object, type(file_object)
			GCS_UPLOAD_FOLDER = 'Profile' 
			
			filename = file_object.filename.replace(" ","_")
			file_object.filename=file_object.filename.replace(" ","_")
			string_io_file = StringIO.StringIO(file_object.stream.read())

			fullName = GCS_UPLOAD_FOLDER + '/'+ filename
			print fullName
			body = {
				'name': fullName,
			}

			
			

			req = storage.objects().insert(bucket=BUCKET_NAME, body=body, media_body=googleapiclient.http.MediaIoBaseUpload(string_io_file, 'application/pdf'))
			response = req.execute()
		resp = Response(json.dumps({"success": True, "datasets": 'Yahoo'}))
		return after_request(resp) 

@app.route('/seminar/seminar/file/upload/',methods=['GET','POST'])
def apiSeminarUpload2():
	if request.method=='POST':
		print request.files
		file_object = request.files['file']
		
		BUCKET_NAME = 'mtrac-b56ab.appspot.com'
		storage = googleapiclient.discovery.build('storage', 'v1')
		
		print '**',file_object, type(file_object)
		GCS_UPLOAD_FOLDER = 'Profile' 
		
		filename = file_object.filename.replace(" ","_")
		file_object.filename=file_object.filename.replace(" ","_")
		string_io_file = StringIO.StringIO(file_object.stream.read())

		fullName = GCS_UPLOAD_FOLDER + '/'+ filename
		print fullName
		body = {
			'name': fullName,
		}
		print body

		
		

		req = storage.objects().insert(bucket=BUCKET_NAME, body=body, media_body=googleapiclient.http.MediaIoBaseUpload(string_io_file, 'application/octet-stream'))
		response = req.execute()



		resp = Response(json.dumps({"success": True, "datasets": 'Yahoo',"message":"Logo has been Updated"}))
		return after_request(resp) 


# Feedback comment
@app.route('/seminar/add/comment/',methods=['GET','POST'])
def APiaddcomment():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
















		seminarId  = userInfo['seminarId']
		topicId     = userInfo['topicId']
		rating      = userInfo['rating']
		comment = userInfo['comment']
		
		
		AddQuestion = dbhelper.AddData().addComment(mobile,seminarId,topicId,rating,comment)

		AddSessionFeed = dbhelper.AddData().addSessionFeedPoint(mobile,seminarId,10)

		if AddQuestion==0:
			d=0
		else:
			d=1
				
	resp = Response(json.dumps({"success": d}))
	return after_request(resp)

# ask question
@app.route('/seminar/add/ask/question/',methods=['GET','POST'])
def APiaddaskquestion():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		name=userinfo['name']
		mobile=userinfo['mobile']
		question=userinfo['question']
		code=userinfo['seminarId']
		imageName=userinfo['imageName']

		now= datetime.now()
		if name=="":
			name ="Anonymus"

		date= now.strftime('%d/%m/%Y')
		time= now.strftime("%I:%M %p" )
		AddUser = dbhelper.AddData().addaskquestion(name,mobile,question,code,date,time,imageName)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)

# ask question list
@app.route('/seminar/get/ask/question/list/',methods=['GET','POST'])
def APiGetdataask():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		code=userinfo['seminarId']
		user_data = dbhelper.GetData().getasklistAll(code)
		print user_data
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				if line[1]=='':
					user_data_dict['name'] ='Anonymus'
				else:
					user_data_dict['name']=line[1]
				
				user_data_dict['mobile']=line[2]
				user_data_dict['question']=line[3]
				user_data_dict['seminarId']=line[4]
				user_data_dict['date']=line[5]
				user_data_dict['time']=line[6]
				user_data_dict['status']=line[7]
				user_data_dict['points']=line[8]
				user_data_dict['imageName']='https://storage.googleapis.com/seminar-efe78.appspot.com/LiveSeminarImage/'+str(line[9])
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)  

# user list
@app.route('/seminar/get/user/details/',methods=['GET','POST'])
def APiGetUserDetails():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile=userinfo['mobile']
		user_data = dbhelper.GetData().getuserdeatisl(mobile)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['name'] =line[1]
				user_data_dict['email']=line[2]
				user_data_dict['mobile']=line[3]
				user_data_dict['dob']=line[4]
				user_data_dict['gender']=line[5]
				user_data_dict['designation1']=line[6]
				user_data_dict['designation2']=line[7]
				user_data_dict['designation3']=line[8]
				user_data_dict['designation4']=line[9]
				user_data_dict['qualification1']=line[10]
				user_data_dict['qualification2']=line[11]
				user_data_dict['qualification3']=line[12]
				user_data_dict['qualification4']=line[13]
				user_data_dict['qualificationYear1']=line[14]
				user_data_dict['qualificationYear2']=line[15]
				user_data_dict['qualificationYear3']=line[16]
				user_data_dict['qualificationYear4']=line[17]
				user_data_dict['affiliations1']=line[18]
				user_data_dict['affiliations2']=line[19]
				user_data_dict['affiliations3']=line[20]
				user_data_dict['affiliations4']=line[21]
				user_data_dict['designationYear1']=line[22]
				user_data_dict['designationYear2']=line[23]
				user_data_dict['designationYear3']=line[24]
				user_data_dict['designationYear4']=line[25]
				user_data_dict['imageName']=line[26]
				user_data_dict['imageUrl']='https://storage.googleapis.com/seminar-efe78.appspot.com/registration/'
				user_data_dict['registrationNo']=line[27]

				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/seminar/user/details/',methods=['GET','POST'])
def APiGetUserDet():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getuserdea()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['name'] =line[1]
				user_data_dict['email']=line[2]
				user_data_dict['mobile']=line[3]
				user_data_dict['dob']=line[4]
				user_data_dict['gender']=line[5]
				user_data_dict['designation1']=line[6]
				user_data_dict['designation2']=line[7]
				user_data_dict['designation3']=line[8]
				user_data_dict['designation4']=line[9]
				user_data_dict['qualification1']=line[10]
				user_data_dict['qualification2']=line[11]
				user_data_dict['qualification3']=line[12]
				user_data_dict['qualification4']=line[13]
				user_data_dict['qualificationYear1']=line[14]
				user_data_dict['qualificationYear2']=line[15]
				user_data_dict['qualificationYear3']=line[16]
				user_data_dict['qualificationYear4']=line[17]
				user_data_dict['affiliations1']=line[18]
				user_data_dict['affiliations2']=line[19]
				user_data_dict['affiliations3']=line[20]
				user_data_dict['affiliations4']=line[21]
				user_data_dict['designationYear1']=line[22]
				user_data_dict['designationYear2']=line[23]
				user_data_dict['designationYear3']=line[24]
				user_data_dict['designationYear4']=line[25]
				user_data_dict['imageName']=line[26]
				user_data_dict['imageUrl']='https://storage.googleapis.com/seminar-efe78.appspot.com/registration/'
				user_data_dict['registrationNo']=line[27]
				seminar_data = dbhelper.GetData().getSeminarStatusData(line[3],seminarId)
				try:
					seminarstatus = seminar_data[0][0]
				except:
					seminarstatus =0

				user_data_dict['status']=seminarstatus

				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)
# get help line
@app.route('/seminar/add/help/',methods=['GET','POST'])
def APiadduserhelp():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		mobile=userinfo['mobile']
		email=userinfo['email']
		seminarId=userinfo['seminarId']

		AddUser = dbhelper.AddData().addUserhelp(mobile,email,seminarId)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)

@app.route('/seminar/get/help/line/',methods=['GET','POST'])
def APiGethelpLine():
	if request.method=='POST':
		helpinfo   = json.loads(request.data)
		seminarId=helpinfo['seminarId']
		seminarCode = dbhelper.GetData().getseminarCode(seminarId)[0][0]

		help_data = dbhelper.GetData().getseminarhelp(seminarCode)
		help_data_db=[]
		if(len(help_data))>0:
			for line in help_data:
				help_data_dict={}
				help_data_dict['id']  = line[0]
				help_data_dict['mobile']=line[1]
				help_data_dict['email']=line[2]
				help_data_dict['seminarId']=line[3]
				
				help_data_db.append(help_data_dict)
				
		resp = Response(json.dumps({"success": True, "help_data": help_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

# points
@app.route('/seminar/get/ask/question/list/all/',methods=['GET','POST'])
def APiGetdataaskAll():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		code=userinfo['seminarId']
		user_data = dbhelper.GetData().getasklist(code)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				if line[1]=='':
					user_data_dict['name'] ='Anonymus'
				else:
					user_data_dict['name']=line[1]
				
				user_data_dict['mobile']=line[2]
				user_data_dict['question']=line[3]
				user_data_dict['seminarId']=line[4]
				user_data_dict['date']=line[5]
				user_data_dict['time']=line[6]
				user_data_dict['status']=line[7]
				user_data_dict['points']=line[8]
				user_data_dict['imageName']='https://storage.googleapis.com/seminar-efe78.appspot.com/LiveSeminarImage/'+str(line[9])
				user_data_dict['pointType']=line[11]

				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)  

 

@app.route('/seminar/get/agenda/image/',methods=['GET','POST'])
def APiGetAgendaImage():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getAgendaImage(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['agenda']  = line[1]
				user_data_dict['seminarId']=line[2]
				user_data_dict['topic']=line[3]
				user_data_dict['speaker']=line[4]
				user_data_dict['startTime']=line[5]
				user_data_dict['endTime']=line[6]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "agenda_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/seminar/get/payment/',methods=['GET','POST'])
def APiGetpayment():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile=userinfo['mobile']
		user_data = dbhelper.GetData().getfinalpayment(mobile)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['name']  = line[1]
				user_data_dict['address']=line[2]
				user_data_dict['seminarCode']=line[3]
				user_data_dict['date']=line[4]
				user_data_dict['amount']=line[5]
				user_data_dict['status']=line[6]
				user_data_dict['mobile']=line[7]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "agenda_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/seminar/get/payment/byseminar/',methods=['GET','POST'])
def APiGetpaymentbySem():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile=userinfo['mobile']
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getpaymentbySeminar(mobile,seminarId)
		try:
			name = user_data[0][0]
			paymentStatus = 1
		except:
			name =''
			paymentStatus = 0

				
		resp = Response(json.dumps({"success": True, "name": name , "mobile":mobile,"seminarId":seminarId,"paymentStatus":paymentStatus }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/seminar/update/payment/',methods=['GET','POST'])
def APiupdatepayment():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		print userInfo
		name=userInfo['name']
		address=userInfo['address']
		seminarCode=userInfo['seminarCode']
		seminarId=userInfo['seminarId']
		date=userInfo['date']
		amount=userInfo['amount']
		status=userInfo['status']
		mobile=userInfo['mobile']
		AddUser = dbhelper.AddData().addPayment(name,address,seminarCode,date,amount,status,mobile,seminarId)
		# EditAssign = dbhelper.aData().Updatepayment(name,address,seminarCode,date,amount,status,mobile)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response":"success","response": db}))
		return after_request(resp)				  


@app.route('/seminar/add/agenda/',methods=['GET','POST'])
def APiaddagenda():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		sessionName=userinfo['sessionName']
		topic=userinfo['topic']
		tTime=userinfo['tTime']
		time=userinfo['time']
		speaker=userinfo['speaker']
		chairperson=userinfo['chairperson']
		hall=userinfo['hall']
		seminarId=userinfo['seminarId']
		date=userinfo['date']
		time2=userinfo['time2']
		time3=userinfo['time3']
		time4=userinfo['time4']
		userId = userinfo['userId']
		
		lastId             =dbhelper.GetData().getPartnerLastID()[0][0]
		if lastId:
			newid=str(123+lastId)
		else:
			newid=str(123)

		topicId = 'SEM' + newid
		

		AddUser = dbhelper.AddData().addAgenda(sessionName,topic,tTime,time,speaker,chairperson,hall,seminarId,date,time2,time3,time4,userId,topicId)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)


@app.route('/seminar/get/polls/question/',methods=['GET','POST'])
def APiGetPollsQues():
	if request.method=='POST':
		
		user_data = dbhelper.GetData().getQuestionPoll()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['seminarId']=line[1]
				user_data_dict['questionId']=line[2]
				user_data_dict['questionType']=line[3]
				user_data_dict['question']=line[4]
				user_data_dict['option1']=line[5]
				user_data_dict['option2']=line[6]
				user_data_dict['option3']=line[7]
				user_data_dict['option4']=line[8]
				user_data_dict['status']=line[10]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "poll_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)  


@app.route('/seminar/add/seminar/rating/',methods=['GET','POST'])
def APiaddSeminarRate():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		mobile=userinfo['mobile']
		rating=userinfo['rating']
		comment=userinfo['comment']
		seminarCode=userinfo['seminarCode']
		topicId=userinfo['topicId']
		overAllExperience=userinfo['overAllExperience']
		conferenceInterest=userinfo['conferenceInterest']
		mostInterestedTopic=userinfo['mostInterestedTopic']
		mostBoringTopic=userinfo['mostBoringTopic']
		mostInformativeTopic=userinfo['mostInformativeTopic']
		sessionShouldShorter=userinfo['sessionShouldShorter']
		whowasBestPresenter=userinfo['whowasBestPresenter']
		likeToatrendAgain=userinfo['likeToatrendAgain']
		wasAppUseful=userinfo['wasAppUseful']
		
		
		AddUser = dbhelper.AddData().addUserRating(mobile,rating,comment,seminarCode,topicId,overAllExperience,conferenceInterest,mostInterestedTopic,mostBoringTopic,mostInformativeTopic,sessionShouldShorter,whowasBestPresenter,likeToatrendAgain,wasAppUseful)
		db={'message':'Rating Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)


@app.route('/seminar/add/quiz/response/',methods=['GET','POST'])
def APiaddQuizRes():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile=userinfo['mobile']
		seminarId=userinfo['seminarId']
		questionId=userinfo['questionId']
		answer=userinfo['answer']
		correct=userinfo['correct']
		if answer == correct:

			AddUser = dbhelper.AddData().addPointQuizPoint(mobile,seminarId,10)
			AddUser = dbhelper.AddData().addQuizPoint(mobile,seminarId,questionId,answer,correct)
			AddUser2 = dbhelper.AddData().addQuizResp(mobile,seminarId,questionId,answer,correct)

		else:
			AddUser = dbhelper.AddData().addQuizResp(mobile,seminarId,questionId,answer,correct)
		db={'message':'Rating Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)


@app.route('/seminar/user/attendance/',methods=['GET','POST'])
def APiUserAttendance():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile=userinfo['mobile']
		seminarId=userinfo['seminarId']
		name=userinfo['name']
		strDate    = str(date.today())
		dateNow   = datetime.strptime(strDate, "%Y-%m-%d").strftime("%d/%m/%Y")
		current_time              = (datetime.now() + timedelta(hours=05,minutes=30)).strftime("%H:%M")
		AddUser = dbhelper.AddData().addAttendance(mobile,seminarId,name,dateNow,current_time)
			
		db={'message':'Rating Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)

@app.route('/seminar/get/seminar/user/',methods=['GET','POST'])
def APiGetSeminarUserD():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getSminarUserData(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['registerd']  = line[0]
				user_data_dict['present']=line[1]
				user_data_dict['seminarId']=seminarId
				seminar_name = dbhelper.GetData().getSeminarName(seminarId)[0][0]
				user_data_dict['seminar_name']=seminar_name
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "seminar_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp) 


@app.route('/seminar/get/rating/',methods=['GET','POST'])
def APiGetAgendaRating():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getRating(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['mobile']=line[1]
				user_data_dict['rating']=line[2]
				user_data_dict['comment']=line[3]
				user_data_dict['seminarId']=line[4]
				user_data_dict['topicId']  = line[5]
				user_data_dict['overAllExperience']=line[6]
				user_data_dict['conferenceInterest']=line[7]
				user_data_dict['mostInterestedTopic']=line[8]
				user_data_dict['mostBoringTopic']=line[9]
				user_data_dict['mostInformativeTopic']  = line[10]
				user_data_dict['sessionShouldShorter']=line[11]
				user_data_dict['whowasBestPresenter']=line[12]
				user_data_dict['likeToatrendAgain']=line[13]
				user_data_dict['wasAppUseful']=line[14]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "rating_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)  


@app.route('/seminar/get/active/time/',methods=['GET','POST'])
def APiGetActiveTime():
	if request.method=='GET':
		user_data = dbhelper.GetData().getPollDate()
		now  = datetime.now()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				print line[1]
				time = now - line[1]
				
				duration_in_s = time.total_seconds() 
				print duration_in_s
				# datetime.timedelta(seconds=1):
				if time > timedelta(seconds=15):
					out=dbhelper.UpdateData().updatePoll2(line[0],now)
					print out
					if out==0:
						d={"confirmation":1}
					else:
						d={"confirmation":0}
				else:
					pass
				# user_data_db.append(user_data_dict)
				
	resp = Response(json.dumps({"success": True }))
	resp.headers['Content-type']='application/json'
	return after_request(resp)


@app.route('/seminar/get/ranking/summary/',methods=['GET','POST'])
def APiGetSeminarSumkRanking():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile=userinfo['mobile']
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getSeminatRanking(seminarId)
		user_data_db=[]
		count=0
		self_ranking=0
		for line in user_data:
			count=count+1
			user_data_dict={}       
			user_data_dict['name']=line[0]
			user_data_dict['mobile']=line[1]
			user_data_dict['totalPoints']=str(line[2])
			user_data_dict['ranking']=count

			if line[1]==mobile:
				self_ranking = count
			user_data_db.append(user_data_dict)


		resp = Response(json.dumps({"success": True, "user_data": user_data_db, "self_ranking": self_ranking }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)  


@app.route('/seminar/get/seminar/view/',methods=['GET','POST'])
def APiGetSeminarView():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		total_user = dbhelper.GetData().getSeminatSum(seminarId)[0][0]
		total_user2 = dbhelper.GetData().getSeminatPart(seminarId)[0][0]
		user_data_db=[]
		
		user_data_dict={}       
		user_data_dict['total_user']=total_user
		user_data_dict['total_user2']=total_user2
		
		user_data_db.append(user_data_dict)


		resp = Response(json.dumps({"success": True, "user_data": user_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)  




# call
@app.route('/seminar/get/seminar/summary/',methods=['GET','POST'])
def APiGetSeminarSumk():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		mobile=userinfo['mobile']
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getSeminatCount(mobile, seminarId)
		try:
			user_name = dbhelper.GetData().getUserName(mobile)[0][0]
		except:
			user_name=''
		seminar_name = dbhelper.GetData().getSeminarName(seminarId)
		selected_ques = dbhelper.GetData().getSelectedque(seminarId)[0][0]

		getTotalPoint = dbhelper.GetData().getTotalPoints(mobile, seminarId)
		
		user_data_db=[]
		if(len(seminar_name))>0:
			for line in seminar_name:
				seminar_name_dict={}
				
				
				seminar_name_dict['name']=user_name
				seminar_name_dict['mobile']=mobile
				try:
					seminar_name_dict['totalPoints']=getTotalPoint[0][1]
				except:
					seminar_name_dict['totalPoints']=0


				try:
					seminar_name_dict['totalquestion']=user_data[0][1]

				except:
					seminar_name_dict['totalquestion']=0


				seminar_name_dict['seminar_name']=seminar_name[0][0]
				seminar_name_dict['selected_ques']=selected_ques

				user_data_db.append(seminar_name_dict)

		
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)  


@app.route('/seminar/get/points/data/',methods=['GET','POST'])
def APiGetPointsData():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		code=userinfo['seminarId']
		user_data = dbhelper.GetData().getPointlist(code)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['mobile']=line[1]
				user_data_dict['seminarId']=line[2]
				user_data_dict['acceptedQ']=line[3]
				user_data_dict['correctA']=line[4]
				user_data_dict['livePoll']=line[5]
				user_data_dict['sessionFeedback']=line[6]
				user_data_dict['seminarFeedback']=line[7]
				user_data_dict['totalPoint']=int(line[3])+int(line[4])+int(line[5])+int(line[6])+int(line[7])
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp) 
		


# seminar
@app.route('/seminar/get/seminar/topic/',methods=['GET','POST'])
def APiGetSeminarTopic():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getSeminarTopic(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				
				
				user_data_dict['agenda']=line[1]
				user_data_dict['seminarId']=line[7]
				user_data_dict['topic']=line[3]
				user_data_dict['date']=str(line[11])
				user_data_dict['facuiltyName']=line[5]
				user_data_dict['time']=line[4]

				# user_data_dict['time']=line[4]
				
				user_data_db.append(user_data_dict)
		resp = Response(json.dumps({"success": True, "seminar_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)  


@app.route('/seminar/live/pooling/',methods=['GET','POST'])
def APiGetlivePool():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		now  = datetime.now()
		questionType = dbhelper.GetData().getQuestionType(seminarId)
		try:
			
			questionId=questionType[0][0]
			questionType=questionType[0][1]
		except:
			questionId=''
			questionType=''

		if questionType =='MULTIPLE':

			user_data = dbhelper.GetData().getpool(seminarId,questionId)
			user_data_db=[]
			if(len(user_data))>0:
				for line in user_data:
					user_data_dict={}
					user_data_dict['id']  = line[0]
					
					user_data_dict['seminarId']=line[1]
					user_data_dict['questionId']=line[2]
					user_data_dict['questionType']=line[3]
					user_data_dict['question']=line[4]
					user_data_dict['option1']=line[5]
					user_data_dict['option2']=line[6]
					user_data_dict['option3']=line[7]
					user_data_dict['option4']=line[8]
					# user_data_dict['id']  = line[0]
					time = now - line[16]
					
					duration_in_s = time.total_seconds() 
					print duration_in_s
					# datetime.timedelta(seconds=1):
					if time > timedelta(seconds=20):
						out=dbhelper.UpdateData().updatePoll2(line[0],now)
						print out
						if out==0:
							d={"confirmation":1}
						else:
							d={"confirmation":0}
					else:
						pass
					user_data_dict['status']=line[10]

					user_data_db.append(user_data_dict)

		if questionType =='TEXT':
			user_data = dbhelper.GetData().getpool(seminarId,questionId)
			user_data_db=[]
			if(len(user_data))>0:
				for line in user_data:
					user_data_dict={}
					user_data_dict['id']  = line[0]
					
					user_data_dict['seminarId']=line[1]
					user_data_dict['questionId']=line[2]
					user_data_dict['questionType']=line[3]
					user_data_dict['question']=line[4]
					user_data_db.append(user_data_dict)

		
				
		try:
			resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		except:
			resp = Response(json.dumps({"success": True, "user_data": [] }))
			resp.headers['Content-type']='application/json'
			return after_request(resp)



@app.route('/seminar/get/live/pooling/',methods=['GET','POST'])
def APiGetlivePPool():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getQuestionLivePool(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
								
				user_data_dict['questionId']=line[0]
				user_data_dict['option1']=line[1]
				user_data_dict['option2']=line[2]
				user_data_dict['option3']=line[3]
				user_data_dict['option4']=line[4]
				user_data_dict['question']=line[5]
				try:
					summary = dbhelper.GetData().getQuestionLivePool2(line[0],line[1],line[2],line[3],line[4])
				except:
					summary=0
				try:
					user_data_dict['opt1']=summary[0][0]
					user_data_dict['opt2']=summary[0][1]
					user_data_dict['opt3']=summary[0][2]
					user_data_dict['opt4']=summary[0][3]
				except:
					user_data_dict['opt1']=0
					user_data_dict['opt2']=0
					user_data_dict['opt3']=0
					user_data_dict['opt4']=0


				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/seminar/get/question/pooling/',methods=['GET','POST'])
def APiGetQuePPool():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		questionId=userinfo['questionId']
		user_data = dbhelper.GetData().getQuestionPool(questionId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
								
				user_data_dict['questionId']=line[0]
				user_data_dict['option1']=line[1]
				user_data_dict['option2']=line[2]
				user_data_dict['option3']=line[3]
				user_data_dict['option4']=line[4]
				user_data_dict['question']=line[5]
				try:
					summary = dbhelper.GetData().getQuestionLivePool2(line[0],line[1],line[2],line[3],line[4])
				except:
					summary=0
				try:
					user_data_dict['opt1']=summary[0][0]
					user_data_dict['opt2']=summary[0][1]
					user_data_dict['opt3']=summary[0][2]
					user_data_dict['opt4']=summary[0][3]
				except:
					user_data_dict['opt1']=0
					user_data_dict['opt2']=0
					user_data_dict['opt3']=0
					user_data_dict['opt4']=0


				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/seminar/get/pooling/',methods=['GET','POST'])
def APiGetlive2PPool():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		pollId= userinfo['pollId']
		mobile= userinfo['mobile']
		poll_status= dbhelper.GetData().getPoolStatus(seminarId,pollId,mobile)
		user_data = dbhelper.GetData().getQueLivePool(seminarId,pollId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
								
				user_data_dict['questionId']=line[0]
				user_data_dict['option1']=line[1]
				user_data_dict['option2']=line[2]
				user_data_dict['option3']=line[3]
				user_data_dict['option4']=line[4]
				user_data_dict['question']=line[5]
				# user_data_dict['participateStatus']=poll_status
				try:
					summary = dbhelper.GetData().getQuestionLivePool2(line[0],line[1],line[2],line[3],line[4])
				except:
					summary=0
				try:
					user_data_dict['opt1']=summary[0][0]
					user_data_dict['opt2']=summary[0][1]
					user_data_dict['opt3']=summary[0][2]
					user_data_dict['opt4']=summary[0][3]
				except:
					user_data_dict['opt1']=0
					user_data_dict['opt2']=0
					user_data_dict['opt3']=0
					user_data_dict['opt4']=0


				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db,"participateStatus":poll_status }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/seminar/question/pooling/',methods=['GET','POST'])
def APiGetQuestionPool():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		
		user_data = dbhelper.GetData().getQusetionpool(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				
				user_data_dict['seminarId']=line[1]
				user_data_dict['questionId']=line[2]
				try:
					vote = dbhelper.GetData().getCountVote(seminarId,questionId)[0][0]
				except:
					vote =0
				if line[3]=='MULTIPLE':
					user_data_dict['questionType']='POLL'
				else:
					user_data_dict['questionType']=line[3]

				user_data_dict['vote']=vote
				user_data_dict['question']=line[4]
				user_data_dict['option1']=line[5]
				user_data_dict['option2']=line[6]
				user_data_dict['option3']=line[7]
				user_data_dict['option4']=line[8]
				user_data_dict['status']=line[10]
				user_data_dict['seminar_status']=line[11]
				user_data_dict['imageName']='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Profile/'+str(line[13])
				user_data_dict['quesStatus']=line[14]

				user_data_db.append(user_data_dict)

		
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/seminar/quiz/question/',methods=['GET','POST'])
def APiGetQuizQues():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		mobile=userinfo['mobile']

		
		user_data = dbhelper.GetData().getQuizQues(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				
				user_data_dict['seminarId']=line[1]
				user_data_dict['questionId']=line[2]
				
				anwer = dbhelper.GetData().getQuizAnswer(mobile,line[2])
				try:
					anwer_data = anwer[0][0]
					quesStatus= anwer[0][1]
				except:
					anwer_data =''
					quesStatus = 0
				user_data_dict['questionType']=line[3]
				# user_data_dict['vote']=vote
				user_data_dict['question']=line[4]
				user_data_dict['option1']=line[5]
				user_data_dict['option2']=line[6]
				user_data_dict['option3']=line[7]
				user_data_dict['option4']=line[8]
				user_data_dict['status']=line[10]
				user_data_dict['seminar_status']=line[11]
				user_data_dict['correctAnswer']=line[12]
				user_data_dict['imageName']=line[13]
				user_data_dict['imageUrl']='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Profile/'
				user_data_dict['quesStatus']=quesStatus
				user_data_dict['answer']=anwer_data

				user_data_db.append(user_data_dict)

		
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/seminar/add/pooling/answer/',methods=['GET','POST'])
def APiaddpoolinganswer():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		seminarId=userinfo['seminarId']
		mobile=userinfo['mobile']
		questionId=userinfo['questionId']
		answer=userinfo['answer']
		
		
		AddUser = dbhelper.AddData().addUserlistB(seminarId,mobile,questionId,answer)
		addPointsForPoll = dbhelper.AddData().addPointLivePollPoint(mobile,seminarId,10)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)                  


# @app.route('/seminar/add/pooling/answer/',methods=['GET','POST'])
# def APiaddpoolinganswer2():
#   if request.method=='POST':
#       userinfo   = json.loads(request.data)
		
		
#       seminarId=userinfo['seminarId']
#       mobile=userinfo['mobile']
#       questionId=userinfo['questionId']
#       answer=userinfo['answer']
		
		
#       AddUser = dbhelper.AddData().addUserlistB(seminarId,mobile,questionId,answer)
#       db={'message':'User Added',"confirmation":1}
		
#       resp = Response(json.dumps({"response":"success"}))
#       return after_request(resp)                  



@app.route('/seminar/add/seminar/data/',methods=['GET','POST'])
def APiaddSeminarlistA():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		#name=userinfo['name']
		mobile=userinfo['mobile']
		seminarId=userinfo['seminarId']
		# userId=userinfo['userId']

		try:
			imageName=userinfo['imageName']
		except:
			imageName=''
		
		code = dbhelper.GetData().getSminarCode(seminarId)[0][0]
		
		text ="Your+Seminar+Code+is+%s."%(str(code))

		url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=INOBIN&mobile=%s&msg=%s'%(str(mobile),text)
		print url
		urlfetch.set_default_fetch_deadline(45)
		resp = urlfetch.fetch(url=url,
			method=urlfetch.GET,
			headers={'Content-Type': 'text/html'})
		AddUser = dbhelper.AddData().addSeminarCode(mobile,seminarId,code,imageName)

		respp = Response(json.dumps({"response": "success","confirmation":1}))
		return after_request(respp)

@app.route('/seminar/check/seminar/data/',methods=['GET','POST'])
def APiaddSeminarlist():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		code=userinfo['seminarCode']
		mobile=userinfo['mobile']
		seminarId=userinfo['seminarId']
		
		last = dbhelper.GetData().getSemainarverify(seminarId,code)
		if last==True:
			AddSeminar = dbhelper.AddData().addseminar_data(mobile,seminarId,code)

			db={'message':'Seminarcode Verified',"confirmation":1}  
			resp = Response(json.dumps({"response": db}))
			return after_request(resp)
		else:
			db={'message':'Seminarcode Not Verified',"confirmation":0}  
			resp = Response(json.dumps({"response": db}))
			return after_request(resp)



@app.route('/seminar/add/seminar/message/',methods=['GET','POST'])
def APiaddMessage():

	if request.method    == 'POST':
		userinfo   = json.loads(request.data)
		print userinfo
		topic= userinfo['topic']
		message= userinfo['message']
		seminarId= userinfo['seminarId']
		dateNow           = str(date.today())
		time              = (datetime.now() + timedelta(hours=05,minutes=30)).strftime("%H:%M")
		fcmTokenList         =dbhelper.GetData().getToken(seminarId)
		
		AddSeminar = dbhelper.AddData().addMessage(topic,message,seminarId)
		if len(fcmTokenList)>0:
			for gcmT in fcmTokenList:			   
				message_data={   "notification":{"action":"Notification","body":message,"title":topic,"type":0,"imageUrl":"http://s33.postimg.org/slnc2rtwv/logo.png"},
							
						"to" : gcmT[2]
				}
				form_data = json.dumps(message_data)

				

				url='https://fcm.googleapis.com/fcm/send'
				urlfetch.set_default_fetch_deadline(45)

				resp = urlfetch.fetch(url=url,
					method=urlfetch.POST,
					payload=form_data,
					headers={"Authorization":"key=AAAAXVC0h0g:APA91bGZ0JdiYz-9Qk6dZKJXd9k9DelhSB6X2GPcmn2r-loRxHuWUpMqN7wzXR_rYLVwgxPQj0o81wq1rbSxt4eBXv0uy6tXgwmlWHPjRbBhZHSUA5TrqqgDEk_MMIYZVpee2MQhkzZu", "Content-Type":"application/json"}
					)

				print resp.content
		
			response = Response(json.dumps({"response":{"confirmation": 1}}))
			return after_request(response)

		else:
			response = Response(json.dumps({"response":{"confirmation": 0}}))
			return after_request(response)



@app.route('/seminar/advertise/seminar/',methods=['GET','POST'])
def APiAdvertise():

	if request.method    == 'POST':
		userinfo   = json.loads(request.data)
		message= userinfo['message']
		seminarId= userinfo['seminarId']
		seminarName= userinfo['seminarName']
		imageName = userinfo['imageName']
		image='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Profile/'+str(imageName)
		dateNow           = str(date.today())
		time              = (datetime.now() + timedelta(hours=05,minutes=30)).strftime("%H:%M")
		fcmTokenList         =dbhelper.GetData().getToken(seminarId)
		print fcmTokenList
		
		AddSeminar = dbhelper.AddData().addSeminarAdvert(message,seminarId,seminarName,imageName)
		if len(fcmTokenList)>0:
			for gcmT in fcmTokenList:			   
				message_data={   "data":{"action":"Notification","body":message,"seminarName":seminarName,"type":1,"imageName":image},
							
						"to" : gcmT[2]
				}
				print message_data
				form_data = json.dumps(message_data)

				

				url='https://fcm.googleapis.com/fcm/send'
				urlfetch.set_default_fetch_deadline(45)

				resp = urlfetch.fetch(url=url,
					method=urlfetch.POST,
					payload=form_data,
					headers={"Authorization":"key=AAAAXVC0h0g:APA91bGZ0JdiYz-9Qk6dZKJXd9k9DelhSB6X2GPcmn2r-loRxHuWUpMqN7wzXR_rYLVwgxPQj0o81wq1rbSxt4eBXv0uy6tXgwmlWHPjRbBhZHSUA5TrqqgDEk_MMIYZVpee2MQhkzZu", "Content-Type":"application/json"}
					)

				print resp.content
		
			response = Response(json.dumps({"response":{"confirmation": 1}}))
			return after_request(response)

		else:
			response = Response(json.dumps({"response":{"confirmation": 0}}))
			return after_request(response)

@app.route('/seminar/add/seminar/document/',methods=['GET','POST'])
def APiaddDocument():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		documentType=userinfo['documentType']

		image= userinfo['image'].replace(" ","_")
		name=userinfo['name']
		description=userinfo['description']
		userId=userinfo['userId']
		if documentType=='Registration':
			AddSeminar = dbhelper.AddData().addRegistrationDocument(seminarId,image,userId)
		else:
			pass

		docs_data = dbhelper.GetData().getDocsDocument(seminarId,documentType)
		if docs_data== True:
			out=dbhelper.UpdateData().updateDocs(seminarId,documentType,image,name,description,userId)

		else:
			AddSeminar = dbhelper.AddData().addDocument(seminarId,documentType,image,name,description,userId)



		db={'message':'Seminarcode Verified',"confirmation":1}  
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/seminar/add/seminar/images/',methods=['GET','POST'])
def APiaddImages():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		image1=userinfo['imageName1']
		image2=userinfo['imageName2']
		image3=userinfo['imageName3']
		image4=userinfo['imageName4']
		image5=userinfo['imageName5']
		image6=userinfo['imageName6']
		image7=userinfo['imageName7']

		docs_data = dbhelper.GetData().getDocsImages(seminarId)
		if docs_data== True:
			out=dbhelper.UpdateData().updateDocsImages(seminarId,image1,image2,image3,image4,image5,image6,image7)

		else:
			AddSeminar = dbhelper.AddData().addDocumentImage(seminarId,image1,image2,image3,image4,image5,image6,image7)



		db={'message':'Images Added',"confirmation":1}  
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)
@app.route('/seminar/user/seminar/join/',methods=['GET','POST'])
def APiUserSeminarJoin():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		mobile=userinfo['mobile']
		
		pdf_data2 = dbhelper.GetData().getBrocher(seminarId)
		print pdf_data2
		try:
			pdf_data= pdf_data2[0][0]

		except:
			pdf_data ='Qatar.pdf'
		pdfUrl='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Profile/'+str(pdf_data)

		docs_data = dbhelper.GetData().getUserRegisterStatus(seminarId,mobile)
		if docs_data== True:
			status=1

		else:
			status=0

		db={'message':'Seminar Status',"confirmation":1,'status':status,'pdfUrl':pdfUrl}  
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/seminar/get/seminar/docs/',methods=['GET','POST'])
def APiGetdocs():
	if request.method=='POST':
		user_data = dbhelper.GetData().getDocs()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['name']=line[1]
				user_data_dict['mobile']=line[2]
				user_data_dict['image']='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Profile/'+str(line[3])
				
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)
		
			
@app.route('/seminar/get/admin/seminar/list/',methods=['POST'])
def APiGetAdminlist():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		userId=userinfo['userId']
		user_data = dbhelper.GetData().getAdminlist(userId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				try:
					brocher_data = dbhelper.GetData().getBrocher(line[0])[0][0]
				except:
					brocher_data=''
				user_data_dict['seminarName']=line[1]
				

				date_object = datetime.strptime(line[2], '%d/%m/%Y')
				saurabh =date_object.strftime('%d %b')
				user_data_dict['seminarDate']=saurabh
				# check_dict['date']=saurabh
				user_data_dict['location']=line[3]
				user_data_dict['seminarCode']=line[4]
				user_data_dict['mobile']=line[4]
				user_data_dict['status']=line[6]
				user_data_dict['seminar_status']=line[7]
				user_data_dict['imageName']='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Profile/'+str(line[8])
				user_data_dict['email']=line[9]
				date_object = datetime.strptime(line[10], '%d/%m/%Y')
				shivam =date_object.strftime('%d %b')
				user_data_dict['endDate']=shivam
				# user_data_dict['endDate']=line[9]
				try:
					pdf_data = dbhelper.GetData().getRegistrationForm(line[0])[0][1]
				except:
					pdf_data ='Qatar.pdf'
				user_data_dict['pdfUrl']='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Profile/'+str(pdf_data)
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)		
		
@app.route('/seminar/get/user/data/list/',methods=['GET','POST'])
def APiGetdatalist():
	if request.method=='POST':
		user_data = dbhelper.GetData().getDatalist()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				try:
					brocher_data = dbhelper.GetData().getBrocher(line[0])[0][0]
				except:
					brocher_data=''
				user_data_dict['seminarName']=line[1]
				

				date_object = datetime.strptime(line[2], '%d/%m/%Y')
				saurabh =date_object.strftime('%d %b')
				user_data_dict['seminarDate']=saurabh
				# check_dict['date']=saurabh
				user_data_dict['location']=line[3]
				user_data_dict['seminarCode']=line[4]
				user_data_dict['mobile']=line[4]
				user_data_dict['status']=line[6]
				user_data_dict['seminar_status']=line[7]
				user_data_dict['imageName']='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Profile/'+str(line[8])
				user_data_dict['email']=line[9]
				date_object = datetime.strptime(line[10], '%d/%m/%Y')
				shivam =date_object.strftime('%d %b')
				user_data_dict['endDate']=shivam
				# user_data_dict['endDate']=line[9]
				
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/seminar/get/pooling/answer/',methods=['GET','POST'])
def APiGetdataanswer():
	if request.method=='POST':
		user_data = dbhelper.GetData().getDatalistB()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['seminarId']=line[1]
				user_data_dict['mobile']=line[2]
				user_data_dict['questionId']=line[3]
				user_data_dict['answer']=line[4]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/seminar/get/lecturer/details/',methods=['GET','POST'])
def APiGetLecture():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getLecturer(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['seminarId']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['profileImage']=line[3]
				user_data_dict['designation']=line[4]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/seminar/get/agenda/Feedback/',methods=['GET','POST'])
def APiGetAgendaFeed():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getFeedbackagenda(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['mobile']  = line[0]
				user_data_dict['topicId']=line[1]
				user_data_dict['rating']=line[2]
				user_data_dict['sessionName']=line[3]
				comment_list=line[4].split("_")
				user_data_dict['comment']=comment_list[0]
				user_data_dict['comment1']=comment_list[1]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "session_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/seminar/get/agenda/details/',methods=['GET','POST'])
def APiGetAgenda():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		print seminarId
		user_data = dbhelper.GetData().getAgenda(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['agenda']  = line[1]
				user_data_dict['seminarId']=line[7]
				user_data_dict['topic']=line[3]
				user_data_dict['speaker']=line[5]
				user_data_dict['startTime']=line[4]
				user_data_dict['topicId']=line[6]
				user_data_dict['hall']=line[9]
				user_data_dict['chairperson']=line[10]
				user_data_dict['date']=str(line[11])
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "agenda_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/seminar/get/registration/form/',methods=['GET','POST'])
def APiGetRegistrationForm():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		print seminarId
		user_data = dbhelper.GetData().getRegistrationForm2(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['seminarId']=line[1]
				user_data_dict['imageUrl']='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Profile/'
				user_data_dict['imageName']=line[2]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "register_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/seminar/get/overall/rating/status/',methods=['GET','POST'])
def APiGetOverallStatus():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		mobile=userinfo['mobile']
		user_data = dbhelper.GetData().getoverallfeedback(seminarId,mobile)
		if user_data== True:
			status=1
		else:
			status=0
		
				
		resp = Response(json.dumps({"success": True, "status": status }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/seminar/get/session/rating/status/',methods=['GET','POST'])
def APiGetOverallSessionStatus():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		mobile=userinfo['mobile']
		topicId=userinfo['topicId']
		user_data = dbhelper.GetData().getsessionfeedback(seminarId,mobile,topicId)
		if user_data== True:
			status=1
		else:
			status=0
		
				
		resp = Response(json.dumps({"success": True, "status": status }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/seminar/get/seminar/sponser/',methods=['GET','POST'])
def APiGetSponser():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getSponser(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['seminarId']=line[1]
				user_data_dict['name']=line[5]
				user_data_dict['imageName']='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Profile/'+str(line[3])
				user_data_dict['description']=line[6]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "seminar_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/seminar/get/point/rule/',methods=['GET','POST'])
def APiGetPointRule():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().APiGetPointRule(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['seminarId']=line[1]
				user_data_dict['name']=line[5]
				user_data_dict['imageName']='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Profile/'+str(line[3])
				user_data_dict['description']=line[6]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "point_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/seminar/get/user/participate/',methods=['GET','POST'])
def APiGetPart():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile=userinfo['mobile']
		user_data = dbhelper.GetData().APiGetPart(mobile)
		user_name = dbhelper.GetData().APiUserName(mobile)[0][0]
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['mobile']  = mobile
				user_data_dict['seminarAttend']=line[0]
				user_data_dict['name']=user_name
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "point_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/seminar/get/seminar/users/',methods=['GET','POST'])
def APiGetSeminarUser():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getSeminaruser(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['mobile']  = line[0]
				user_data_dict['name']=line[1]
				user_data_dict['seminarId']=seminarId
				user_data_dict['email']=line[3]
				user_data_dict['imageName']=line[2]
				user_data_dict['imageUrl']='https://storage.googleapis.com/seminar-efe78.appspot.com/registration/'
				
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "seminar_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/seminar/get/notice/',methods=['GET','POST'])
def APiGetNotice():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getNotice(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['topic']=line[1]
				user_data_dict['message']=line[2]
				user_data_dict['seminarId']=seminarId
				
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "seminar_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/seminar/get/user/rank/',methods=['GET','POST'])
def APiGetranklist():
	if request.method=='POST':
		user_data = dbhelper.GetData().getranklist()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['seminarId']=line[1]
				user_data_dict['mobile']=line[2]
				user_data_dict['seminarName']=line[3]
				user_data_dict['rankOne']=line[4]
				user_data_dict['rankTwo']=line[5]
				user_data_dict['rankThired']=line[6]
				user_data_dict['score']=line[7]
				user_data_dict['userRank']=line[8]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)                                  


@app.route('/seminar/get/seminar/register/',methods=['GET','POST'])
def APiGetregisterSeminar():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		seminarId=userinfo['seminarId']
		user_data = dbhelper.GetData().getSeminarRegister(seminarId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['mobile']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['seminarId']=line[3]
				user_data_dict['code']=line[4]
				user_data_dict['imageName']=line[5]
				
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)                                  




# web version

@app.route('/seminar/active/polls/',methods=['GET','POST'])
def APiUploadProfile():
	if request.method=='POST':
		providerInfo  = json.loads(request.data)    
		Id = providerInfo['id'] 
		now  = datetime.now()
		out=dbhelper.UpdateData().updatePoll(Id,now)
		print out
		if out==0:
			d={"confirmation":1}
		else:
			d={"confirmation":0}
		
					
	resp = Response(json.dumps({"success": True}))
	return after_request(resp)


@app.route('/seminar/lock/polls/',methods=['GET','POST'])
def APiLockPolls():
	if request.method=='POST':
		providerInfo  = json.loads(request.data)    
		Id = providerInfo['id'] 
		out=dbhelper.UpdateData().updateLockPoll(Id)
		print out
		if out==0:
			d={"confirmation":1}
		else:
			d={"confirmation":0}
		
					
	resp = Response(json.dumps({"success": True}))
	return after_request(resp)


@app.route('/seminar/delete/session/',methods=['GET','POST'])
def APiDeleteSession():
	if request.method=='POST':
		providerInfo  = json.loads(request.data)    
		Id = providerInfo['Id'] 
		out =dbhelper.DeleteData().deleteSession(Id)
		print out
		if out==0:
			d={"confirmation":1}
		else:
			d={"confirmation":0}
		
					
	resp = Response(json.dumps({"success": True}))
	return after_request(resp)


@app.route('/seminar/update/user/profile/',methods=['GET','POST'])
def APiUserProfile():
	if request.method=='POST':
		providerInfo  = json.loads(request.data)    
		mobile = providerInfo['mobile'] 
		imageName= providerInfo['imageName']
		out=dbhelper.UpdateData().updateProfileImage(mobile,imageName)
		print out
		if out==0:
			d={"confirmation":1}
		else:
			d={"confirmation":0}
		
					
	resp = Response(json.dumps({"success": True}))
	return after_request(resp)

@app.route('/seminar/unlock/polls/',methods=['GET','POST'])
def APiUnlockProfile():
	if request.method=='POST':
		providerInfo  = json.loads(request.data)    
		Id = providerInfo['id'] 
		out=dbhelper.UpdateData().updateunLockPoll(Id)
		print out
		if out==0:
			d={"confirmation":1}
		else:
			d={"confirmation":0}
		
					
	resp = Response(json.dumps({"success": True}))
	return after_request(resp)

@app.route('/seminar/inactive/polls/',methods=['GET','POST'])
def APiInActive():
	if request.method=='POST':
		providerInfo  = json.loads(request.data)    
		Id = providerInfo['id'] 
		out=dbhelper.UpdateData().updateInPoll(Id)
		print out
		if out==0:
			d={"confirmation":1}
		else:
			d={"confirmation":0}
		
	resp = Response(json.dumps({"success": True}))
	return after_request(resp)



@app.route('/seminar/active/ques/',methods=['GET','POST'])
def APiActQue():
	if request.method=='POST':
		providerInfo  = json.loads(request.data)    
		Id = providerInfo['id'] 
		out=dbhelper.UpdateData().updateActQue(Id)
		getData = dbhelper.GetData().getQuestionInfo(Id)
		dbH =dbhelper.AddData().addPointAcceptedoint(getData[0][2], getData[0][4],10)
		if out==0:
			d={"confirmation":1}
		else:
			d={"confirmation":0}
		
					
	resp = Response(json.dumps({"success": True}))
	return after_request(resp)


@app.route('/seminar/deactive/ques/',methods=['GET','POST'])
def APiDeactQue():
	if request.method=='POST':
		providerInfo  = json.loads(request.data)    
		Id = providerInfo['id'] 
		out=dbhelper.UpdateData().updateDeQue(Id)
		print out
		if out==0:
			d={"confirmation":1}
		else:
			d={"confirmation":0}
		
					
	resp = Response(json.dumps({"success": True}))
	return after_request(resp)


@app.route('/seminar/get/session/list/',methods=['GET','POST'])
def ApiGetSeminarSession():
	if request.method=='POST':
		user_data =json.loads(request.data)
		seminarId=user_data['seminarId']
		hall=user_data['hall']
		date=user_data['date']
		print date
		session_info_data = dbhelper.GetData().GetSessionList(seminarId,hall,date)
		session_info_data_db = []
		if(len(session_info_data))>0:
			for line in session_info_data:
				session_info_data_dict = {}
				session_info_data_dict['sessionaName']=line[0]
				session_info_data_dict['time']=line[1]
				session_info_data_dict['chairPerson']=line[2]
				checkStringLst= dbhelper.GetData().SessionDetails(line[0],hall,date)
				# checkStringLst= data[13].split(',')
				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['topic'] = check[3]
					check_dict['tTime'] = check[4]
					check_dict['speaker'] = check[5]
					check_dict['topicId'] = check[6]
					check_dict['hall'] = check[9]
					check_dict['date']=check[11]
					date_object = datetime.strptime(date, '%d/%m/%Y')
					print(date_object.strftime('%d %B'))
					

					checkList.append(check_dict)

				session_info_data_dict['sessoinList']=checkList
				session_info_data_db.append(session_info_data_dict)

		resp = Response(json.dumps({"success": True, "session_data": session_info_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/seminar/get/session/total/',methods=['GET','POST'])
def ApiGetSeminarTotal():
	if request.method=='POST':
		user_data =json.loads(request.data)
		seminarId=user_data['seminarId']
		session_info_data = dbhelper.GetData().GetSessionListTotal(seminarId)
		session_info_data_db = []
		if(len(session_info_data))>0:
			for line in session_info_data:
				session_info_data_dict = {}
				session_info_data_dict['id']=line[0]
				session_info_data_dict['sessionaName']=line[1]
				session_info_data_dict['time']=line[2]
				session_info_data_dict['topic']=line[3]
				session_info_data_dict['tTime'] = line[4]
				session_info_data_dict['speaker'] = line[5]
				session_info_data_dict['topicId'] = line[6]
				session_info_data_dict['seminarId'] = line[7]
				session_info_data_dict['hall'] = line[9]
				session_info_data_dict['chairPerson']=line[10]
				session_info_data_dict['date']=str(line[11])
				session_info_data_dict['time2'] = line[12]
				session_info_data_dict['time3']=line[13]
				session_info_data_dict['time3']=line[14]
				session_info_data_db.append(session_info_data_dict)

		resp = Response(json.dumps({"success": True, "session_data": session_info_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/seminar/update/user/data/',methods=['GET','POST'])
def APiUserDatanew():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		print userInfo
		mobile=userInfo['mobile']
		designation1=userInfo['designation1']
		designation2=userInfo['designation2']
		designation3=userInfo['designation3']
		designation4=userInfo['designation4']
		qualification1=userInfo['qualification1']
		qualification2=userInfo['qualification2']
		qualification3=userInfo['qualification3']
		qualification4=userInfo['qualification4']
		qualificationYear1=userInfo['qualificationYear1']
		qualificationYear2=userInfo['qualificationYear2']
		qualificationYear3=userInfo['qualificationYear3']
		qualificationYear4=userInfo['qualificationYear4']
		affiliations1=userInfo['affiliations1']
		affiliations2=userInfo['affiliations2']
		affiliations3=userInfo['affiliations3']
		affiliations4=userInfo['affiliations4']
		designationYear1=userInfo['designationYear1']
		designationYear2=userInfo['designationYear2']
		designationYear3=userInfo['designationYear3']
		designationYear4=userInfo['designationYear4']

		
		EditAssign = dbhelper.UpdateData().Updateuserdata(mobile,	designation1,	designation2,	designation3,	designation4,	qualification1,	qualification2,	qualification3,	qualification4,	qualificationYear1,	qualificationYear2,	qualificationYear3,	qualificationYear4,	affiliations1,	affiliations2,	affiliations3,	affiliations4,	designationYear1,	designationYear2,	designationYear3,	designationYear4)
		db={'message':'UserDataUpdate',"confirmation":1}
			



					
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/seminar/get/certificate/list/',methods=['GET','POST'])
def ApiGetCertList():
	if request.method=='POST':
		user_data =json.loads(request.data)
		mobile = user_data['mobile']
		seminarId = user_data['seminarId']
		name = dbhelper.GetData().GetName(mobile)[0][0]
		session_info_data = dbhelper.GetData().GetSessionSeminar(seminarId)
		attendance = dbhelper.GetData().GetAttendanceStatus(mobile,seminarId)
		try:
			attend = attendance[0][0]
			status = 1
		except:
			status = 0
		address=session_info_data[0][0]
		date=session_info_data[0][1]

		certificate = create_cert.newtext%(name,address,date)
		

		resp = Response(json.dumps({"success": True, "session_data": certificate ,"status":status }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)		