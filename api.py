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

def SendMsg(mobile, Msg):
	text = Msg 
	m_phone="91"+str(mobile)
	url ='http://enterprise.smsgatewaycenter.com/SMSApi/rest/send'
	querystring = {"userId":"servtrans","password":"Tgb@12345","senderId":"SERVSM","sendMethod":"simpleMsg","msgType":"text","mobile":m_phone,"msg":text,"duplicateCheck":"true","format":"json"}
	params = urllib.urlencode(querystring)
	response = urllib2.urlopen(url, params)
	json_response = json.loads(response.read())

@app.after_request
def after_request(response):
	response.headers['Access-Control-Allow-Origin']='*'
	response.headers['Access-Control-Allow-Headers']='Content-Type, Authorization'
	response.headers['Access-Control-Allow-Methods']= 'GET, PUT, POST, DELETE'
	return response

	
	

################################ Post Login Teacher Diary ####################################

@app.route('/api/class/survey/',methods=['GET','POST'])
def APiaddsurvey():
	if request.method=='POST':
		employeeInfo   = json.loads(request.data)
		
		username           = employeeInfo['username']
		registeredStudent  = employeeInfo['registeredStudent']
		presentStudent     = employeeInfo['presentStudent']
		absentStudent      = employeeInfo['absentStudent']
		appointedTeacher   = employeeInfo['appointedTeacher']
		presentTeacher     = employeeInfo['presentTeacher']  
		absentTeacher      = employeeInfo['absentTeacher']
		studentStatus      = employeeInfo['studentStatus']
		punctualityStudent = employeeInfo['punctualityStudent']
		teacherStatus      = employeeInfo['teacherStatus']
		punctualityTeacher = employeeInfo['punctualityTeacher']
		classActivity      = employeeInfo['classActivity']
		conversation       = employeeInfo['conversation']
		relationship       = employeeInfo['relationship']
		studyMaterial      = employeeInfo['studyMaterial']
		studentExibition   = employeeInfo['studentExibition']
		groupWork          = employeeInfo['groupWork']
		Questions          = employeeInfo['Questions']
		studentSkills      = employeeInfo['studentSkills']
		lastActivity       = employeeInfo['lastActivity']
		Assignment         = employeeInfo['Assignment']
		assignmentMarks    = employeeInfo['assignmentMarks']
		lunchStatus        = employeeInfo['lunchStatus']
		lunchInspection    = employeeInfo['lunchInspection']
		Cleanliness        = employeeInfo['Cleanliness']
		drinkingWater      = employeeInfo['drinkingWater']
		toiletStatus       = employeeInfo['toiletStatus']
		ptmMeeting         = employeeInfo['ptmMeeting']
		ptmPresence        = employeeInfo['ptmPresence']
		dateTime           =datetime.now()
		
		AddTeacher = dbhelper.AddData().addclasssurvey(username,registeredStudent,presentStudent,absentStudent,appointedTeacher,presentTeacher,absentTeacher,studentStatus,punctualityStudent,teacherStatus,punctualityTeacher,classActivity,conversation,relationship,studyMaterial,studentExibition,groupWork,Questions,studentSkills,lastActivity,Assignment,assignmentMarks,lunchStatus,lunchInspection,Cleanliness,drinkingWater,toiletStatus,ptmMeeting,ptmPresence,dateTime)
		if AddTeacher==0:
			d=1
		else:
			d=0
				
	resp = Response(json.dumps({"success": d}))
	return after_request(resp)

@app.route('/api/school/details/',methods=['GET','POST'])
def APiaddschool():
	if request.method=='POST':
		employeeInfo   = json.loads(request.data)
		
		username    = employeeInfo['username']
		schoolName  = employeeInfo['schoolName']
		schoolCode  = employeeInfo['schoolCode']
		
		
		AddTeacher = dbhelper.AddData().addschooldetails(username,schoolName,schoolCode)

				
	resp = Response(json.dumps({"success": True}))
	return after_request(resp)






@app.route('/api/get/login/details/',methods=['GET','POST'])
def APigetlogin():
	if request.method=='POST':
		configure_data              = json.loads(request.data)
		username                    = configure_data['username']
		password                    = configure_data['password']
		
		
		lesson_info_data = dbhelper.GetData().getloginDetails(username,password)
		lesson_info_data_db = []

		if(len(lesson_info_data))>0:
			for line in lesson_info_data:
				lesson_info_data_dict = {}
				lesson_info_data_dict['id']            =line[0]
				lesson_info_data_dict['username']      =line[1]
				lesson_info_data_dict['Password']      =line[2]
				lesson_info_data_dict['name']          =line[3]
				lesson_info_data_dict['adminType']     =line[4]
				

				
				  
								
				lesson_info_data_db.append(lesson_info_data_dict)
		
			resp = Response(json.dumps({"success": 1,  "profData":lesson_info_data_db}))
		else:
			resp = Response(json.dumps({"success": 0}))
			
		resp.headers['Content-type']='application/json'
		return after_request(resp)




@app.route('/api/get/class/survey/',methods=['GET','POST'])
def APigetsurvey():
	if request.method=='POST':
		configure_data              = json.loads(request.data)
		username                    = configure_data['username']
	 
		lesson_info_data = dbhelper.GetData().getclasssurvey(username)
		lesson_info_data_db = []

		if(len(lesson_info_data))>0:
			for line in lesson_info_data:
				lesson_info_data_dict = {}
				lesson_info_data_dict['id']                =line[0]
				lesson_info_data_dict['username']          =line[1]
				lesson_info_data_dict['registeredStudent'] =line[2]
				lesson_info_data_dict['presentStudent']    =line[3]
				lesson_info_data_dict['absentStudent']     =line[4]
				lesson_info_data_dict['appointedTeacher']  =line[5]
				lesson_info_data_dict['presentTeacher']    =line[6]
				lesson_info_data_dict['absentTeacher']     =line[7]
				lesson_info_data_dict['studentStatus']     =line[8]
				lesson_info_data_dict['punctualityStudent']=line[9]
				lesson_info_data_dict['teacherStatus']     =line[10]
				lesson_info_data_dict['punctualityTeacher']=line[11]
				lesson_info_data_dict['classActivity']     =line[12]
				lesson_info_data_dict['conversation']      =line[13]
				lesson_info_data_dict['relationship']      =line[14]
				lesson_info_data_dict['studyMaterial']     =line[15]
				lesson_info_data_dict['studentExibition']  =line[16]
				lesson_info_data_dict['groupWork']         =line[17]
				lesson_info_data_dict['Questions']         =line[18]
				lesson_info_data_dict['studentSkills']     =line[19]
				lesson_info_data_dict['lastActivity']      =line[20]
				lesson_info_data_dict['Assignment']        =line[21]
				lesson_info_data_dict['assignmentMarks']   =line[22]
				lesson_info_data_dict['lunchStatus']       =line[23]
				lesson_info_data_dict['lunchInspection']   =line[24]
				lesson_info_data_dict['Cleanliness']       =line[25]
				lesson_info_data_dict['drinkingWater']     =line[26]
				lesson_info_data_dict['toiletStatus']      =line[27]
				lesson_info_data_dict['ptmMeeting']        =line[28]
				lesson_info_data_dict['ptmPresence']       =line[29]

				lesson_info_data_db.append(lesson_info_data_dict)
		
			resp = Response(json.dumps({"success": 1,  "profData":lesson_info_data_db}))
		else:
			resp = Response(json.dumps({"success": 0}))
			
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/api/get/admin/data/',methods=['GET','POST'])
def APigetAdminData():
	if request.method=='POST':
	   
		lesson_info_data = dbhelper.GetData().getAdminsurvey()
		lesson_info_data_db = []

		if(len(lesson_info_data))>0:
			for line in lesson_info_data:
				lesson_info_data_dict = {}
				lesson_info_data_dict['id']                =line[0]
				lesson_info_data_dict['username']          =line[1]
				lesson_info_data_dict['registeredStudent'] =line[2]
				lesson_info_data_dict['presentStudent']    =line[3]
				lesson_info_data_dict['absentStudent']     =line[4]
				lesson_info_data_dict['appointedTeacher']  =line[5]
				lesson_info_data_dict['presentTeacher']    =line[6]
				lesson_info_data_dict['absentTeacher']     =line[7]
				lesson_info_data_dict['studentStatus']     =line[8]
				lesson_info_data_dict['punctualityStudent']=line[9]
				lesson_info_data_dict['teacherStatus']     =line[10]
				lesson_info_data_dict['punctualityTeacher']=line[11]
				lesson_info_data_dict['classActivity']     =line[12]
				lesson_info_data_dict['conversation']      =line[13]
				lesson_info_data_dict['relationship']      =line[14]
				lesson_info_data_dict['studyMaterial']     =line[15]
				lesson_info_data_dict['studentExibition']  =line[16]
				lesson_info_data_dict['groupWork']         =line[17]
				lesson_info_data_dict['Questions']         =line[18]
				lesson_info_data_dict['studentSkills']     =line[19]
				lesson_info_data_dict['lastActivity']      =line[20]
				lesson_info_data_dict['Assignment']        =line[21]
				lesson_info_data_dict['assignmentMarks']   =line[22]
				lesson_info_data_dict['lunchStatus']       =line[23]
				lesson_info_data_dict['lunchInspection']   =line[24]
				lesson_info_data_dict['Cleanliness']       =line[25]
				lesson_info_data_dict['drinkingWater']     =line[26]
				lesson_info_data_dict['toiletStatus']      =line[27]
				lesson_info_data_dict['ptmMeeting']        =line[28]
				lesson_info_data_dict['ptmPresence']       =line[29]

				lesson_info_data_db.append(lesson_info_data_dict)
		
			resp = Response(json.dumps({"success": 1,  "profData":lesson_info_data_db}))
		else:
			resp = Response(json.dumps({"success": 0}))
			
		resp.headers['Content-type']='application/json'
		return after_request(resp)

# survey by user


@app.route('/api/get/user/survey/',methods=['GET','POST'])
def APigetUserSurvey():
	if request.method=='POST':
		configure_data= json.loads(request.data)
		mobile = configure_data['mobile']
	   
		lesson_info_data = dbhelper.GetData().getUsersurvey(mobile)
		lesson_info_data_db = []

		if(len(lesson_info_data))>0:
			for line in lesson_info_data:
				lesson_info_data_dict = {}
				lesson_info_data_dict['id']                =line[0]
				lesson_info_data_dict['username']          =line[1]
				lesson_info_data_dict['registeredStudent'] =line[2]
				lesson_info_data_dict['presentStudent']    =line[3]
				lesson_info_data_dict['absentStudent']     =line[4]
				lesson_info_data_dict['appointedTeacher']  =line[5]
				lesson_info_data_dict['presentTeacher']    =line[6]
				lesson_info_data_dict['absentTeacher']     =line[7]
				lesson_info_data_dict['studentStatus']     =line[8]
				lesson_info_data_dict['punctualityStudent']=line[9]
				lesson_info_data_dict['teacherStatus']     =line[10]
				lesson_info_data_dict['punctualityTeacher']=line[11]
				lesson_info_data_dict['classActivity']     =line[12]
				lesson_info_data_dict['conversation']      =line[13]
				lesson_info_data_dict['relationship']      =line[14]
				lesson_info_data_dict['studyMaterial']     =line[15]
				lesson_info_data_dict['studentExibition']  =line[16]
				lesson_info_data_dict['groupWork']         =line[17]
				lesson_info_data_dict['Questions']         =line[18]
				lesson_info_data_dict['studentSkills']     =line[19]
				lesson_info_data_dict['lastActivity']      =line[20]
				lesson_info_data_dict['Assignment']        =line[21]
				lesson_info_data_dict['assignmentMarks']   =line[22]
				lesson_info_data_dict['lunchStatus']       =line[23]
				lesson_info_data_dict['lunchInspection']   =line[24]
				lesson_info_data_dict['Cleanliness']       =line[25]
				lesson_info_data_dict['drinkingWater']     =line[26]
				lesson_info_data_dict['toiletStatus']      =line[27]
				lesson_info_data_dict['ptmMeeting']        =line[28]
				lesson_info_data_dict['ptmPresence']       =line[29]

				lesson_info_data_db.append(lesson_info_data_dict)
		
			resp = Response(json.dumps({"success": 1,  "surveyData":lesson_info_data_db}))
		else:
			resp = Response(json.dumps({"success": 0}))
			
		resp.headers['Content-type']='application/json'
		return after_request(resp)

# end here

@app.route('/api/latest/version/',methods=['GET','POST'])
def APiappByversion():
	if request.method=='POST':
	   
		
		app_data = dbhelper.GetData().getLatestVersion()
		app_data_db=[]
		
		if(len(app_data))>0:
			for line in app_data:
				app_data_dict={}
				app_data_dict['id']                                = line[0]
				app_data_dict['appName']                           = line[1]
				app_data_dict['version']                           = line[2]
				app_data_dict['versionCode']                       = line[3]
				app_data_dict['updateOn']                          = line[4]
				
			   
				
				app_data_db.append(app_data_dict)
				
		resp = Response(json.dumps({"success": True, "app_data": app_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp) 

@app.route('/api/get/school/details/',methods=['GET','POST'])
def APigetschool():
	if request.method=='POST':
		configure_data              = json.loads(request.data)
		username                    = configure_data['username']
		
		lesson_info_data = dbhelper.GetData().getschooldetails(username)
		lesson_info_data_db = []

		if(len(lesson_info_data))>0:
			for line in lesson_info_data:
				lesson_info_data_dict = {}
				lesson_info_data_dict['id']            =line[0]
				lesson_info_data_dict['username']      =line[1]
				lesson_info_data_dict['schoolName']    =line[2]
				lesson_info_data_dict['schoolCode']    =line[3]
				  
								
				lesson_info_data_db.append(lesson_info_data_dict)
		
			resp = Response(json.dumps({"success": 1,  "profData":lesson_info_data_db}))
		else:
			resp = Response(json.dumps({"success": 0}))
			
		resp.headers['Content-type']='application/json'
		return after_request(resp)


# user details

@app.route('/api/user/login/', methods=['GET','POST'])
def ApiUserLogin():
	if request.method  == 'POST':
		user_data =json.loads(request.data)
		mobile = user_data['mobile']
		otp  = user_data['otp']

		User          = dbhelper.GetData().getUserLoginStatus(mobile)
		
		if User:
			
			username = User[0][1]
			mobile = User[0][6]


			text =" Welcome to Bihar SSCA. Your Login OTP is %s."%(str(otp))

			m_phone="91"+str(mobile)
			url ='http://enterprise.smsgatewaycenter.com/SMSApi/rest/send'
			querystring = {"userId":"servtrans","password":"Tgb@12345","senderId":"SERVSM","sendMethod":"simpleMsg","msgType":"text","mobile":m_phone,"msg":text,"duplicateCheck":"true","format":"json"}
			params = urllib.urlencode(querystring)
			response = urllib2.urlopen(url, params)
			json_response = json.loads(response.read())
			print json_response



			 db={'message':'User Exist',"confirmation":1,"username":username,"mobile":mobile}
		else:
			db={'message': 'User Not Exist', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)


# signup

@app.route('/api/add/user/',methods=['GET','POST'])
def APiadduser():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		username           = userInfo['username']
		email      = userInfo['email']
		phone_no = userInfo['mobile']
		state           = userInfo['state']
		district      = userInfo['district']
		block = userInfo['block']
		school = userInfo['school']
		
		
		AddTeacher = dbhelper.AddData().addUser(username,email,phone_no,state,district,block,school)
		if AddTeacher==0:
			db={'message':'User Not Added',"confirmation":0}

			

		else:
			db={'message':'User Added',"confirmation":1,"schoolName":school,"mobile":phone_no}
			text ="Form has been submitted successfully."

			m_phone="91"+str(phone_no)
			url ='http://enterprise.smsgatewaycenter.com/SMSApi/rest/send'
			querystring = {"userId":"servtrans","password":"Tgb@12345","senderId":"SERVSM","sendMethod":"simpleMsg","msgType":"text","mobile":m_phone,"msg":text,"duplicateCheck":"true","format":"json"}
			params = urllib.urlencode(querystring)
			response = urllib2.urlopen(url, params)
			json_response = json.loads(response.read())
			print json_response
			
				
	resp = Response(json.dumps({"response": db}))
	return after_request(resp)

# resend

@app.route('/api/resend/otp/', methods=['GET','POST'])
def AddResendOtp():
	if request.method       == 'POST':
		user_data           =json.loads(request.data)
		print user_data
		mobile              = user_data['mobile']
		otp                = user_data['otp']
		
		
		text =" Welcome to Bihar SSCA. Your Login OTP is %s."%(str(otp))

		m_phone="91"+str(mobile)
		url ='http://enterprise.smsgatewaycenter.com/SMSApi/rest/send'
		querystring = {"userId":"servtrans","password":"Tgb@12345","senderId":"SERVSM","sendMethod":"simpleMsg","msgType":"text","mobile":m_phone,"msg":text,"duplicateCheck":"true","format":"json"}
		params = urllib.urlencode(querystring)
		response = urllib2.urlopen(url, params)
		json_response = json.loads(response.read())
		print json_response


		

		resp = Response(json.dumps({ "response": "success"}))
		return after_request(resp)


@app.route('/api/send/message/', methods=['GET','POST'])
def AddResendMess():
	if request.method       == 'POST':
		user_data           =json.loads(request.data)
		mobile              = user_data['mobile']
		message                = user_data['message']
		
		
		

		url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=idwealth1&pwd=api@idwealth1&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),message)
		print url
		urlfetch.set_default_fetch_deadline(45)
		resp = urlfetch.fetch(url=url,
			method=urlfetch.GET,
			headers={'Content-Type': 'text/html'})
		respp = Response(json.dumps({"response": "success"}))
		return after_request(respp)




@app.route('/api/add/question/',methods=['GET','POST'])
def APiaddquestion():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		lastId   =dbhelper.GetData().getLastIDNew()[0][0]
		if lastId:
			newid=str(123+lastId)
		else:
			newid=str(123)
		registration_code = 'MSOPA' + str(mobile[-4:]) + newid
		question           = userInfo['question']
		option1  = userInfo['option1']
		option2     = userInfo['option2']
		option3      = userInfo['option3']
		option4 = userInfo['option4']
		
		
		AddQuestion = dbhelper.AddData().addQuestionget(question,option1,option2,option3,option4)
		if AddQuestion==0:
			d=0
		else:
			d=1
				
	resp = Response(json.dumps({"success": d}))
	return after_request(resp)

@app.route('/api/add/survey/list/',methods=['GET','POST'])
def APiaddsurveylist():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		description  = userInfo['description']
		survey  = userInfo['survey']
		
		
		AddQuestion = dbhelper.AddData().addsurvey(description,survey)
		if AddQuestion==0:
			d=0
		else:
			d=1
				
	resp = Response(json.dumps({"success": d}))
	return after_request(resp)	

# user details
@app.route('/api/get/user/details/',methods=['POST'])
def APiUserListing():
	if request.method=='POST':
		user_data = dbhelper.GetData().getuserList()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
			   
				user_data_dict['id']   = line[0]
				user_data_dict['username']  = line[1]
				user_data_dict['password'] = line[2]
				user_data_dict['name']= line[3]
				user_data_dict['adminType'] = line[4]
				if line[5]==1:
					user_data_dict['status'] = "Active"

				else:
					user_data_dict['status'] = "Inactive"
				user_data_dict['phone_no'] = line[6]
				user_data_dict['email'] = line[7]
				
				
				user_data_db.append(user_data_dict)

				
		resp = Response(json.dumps({"success": 1, "configure_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

# Activate
@app.route('/api/activate/user/',methods=['GET','POST'])
def APiActivateUser():
	if request.method=='POST':
		userInfo  = json.loads(request.data)    
		Id  = userInfo['Id'] 
		phone_no = userInfo['phone_no']
		
		out  =dbhelper.UpdateData().updateUserStatus(Id)
		text =" You have Activated from Bihar SSCA."
		m_phone="91"+str(phone_no)
		url ='http://enterprise.smsgatewaycenter.com/SMSApi/rest/send'
		querystring = {"userId":"servtrans","password":"Tgb@12345","senderId":"SERVSM","sendMethod":"simpleMsg","msgType":"text","mobile":m_phone,"msg":text,"duplicateCheck":"true","format":"json"}
		params = urllib.urlencode(querystring)
		response = urllib2.urlopen(url, params)
		json_response = json.loads(response.read())
		print json_response
				   
	resp = Response(json.dumps({"success": True}))
	return after_request(resp)


@app.route('/api/deactivate/user/',methods=['GET','POST'])
def APiDeActivateUser():
	if request.method=='POST':
		userInfo  = json.loads(request.data)    
		Id  = userInfo['Id'] 
		phone_no = userInfo['phone_no']
		
		out  =dbhelper.UpdateData().updateDeUserStatus(Id)
		text =" You have Deactivated from Bihar SSCA."
		m_phone="91"+str(phone_no)
		url ='http://enterprise.smsgatewaycenter.com/SMSApi/rest/send'
		querystring = {"userId":"servtrans","password":"Tgb@12345","senderId":"SERVSM","sendMethod":"simpleMsg","msgType":"text","mobile":m_phone,"msg":text,"duplicateCheck":"true","format":"json"}
		params = urllib.urlencode(querystring)
		response = urllib2.urlopen(url, params)
		json_response = json.loads(response.read())
		print json_response
		
				   
	resp = Response(json.dumps({"success": True}))
	return after_request(resp)


# user signup

@app.route('/api/check/user/status/', methods=['GET','POST'])
def AddCheckStatus():
	if request.method       == 'POST':
		user_data           =json.loads(request.data)
		mobile              = user_data['mobile']
		otp                 = user_data['otp']
			
		UserStatus  = dbhelper.GetData().getUserLoginStatus(mobile)

		if(len(UserStatus))>0:
			db={'message':'User Already Exist',"confirmation":1}

		else:
			db={'message': 'User Not Exist', "confirmation":0}

			text =" Welcome to Bihar SSCA. Your Login OTP is %s."%(str(otp))
			m_phone="91"+str(mobile)
			url ='http://enterprise.smsgatewaycenter.com/SMSApi/rest/send'
			querystring = {"userId":"servtrans","password":"Tgb@12345","senderId":"SERVSM","sendMethod":"simpleMsg","msgType":"text","mobile":m_phone,"msg":text,"duplicateCheck":"true","format":"json"}
			params = urllib.urlencode(querystring)
			response = urllib2.urlopen(url, params)
			json_response = json.loads(response.read())
			print json_response

			

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)






# state api

@app.route('/api/get/state/details/',methods=['POST'])
def APiStateData():
	if request.method=='POST':
		state_data = dbhelper.GetData().getStateList()
		state_data_db=[]
		if(len(state_data))>0:
			for line in state_data:
				state_data_dict={}
			   
				state_data_dict['id']   = line[0]
				state_data_dict['stateCode']  = line[1]
				state_data_dict['stateName'] = line[2]
				
				state_data_db.append(state_data_dict)

				
		resp = Response(json.dumps({"success": 1, "configure_data": state_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/api/get/district/data/',methods=['POST'])
def APiDistrictData():
	if request.method=='POST':
		user_data           =json.loads(request.data)
		stateCode              = user_data['stateCode']
		district_data = dbhelper.GetData().getDistrictList(stateCode)
		district_data_db=[]
		if(len(district_data))>0:
			for line in district_data:
				district_data_dict={}
			   
				district_data_dict['districtName']   = line[0]
				district_data_dict['districtcode']   = line[1]
			   
				district_data_db.append(district_data_dict)

				
		resp = Response(json.dumps({"success": 1, "district_data": district_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/block/data/',methods=['POST'])
def APiBlockData():
	if request.method=='POST':
		user_data           =json.loads(request.data)
		districtcode              = user_data['districtcode']
		school_data = dbhelper.GetData().getBlockList(districtcode)
		school_data_db=[]
		if(len(school_data))>0:
			for line in school_data:
				school_data_dict={}
			   
				school_data_dict['block']   = line[0]
				
			   
				school_data_db.append(school_data_dict)

				
		resp = Response(json.dumps({"success": 1, "school_data": school_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/api/get/school/data/',methods=['POST'])
def APiSchoolData():
	if request.method=='POST':
		user_data           =json.loads(request.data)
		block              = user_data['block']
		school_data = dbhelper.GetData().getSchoolList(block)
		school_data_db=[]
		if(len(school_data))>0:
			for line in school_data:
				school_data_dict={}
			   
				school_data_dict['schoolName']   = line[0]
				
			   
				school_data_db.append(school_data_dict)

				
		resp = Response(json.dumps({"success": 1, "school_data": school_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/check/active/status/',methods=['POST'])
def APiCheckUserData():
	if request.method=='POST':
		user_data           =json.loads(request.data)
		mobile              = user_data['mobile']
		
		
		user_data = dbhelper.GetData().getUserStatus(mobile)
		user_status = user_data[0][0]
		survey_status = user_data[0][1]
		

		
				
		resp = Response(json.dumps({"success": 1, "user_status": user_status,"survey_status": survey_status }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


# @app.route('/api/check/survey/status/',methods=['POST'])
# def APiCheckSurvey():
# 	if request.method=='POST':
# 		user_data           =json.loads(request.data)
# 		mobile              = user_data['mobile']
		
# 		try:
# 			survey_status = dbhelper.GetData().getSurveyStatus(mobile)[0][0]
# 		except:
# 			survey_status =''

		
				
# 		resp = Response(json.dumps({"success": 1, "user_status": user_data }))
# 		resp.headers['Content-type']='application/json'
# 		return after_request(resp)


@app.route('/api/user/status/summary/',methods=['POST'])
def APigetSummaryList():
	if request.method=='POST':
		
		user_data = dbhelper.GetData().getUserSummary()
		
		user_data_db=[]
		
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['Inactive']                  = line[0]
				user_data_dict['active']                    = line[1]
				
				
				user_data_db.append(user_data_dict)

				
		resp = Response(json.dumps({"success": 1, "configure_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/api/user/survey/status/',methods=['POST'])
def APigetUserStatusSurvey():
	if request.method=='POST':
		current_time = datetime.now()
		print current_time

		
		user_data = dbhelper.GetData().getUserSurveyStatus()
		
		user_data_db=[]
		
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['Inactive']                  = line[0]
				user_data_dict['active']                    = line[1]
				
				
				user_data_db.append(user_data_dict)

				
		resp = Response(json.dumps({"success": 1, "configure_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


# api
@app.route('/api/user/suvey/details/',methods=['GET','POST'])
def APiUserStatusSurvey():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		username           = userInfo['username']
		district      = userInfo['district']
		block = userInfo['block']
		school = userInfo['school']
		
		
		user_data = dbhelper.GetData().getUserSurveyStatus(username,district,block,school)
		question = dbhelper.GetData().getQuestionStatus()[0][0]
		
		user_data_db=[]
		
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['status']   = line[0]
				user_data_dict['activeQuestion']   = question
				user_data_dict['username']   = username
				user_data_dict['district']   = district
				user_data_dict['block']   = block
				user_data_dict['school']   = school
				
				
				user_data_db.append(user_data_dict)

				
		resp = Response(json.dumps({"success": 1, "configure_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)






