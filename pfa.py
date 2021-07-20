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

import sys

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


# user details

@app.route('/api/user/login/', methods=['GET','POST'])
def ApiUserLogin():
	if request.method  == 'POST':
		user_data =json.loads(request.data)
		mobile = user_data['mobile']
		otp  = user_data['otp']

		User= dbhelper.GetData().getUserLoginStatus(mobile)

		if len(User)>0:

			name = User[0][0]
			email = User[0][1]

			mobile=User[0][2]
			alternateNo=User[0][3]
			try:
				parentName = User[0][4]
			except:
				parentName = ''
			status= User[0][5]
			image_url=User[0][6]
			if User[0][7] is None:

				registrationId=""
			else:
				registrationId=User[0][7]

			if User[0][6] is None:
				image_url=""
			else:
				image_url=image_url



			text =" Welcome+to+IPE+GLOBAL. Your+Login+OTP+is+ %s."%(str(otp))

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			print url
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})



			db={'message':'User Exist',"confirmation":1,"name":name,"mobile":mobile,"status":status,"otp":otp, "email":email,"image_url":image_url,"registrationId":registrationId}
			print db
		else:
			db={'message': 'User Not Exist', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)


@app.route('/api/user/login/new/', methods=['GET','POST'])
def ApiUserLoginNew():
	if request.method  == 'POST':
		user_data =json.loads(request.data)
		mobile = user_data['mobile']
		otp  = user_data['otp']
		print otp
		User= dbhelper.GetData().getUserLoginStatusNew(mobile)
		if len(User)>0:
			name = User[0][0]
			email = User[0][1]
			mobile=User[0][2]
			alternateNo=User[0][3]
			try:
				parentName = User[0][4]
			except:
				parentName =''
			status= User[0][5]
			image_url=User[0][6]
			if User[0][7] is None:
				registrationId=""
			else:
				registrationId=User[0][7]
			if User[0][6] is None:
				image_url=""
			else:
				image_url=image_url
			text =" Welcome+to+IPE+GLOBAL. Your+Login+OTP+is+ %s."%(str(otp))
			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})
			db={'message':'User Exist',"confirmation":1,"name":name,"mobile":mobile,"status":status,"otp":otp, "email":email,"image_url":image_url,"registrationId":registrationId}
		else:
			db={'message': 'User Not Exist', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

# signup

@app.route('/api/add/user/',methods=['GET','POST'])
def APiadduser():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		name= userInfo['name']
		email = userInfo['email']
		mobile = userInfo['mobile']
		alternateNo= userInfo['alternateNo']
		parentName      = userInfo['parentName']
		otp      = userInfo['otp']
		user_status =dbhelper.GetData().getUserStatus(mobile)
		print user_status
		if user_status==True:
			db={'message':'User Already Exist',"confirmation":0}
			resp = Response(json.dumps({"response": db}))
			return after_request(resp)
		else:
			AddUser = dbhelper.AddData().addUser(name,email,mobile,alternateNo,parentName)

			db={'message':'User Added',"confirmation":1,"mobile":mobile,"name":name,"email":email,"otp":otp}

			text ="User+has+been+registered+successfully.Your+Login+OTP+is+ %s."%(str(otp))

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			print url
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})
			respp = Response(json.dumps({"response": db}))
			return after_request(respp)

@app.route('/api/admin/partner/list/',methods=['GET','POST'])
def APiAdminPartnerList():
	if request.method=='POST':
		partner_data  = dbhelper.GetData().getAdminPartnerList()
		partner_data_db=[]
		if(len(partner_data))>0:
			for line in partner_data:
				partner_data_dict={}
				partner_data_dict['mobile']          = line[0]
				partner_data_dict['name']            = line[1]

				partner_data_db.append(partner_data_dict)

		resp = Response(json.dumps({"success": True, "partner_data": partner_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/user/addtoken/', methods=['GET','POST'])
def fcmAuthCustomer():
	if request.method       == 'POST':
		token_data          =json.loads(request.data)
		mobile             =token_data['mobile']
		fcmToken           =token_data['fcmToken']
		update              =dbhelper.DeleteData().deleteToken(mobile)
		last                =dbhelper.AddData().addToken(mobile,fcmToken)
		if last:
			db={'message':'Token Added',"confirmation":1}
		else:
			db={'message': 'Token not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

# Selection app report
@app.route('/api/youth/notice/', methods=['GET','POST'])
def fcmMessageNotice():

	if request.method    == 'POST':
		token_data        =json.loads(request.data)
		# deviceLst         =token_data['deviceLst']
		message           = token_data['message']
		titles           = token_data['titles']
		dateNow           = str(date.today())
		time              = (datetime.now() + timedelta(hours=05,minutes=30)).strftime("%H:%M")

		fcmTokenList         =dbhelper.GetData().getToken2()
		if len(fcmTokenList)>0:
			for gcmT in fcmTokenList:
				mobile = gcmT[1]
				UpDateConfigure = dbhelper.AddData().AddMessage(mobile,message,titles,dateNow,time)
				message_data={   "notification":{"action":"Notification","body":message,"title":titles,"imageUrl":"http://s33.postimg.org/slnc2rtwv/logo.png"},


				"to" : gcmT[0]
				}
				form_data = json.dumps(message_data)


				url='https://fcm.googleapis.com/fcm/send'
				urlfetch.set_default_fetch_deadline(45)

				resp = urlfetch.fetch(url=url,
					method=urlfetch.POST,
					payload=form_data,
					headers={"Authorization":"key=AIzaSyCIXNIX9do1ajdKzNHt9TkhIXu7pG9Vb4k", "Content-Type":"application/json"}
					)

			response = Response(json.dumps({"response":{"confirmation": 1}}))
			return after_request(response)

		else:
			response = Response(json.dumps({"response":{"confirmation": 0}}))
			return after_request(response)


@app.route('/api/app/latest/version/',methods=['GET','POST'])
def APiInnoByversion():
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


@app.route('/api/add/user/new/',methods=['GET','POST'])
def APiadduserNew():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		name= userInfo['name']
		email = userInfo['email']
		mobile = userInfo['mobile']
		alternateNo= userInfo['alternateNo']
		parentName      = userInfo['parentName']
		otp      = userInfo['otp']
		user_status =dbhelper.GetData().getUserStatusNew(mobile)
		print user_status
		if user_status==True:
			db={'message':'User Already Exist',"confirmation":0}
			resp = Response(json.dumps({"response": db}))
			return after_request(resp)
		else:
			AddUser = dbhelper.AddData().addUserNew(name,email,mobile,alternateNo,parentName)

			db={'message':'User Added',"confirmation":1,"mobile":mobile,"name":name,"email":email,"otp":otp}

			text ="User+has+been+registered+successfully.Your+Login+OTP+is+ %s."%(str(otp))

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			print url
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})
			respp = Response(json.dumps({"response": db}))
			return after_request(respp)



@app.route('/api/add/user/updated/',methods=['GET','POST'])
def APiadduserUpdate():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		name= userInfo['name']
		email = userInfo['email']
		mobile = userInfo['mobile']
		alternateNo= userInfo['alternateNo']
		parentName      = userInfo['parentName']
		motherName = userInfo['motherName']
		secondaryMobile= userInfo['secondaryMobile']
		otp      = userInfo['otp']
		user_status =dbhelper.GetData().getUserStatusNew(mobile)
		print user_status
		if user_status==True:
			db={'message':'User Already Exist',"confirmation":0}
			resp = Response(json.dumps({"response": db}))
			return after_request(resp)
		else:
			AddUser = dbhelper.AddData().addUserUpdate(name,email,mobile,alternateNo,parentName,motherName,secondaryMobile)

			db={'message':'User Added',"confirmation":1,"mobile":mobile,"name":name,"email":email,"otp":otp}

			# text ="User+has+been+registered+successfully.Your+Login+OTP+is+ %s."%(str(otp))

			# url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			# print url
			# urlfetch.set_default_fetch_deadline(45)
			# resp = urlfetch.fetch(url=url,
			#   method=urlfetch.GET,
			#   headers={'Content-Type': 'text/html'})
			respp = Response(json.dumps({"response": db}))
			return after_request(respp)







@app.route('/api/user/data/',methods=['GET','POST'])
def APiUserData():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		print userInfo
		mobile  = userInfo['mobile']
		domicile_document= userInfo['domicile_document']
		documentUrl  = userInfo['documentUrl']
		dob= userInfo['dob']
		gender= userInfo['gender']
		maritalStatus  = userInfo['maritalStatus']
		category= userInfo['category']
		disability  = userInfo['disability']
		profile_image= userInfo['profile_image']
		khasi_read  = userInfo['khasi_read']
		khasi_write= userInfo['khasi_write']
		khasi_speak  = userInfo['khasi_speak']
		garo_read= userInfo['garo_read']
		garo_write  = userInfo['garo_write']
		garo_speak= userInfo['garo_speak']
		english_read  = userInfo['english_read']
		english_write= userInfo['english_write']
		english_speak  = userInfo['english_speak']
		hindi_read= userInfo['hindi_read']
		hindi_write  = userInfo['hindi_write']
		hindi_speak= userInfo['hindi_speak']
		other_read  = userInfo['other_read']
		other_write= userInfo['other_write']
		other_speak  = userInfo['other_speak']
		higher_education= userInfo['higher_education']
		passing_year  = userInfo['passing_year']
		training= userInfo['training']
		employed  = userInfo['employed']
		work_experience= userInfo['work_experience']
		employment_prefer  =userInfo['employment_prefer']
		work_outside= userInfo['work_outside']
		expectedSalary= userInfo['expectedSalary']
		short_training  = userInfo['short_training']
		notice_period= userInfo['notice_period']
		address  = userInfo['address']
		houseNo= userInfo['houseNo']
		landmark  = userInfo['landmark']
		city= userInfo['city']
		state  = userInfo['state']
		pincode= userInfo['pincode']
		status  = 1
		trainingType= userInfo['trainingType']
		specialization  = userInfo['specialization']
		trainingDate= userInfo['trainingDate']
		trainingDuration  = userInfo['trainingDuration']
		completionDate= userInfo['completionDate']
		willingState  = userInfo['willingState']
		willingCity= userInfo['willingCity']
		course= userInfo['course']

		health= userInfo['health']
		hospitality  = userInfo['hospitality']
		tourism= userInfo['tourism']
		it  = userInfo['it']
		retail= userInfo['retail']
		manufacturing  = userInfo['manufacturing']
		food= userInfo['food']
		construction= userInfo['construction']
		education= userInfo['education']
		banking= userInfo['banking']
		others= userInfo['others']

		pQualification= userInfo['pQualification']
		pCourse= userInfo['pCourse']
		pPassingYear= userInfo['pPassingYear']

		profile_image= userInfo['profile_image']
		registration_status =dbhelper.GetData().getRegistrationStatus(mobile)
		print registration_status

		if len(registration_status)>0 and  registration_status[0][0] is not None:

			registration_code=registration_status[0][0]
			db= {'message':'Already Registered',"confirmation":2, "registration_code":registration_code}

		else:
			lastId           =dbhelper.GetData().getLastID()[0][0]
			if lastId:
				newid=str(123+lastId)
			else:
				newid=str(123)

			registration_code = 'RXN' + str(mobile[-4:]) + newid
			EditAssign = dbhelper.UpdateData().UpdateUserData(mobile,domicile_document,documentUrl,dob,gender,maritalStatus,category,disability,profile_image,khasi_read,khasi_write,khasi_speak,garo_read,garo_write,garo_speak,english_read,english_write,english_speak,hindi_read,hindi_write,hindi_speak,other_read,other_write,other_speak,higher_education,passing_year,training,employed,work_experience,employment_prefer,work_outside,expectedSalary,short_training,notice_period,address,houseNo,landmark,city,state,pincode,status,trainingType,specialization,trainingDate,trainingDuration,completionDate,willingState,willingCity,course,health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others,pQualification,pCourse,pPassingYear,profile_image,registration_code)
			db={'message':'UserDataUpdate',"confirmation":1, "registration_code": registration_code}
			text="Congratulations+!+Your+Form+has+been+Submitted+Succesfully.Your+Registration+No+is '%s'"%(registration_code)

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			print url
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})




		resp = Response(json.dumps({"response": db}))
		return after_request(resp)



@app.route('/api/user/data/new/',methods=['GET','POST'])
def APiUserDataNew():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		print userInfo
		mobile  = userInfo['mobile']
		domicile_document= userInfo['domicile_document']
		documentUrl  = ""
		dob= userInfo['dob']
		gender= userInfo['gender']
		# maritalStatus  = userInfo['maritalStatus']
		category= userInfo['category']
		govtIdType= userInfo['govtIdType']
		govtIdOthers= userInfo['govtIdOthers']
		govtIdNumber= userInfo['govtIdNumber']
		govtIdImage= userInfo['govtIdImage']

		higher_education= userInfo['higher_education']
		course= userInfo['course']

		passing_year  = userInfo['passing_year']
		pQualification= userInfo['pQualification']
		pCourse= userInfo['pCourse']
		pPassingYear= userInfo['pPassingYear']
		work_outside= userInfo['work_outside']
		skillsName=userInfo['skillsName']

		health= userInfo['health']
		hospitality  = userInfo['hospitality']
		tourism= userInfo['tourism']
		it  = userInfo['it']
		retail= userInfo['retail']
		manufacturing  = userInfo['manufacturing']
		food= userInfo['food']
		construction= userInfo['construction']
		education= userInfo['education']
		banking= userInfo['banking']
		others= userInfo['others']
		address  = userInfo['address']
		houseNo= userInfo['houseNo']
		villageName  = userInfo['villageName']
		city= userInfo['city']
		state  = userInfo['state']
		pincode= userInfo['pincode']



		status  = 1
		registration_status =dbhelper.GetData().getRegistrationStatusNew(mobile)
		print registration_status

		if len(registration_status)>0 and  registration_status[0][0] is not None:

			registration_code=registration_status[0][0]
			db= {'message':'Already Registered',"confirmation":2, "registration_code":registration_code}

		else:
			lastId           =dbhelper.GetData().getLastIDNew()[0][0]
			if lastId:
				newid=str(123+lastId)
			else:
				newid=str(123)


			registration_code = 'MSOPA' + str(mobile[-4:]) + newid



			EditAssign = dbhelper.UpdateData().UpdateUserBasicData(mobile,domicile_document,documentUrl,dob,gender,category,govtIdType, govtIdNumber, govtIdImage, higher_education,course, passing_year,pQualification,pCourse,pPassingYear, work_outside,skillsName, health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others, address,houseNo,villageName,city,state,pincode,registration_code)
			db={'message':'UserDataUpdate',"confirmation":1, "registration_code": registration_code}
			text="Congratulations+!+Your+Form+has+been+Submitted+Succesfully.Your+Registration+No+is '%s'"%(registration_code)

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})




		resp = Response(json.dumps({"response": db}))
		return after_request(resp)




@app.route('/api/youth/employee/absent/',methods=['POST'])
def APigetMtrackAbsentList():
	if request.method=='POST':
		configure_data              = json.loads(request.data)

		strDate                     = str(date.today())
		dateNow                     = datetime.strptime(strDate, "%Y-%m-%d").strftime("%m/%d/%Y")



		emp_data = dbhelper.GetData().getAllAbsentEmployeeList(dateNow)
		total= len(emp_data)
		emp_data_db=[]

		if(len(emp_data))>0:
			for line in emp_data:
				emp_data_dict={}
				emp_data_dict['name']                = line[0]
				emp_data_dict['company']              = line[1]
				emp_data_dict['job_role']               = line[2]
				emp_data_dict['mobile']              = line[3]
				emp_data_db.append(emp_data_dict)


		resp = Response(json.dumps({"success": True, "user_data": emp_data_db,"total":total }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)




@app.route('/api/add/user/list/',methods=['GET','POST'])
def APiAdduserList():
	if request.method=='POST':
		tripInfo   = json.loads(request.data)
		dataLst          = tripInfo['data']
		for userInfo in dataLst:
			print userInfo
			name= userInfo['name']
			email = userInfo['email']
			mobile = userInfo['mobile']
			alternateNo= userInfo['alternateNo']
			parentName      = userInfo['parentName']
			domicile_document= userInfo['domicile_document']
			documentUrl  = ""
			dob= userInfo['dob']
			gender= userInfo['gender']
			category= userInfo['category']
			govtIdType= userInfo['govtIdType']
			govtIdOthers= userInfo['govtIdOthers']
			govtIdNumber= userInfo['govtIdNumber']
			govtIdImage= userInfo['govtIdImage']
			higher_education= userInfo['higher_education']
			course= userInfo['course']
			passing_year  = userInfo['passing_year']
			pQualification= userInfo['pQualification']
			pCourse= userInfo['pCourse']
			pPassingYear= userInfo['pPassingYear']
			work_outside= userInfo['work_outside']
			skillsName=userInfo['skillsName']
			health= userInfo['health']
			hospitality  = userInfo['hospitality']
			tourism= userInfo['tourism']
			it  = userInfo['it']
			retail= userInfo['retail']
			manufacturing  = userInfo['manufacturing']
			food= userInfo['food']
			construction= userInfo['construction']
			education= userInfo['education']
			banking= userInfo['banking']
			others= userInfo['others']
			address  = userInfo['address']
			houseNo= userInfo['houseNo']
			villageName  = userInfo['villageName']
			city= userInfo['city']
			state  = userInfo['state']
			pincode= userInfo['pincode']
			pAddress1  = userInfo['pAddress1']
			pAddress2  = userInfo['pAddress2']
			pVillage= userInfo['pVillage']
			pState  = userInfo['pState']
			pCity= userInfo['pCity']
			pPincode  = userInfo['pPincode']
			user_type = userInfo['user_type']
			maritalStatus  = userInfo['maritalStatus']
			disability  = userInfo['disability']
			profile_image= userInfo['profile_image']
			khasi_read  = userInfo['khasi_read']
			khasi_write= userInfo['khasi_write']
			khasi_speak  = userInfo['khasi_speak']
			garo_read= userInfo['garo_read']
			garo_write  = userInfo['garo_write']
			garo_speak= userInfo['garo_speak']
			english_read  = userInfo['english_read']
			english_write= userInfo['english_write']
			english_speak  = userInfo['english_speak']
			hindi_read= userInfo['hindi_read']
			hindi_write  = userInfo['hindi_write']
			hindi_speak= userInfo['hindi_speak']
			other_read  = userInfo['other_read']
			other_write= userInfo['other_write']
			other_speak  = userInfo['other_speak']
			training= userInfo['training']
			trainingType= userInfo['trainingType']
			specialization  = userInfo['specialization']
			trainingDuration  = userInfo['trainingDuration']
			completionDate= userInfo['completionDate']
			employed  = userInfo['employed']
			work_experience= userInfo['work_experience']
			employment_prefer  =userInfo['employment_prefer']
			short_training  = userInfo['short_training']
			notice_period= userInfo['notice_period']
			companyName= userInfo['companyName']
			workPlace  =userInfo['workPlace']
			salary  = userInfo['salary']
			employed_since= userInfo['employed_since']



			status  = 1
			registration_status =dbhelper.GetData().getRegistrationStatusNew(mobile)
			print registration_status

			if len(registration_status)>0 and  registration_status[0][0] is not None:

				registration_code=registration_status[0][0]
				db= {'message':'Already Registered',"confirmation":2, "registration_code":registration_code}

			else:
				lastId           =dbhelper.GetData().getLastIDNew()[0][0]
				if lastId:
					newid=str(123+lastId)
				else:
					newid=str(123)
				registration_code = 'MSOPA' + str(mobile[-4:]) + newid
				EditAssign = dbhelper.AddData().AdduserList(name,email,mobile,alternateNo,parentName,domicile_document,documentUrl,dob,gender,category,govtIdType, govtIdNumber, govtIdImage, higher_education,course, passing_year,pQualification,pCourse,pPassingYear, work_outside,skillsName, health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others, address,houseNo,villageName,city,state,pincode,pAddress1,pAddress2,pVillage,pCity,pState,pPincode,user_type,registration_code,maritalStatus,disability,profile_image,khasi_read,khasi_write,khasi_speak,garo_read,garo_write,garo_speak,english_read,english_write,english_speak,hindi_read,hindi_write,hindi_speak,other_read,other_write,other_speak,training,trainingType,specialization,trainingDuration,completionDate, employed,work_experience,employment_prefer,short_training,notice_period,companyName,workPlace,salary,employed_since)
				db={'message':'UserDataUpdate',"confirmation":1, "registration_code": registration_code}
				text="Congratulations+!+Your+Form+has+been+Submitted+Succesfully.Your+Registration+No+is '%s'"%(registration_code)

				url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
				print url
				urlfetch.set_default_fetch_deadline(45)
				resp = urlfetch.fetch(url=url,
					method=urlfetch.GET,
					headers={'Content-Type': 'text/html'})
			resp = Response(json.dumps({"response": db}))
			return after_request(resp)



@app.route('/api/user/list/secondary/',methods=['GET','POST'])
def APiUserListSecondary():
	if request.method=='POST':
		tripInfo   = json.loads(request.data)
		dataLst          = tripInfo['data']
		for userInfo in dataLst:


			mobile  = userInfo['mobile']
			maritalStatus  = userInfo['maritalStatus']
			disability  = userInfo['disability']
			profile_image= userInfo['profile_image']
			khasi_read  = userInfo['khasi_read']
			khasi_write= userInfo['khasi_write']
			khasi_speak  = userInfo['khasi_speak']
			garo_read= userInfo['garo_read']
			garo_write  = userInfo['garo_write']
			garo_speak= userInfo['garo_speak']
			english_read  = userInfo['english_read']
			english_write= userInfo['english_write']
			english_speak  = userInfo['english_speak']
			hindi_read= userInfo['hindi_read']
			hindi_write  = userInfo['hindi_write']
			hindi_speak= userInfo['hindi_speak']
			other_read  = userInfo['other_read']
			other_write= userInfo['other_write']
			other_speak  = userInfo['other_speak']
			training= userInfo['training']
			trainingType= userInfo['trainingType']
			specialization  = userInfo['specialization']
			trainingDuration  = userInfo['trainingDuration']
			completionDate= userInfo['completionDate']

			employed  = userInfo['employed']
			work_experience= userInfo['work_experience']
			employment_prefer  =userInfo['employment_prefer']
			short_training  = userInfo['short_training']
			notice_period= userInfo['notice_period']

			companyName= userInfo['companyName']
			workPlace  =userInfo['workPlace']
			salary  = userInfo['salary']
			employed_since= userInfo['employed_since']

			EditAssign = dbhelper.UpdateData().UpdateUserListSecondary(mobile,maritalStatus,disability,profile_image,khasi_read,khasi_write,khasi_speak,garo_read,garo_write,garo_speak,english_read,english_write,english_speak,hindi_read,hindi_write,hindi_speak,other_read,other_write,other_speak,training,trainingType,specialization,trainingDuration,completionDate, employed,work_experience,employment_prefer,short_training,notice_period,companyName,workPlace,salary,employed_since)
			db={'message':'UserDataUpdate',"confirmation":1}


			resp = Response(json.dumps({"response": db}))
			return after_request(resp)








# second

@app.route('/api/add/user/data/new/',methods=['GET','POST'])
def APiAddUserDataNew2():
	if request.method=='POST':
		userInfo   = json.loads(request.data)

		mobile  = userInfo['mobile']
		domicile_document= userInfo['domicile_document']
		documentUrl  = ""
		dob= userInfo['dob']
		gender= userInfo['gender']
		# maritalStatus  = userInfo['maritalStatus']
		category= userInfo['category']
		govtIdType= userInfo['govtIdType']
		govtIdOthers= userInfo['govtIdOthers']
		govtIdNumber= userInfo['govtIdNumber']
		govtIdImage= userInfo['govtIdImage']

		higher_education= userInfo['higher_education']
		course= userInfo['course']

		passing_year  = userInfo['passing_year']
		pQualification= userInfo['pQualification']
		pCourse= userInfo['pCourse']
		pPassingYear= userInfo['pPassingYear']
		work_outside= userInfo['work_outside']
		skillsName=userInfo['skillsName']

		health= userInfo['health']
		hospitality  = userInfo['hospitality']
		tourism= userInfo['tourism']
		it  = userInfo['it']
		retail= userInfo['retail']
		manufacturing  = userInfo['manufacturing']
		food= userInfo['food']
		construction= userInfo['construction']
		education= userInfo['education']
		banking= userInfo['banking']
		others= userInfo['others']
		address  = userInfo['address']
		houseNo= userInfo['houseNo']
		villageName  = userInfo['villageName']
		city= userInfo['city']
		state  = userInfo['state']
		pincode= userInfo['pincode']

		pAddress1  = userInfo['pAddress1']
		pAddress2  = userInfo['pAddress2']
		pVillage= userInfo['pVillage']
		pState  = userInfo['pState']
		pCity= userInfo['pCity']
		pPincode  = userInfo['pPincode']
		user_type = userInfo['user_type']
		# userCity  = ''
		# userState  = userInfo['cState']
		# latitude= userInfo['lat']
		# longitude  = userInfo['lng']

		status  = 1
		registration_status =dbhelper.GetData().getRegistrationStatusNew(mobile)


		if len(registration_status)>0 and  registration_status[0][0] is not None:

			registration_code=registration_status[0][0]
			db= {'message':'Already Registered',"confirmation":2, "registration_code":registration_code}

		else:
			lastId           =dbhelper.GetData().getLastIDNew()[0][0]
			if lastId:
				newid=str(123+lastId)
			else:
				newid=str(123)


			registration_code = 'MSOPA' + str(mobile[-4:]) + newid



			EditAssign = dbhelper.UpdateData().UpdateUserAddData2(mobile,domicile_document,documentUrl,dob,gender,category,govtIdType, govtIdNumber, govtIdImage, higher_education,course, passing_year,pQualification,pCourse,pPassingYear, work_outside,skillsName, health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others, address,houseNo,villageName,city,state,pincode,pAddress1,pAddress2,pVillage,pState,pCity,pPincode,registration_code,user_type)
			db={'message':'UserDataUpdate',"confirmation":1, "registration_code": registration_code}
			text="Congratulations+!+Your+Form+has+been+Submitted+Succesfully.Your+Registration+No+is '%s'"%(registration_code)

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			print url
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})




		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/api/add/user/data/updated/',methods=['GET','POST'])
def APiAddUserDataUpdate():
	if request.method=='POST':
		userInfo   = json.loads(request.data)

		mobile  = userInfo['mobile']
		domicile_document= userInfo['domicile_document']
		documentUrl  = ""
		dob= userInfo['dob']
		gender= userInfo['gender']
		# maritalStatus  = userInfo['maritalStatus']
		category= userInfo['category']
		govtIdType= userInfo['govtIdType']
		govtIdOthers= userInfo['govtIdOthers']
		govtIdNumber= userInfo['govtIdNumber']
		govtIdImage= userInfo['govtIdImage']

		higher_education= userInfo['higher_education']
		course= userInfo['course']

		passing_year  = userInfo['passing_year']
		pQualification= userInfo['pQualification']
		pCourse= userInfo['pCourse']
		pPassingYear= userInfo['pPassingYear']
		work_outside= userInfo['work_outside']
		skillsName=userInfo['skillsName']

		health= userInfo['health']
		hospitality  = userInfo['hospitality']
		tourism= userInfo['tourism']
		it  = userInfo['it']
		retail= userInfo['retail']
		manufacturing  = userInfo['manufacturing']
		food= userInfo['food']
		construction= userInfo['construction']
		education= userInfo['education']
		banking= userInfo['banking']
		others= userInfo['others']
		address  = userInfo['address'].replace("'s","s")
		houseNo= userInfo['houseNo']
		villageName  = userInfo['villageName']
		city= userInfo['city']
		state  = userInfo['state']
		pincode= userInfo['pincode']

		pAddress1  = userInfo['pAddress1'].replace("'s","s")
		pAddress2  = userInfo['pAddress2'].replace("'s","s")
		pVillage= userInfo['pVillage']
		pState  = userInfo['pState']
		pCity= userInfo['pCity']
		pPincode  = userInfo['pPincode']
		user_type = userInfo['user_type']
		userCity  = userInfo['usercity']
		userState  = userInfo['cState']
		latitude= userInfo['lat']
		longitude  = userInfo['lng']
		# dob_calclute=userInfo['dob_calclute']

		status  = 1
		registration_status =dbhelper.GetData().getRegistrationStatusNew(mobile)


		if len(registration_status)>0 and  registration_status[0][0] is not None:

			registration_code=registration_status[0][0]
			db= {'message':'Already Registered',"confirmation":2, "registration_code":registration_code}

		else:
			lastId           =dbhelper.GetData().getLastIDNew()[0][0]
			if lastId:
				newid=str(123+lastId)
			else:
				newid=str(123)


			registration_code = 'MSOPA' + str(mobile[-4:]) + newid
			EditAssign = dbhelper.UpdateData().UpdateUserAddData3(mobile,domicile_document,documentUrl,dob,gender,category,govtIdType, govtIdNumber, govtIdImage, higher_education,course, passing_year,pQualification,pCourse,pPassingYear, work_outside,skillsName, health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others, address,houseNo,villageName,city,state,pincode,pAddress1,pAddress2,pVillage,pState,pCity,pPincode,registration_code,user_type,userCity,userState,latitude,longitude)
			db={'message':'UserDataUpdate',"confirmation":1, "registration_code": registration_code}
			text="Congratulations+!+Your+Form+has+been+Submitted+Succesfully.Your+Registration+No+is '%s'"%(registration_code)

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			print url
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})




		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/api/add/user/data/new/updated/',methods=['GET','POST'])
def APiAddUserDataNewUpdate():
	if request.method=='POST':
		userInfo   = json.loads(request.data)

		mobile  = userInfo['mobile']
		domicile_document= userInfo['domicile_document']
		documentUrl  = ""
		dob= userInfo['dob']
		gender= userInfo['gender']
		# maritalStatus  = userInfo['maritalStatus']
		category= userInfo['category']
		govtIdType= userInfo['govtIdType']
		govtIdOthers= userInfo['govtIdOthers']
		govtIdNumber= userInfo['govtIdNumber']
		govtIdImage= userInfo['govtIdImage']

		higher_education= userInfo['higher_education']
		course= userInfo['course']

		passing_year  = userInfo['passing_year']
		pQualification= userInfo['pQualification']
		pCourse= userInfo['pCourse']
		pPassingYear= userInfo['pPassingYear']
		work_outside= userInfo['work_outside']
		skillsName=userInfo['skillsName']

		health= userInfo['health']
		hospitality  = userInfo['hospitality']
		tourism= userInfo['tourism']
		it  = userInfo['it']
		retail= userInfo['retail']
		manufacturing  = userInfo['manufacturing']
		food= userInfo['food']
		construction= userInfo['construction']
		education= userInfo['education']
		banking= userInfo['banking']
		others= userInfo['others']
		address  = userInfo['address'].replace("'s","s")
		houseNo= userInfo['houseNo']
		villageName  = userInfo['villageName']
		city= userInfo['city']
		state  = userInfo['state']
		pincode= userInfo['pincode']

		pAddress1  = userInfo['pAddress1'].replace("'s","s")
		pAddress2  = userInfo['pAddress2'].replace("'s","s")
		pVillage= userInfo['pVillage']
		pState  = userInfo['pState']
		pCity= userInfo['pCity']
		pPincode  = userInfo['pPincode']
		user_type = userInfo['user_type']
		userCity  = userInfo['usercity']
		userState  = userInfo['cState']
		latitude= userInfo['lat']
		longitude  = userInfo['lng']
		dob_calclute=userInfo['dob_calclute']

		status  = 1
		registration_status =dbhelper.GetData().getRegistrationStatusNew(mobile)


		if len(registration_status)>0 and  registration_status[0][0] is not None:

			registration_code=registration_status[0][0]
			db= {'message':'Already Registered',"confirmation":2, "registration_code":registration_code}

		else:
			lastId           =dbhelper.GetData().getLastIDNew()[0][0]
			if lastId:
				newid=str(123+lastId)
			else:
				newid=str(123)


			registration_code = 'MSOPA' + str(mobile[-4:]) + newid
			EditAssign = dbhelper.UpdateData().UpdateUserAddData4(mobile,domicile_document,documentUrl,dob,gender,category,govtIdType, govtIdNumber, govtIdImage, higher_education,course, passing_year,pQualification,pCourse,pPassingYear, work_outside,skillsName, health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others, address,houseNo,villageName,city,state,pincode,pAddress1,pAddress2,pVillage,pState,pCity,pPincode,registration_code,user_type,userCity,userState,latitude,longitude,dob_calclute)
			db={'message':'UserDataUpdate',"confirmation":1, "registration_code": registration_code}
			text="Congratulations+!+Your+Form+has+been+Submitted+Succesfully.Your+Registration+No+is '%s'"%(registration_code)

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			print url
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})




		resp = Response(json.dumps({"response": db}))
		return after_request(resp)



@app.route('/api/add/user/list/updated/',methods=['GET','POST'])
def APiAdduserUpdateList():
	if request.method=='POST':
		tripInfo   = json.loads(request.data)
		dataLst          = tripInfo['data']
		print dataLst
		for userInfo in dataLst:
			print userInfo
			mobile  = userInfo['mobile']
			email = userInfo['email']
			parentName = userInfo['parentName']
			name = userInfo['name']
			alternateNo = userInfo['alternateNo']
			motherName = userInfo['motherName']
			secondaryMobile = userInfo['secondaryMobile']
			domicile_document= userInfo['domicile_document']
			documentUrl  = ""
			dob= userInfo['dob']
			gender= userInfo['gender']
			# maritalStatus  = userInfo['maritalStatus']
			category= userInfo['category']
			govtIdType= userInfo['govtIdType']
			govtIdOthers= userInfo['govtIdOthers']
			govtIdNumber= userInfo['govtIdNumber']
			govtIdImage= userInfo['govtIdImage']

			higher_education= userInfo['higher_education']
			course= userInfo['course']

			passing_year  = userInfo['passing_year']
			pQualification= userInfo['pQualification']
			pCourse= userInfo['pCourse']
			pPassingYear= userInfo['pPassingYear']
			work_outside= userInfo['work_outside']
			skillsName=userInfo['skillsName']

			health= userInfo['health']
			hospitality  = userInfo['hospitality']
			tourism= userInfo['tourism']
			it  = userInfo['it']
			retail= userInfo['retail']
			manufacturing  = userInfo['manufacturing']
			food= userInfo['food']
			construction= userInfo['construction']
			education= userInfo['education']
			banking= userInfo['banking']
			others= userInfo['others']
			address  = userInfo['address'].replace("'s","s")
			houseNo= userInfo['houseNo']
			villageName  = userInfo['villageName']
			city= userInfo['city']
			state  = userInfo['state']
			pincode= userInfo['pincode']

			pAddress1  = userInfo['pAddress1'].replace("'s","s")
			pAddress2  = userInfo['pAddress2'].replace("'s","s")
			pVillage= userInfo['pVillage']
			pState  = userInfo['pState']
			pCity= userInfo['pCity']
			pPincode  = userInfo['pPincode']
			user_type = userInfo['user_type']
			userCity  = userInfo['usercity']
			userState  = userInfo['cState']
			latitude= userInfo['lat']
			longitude  = userInfo['lng']
			mobile  = userInfo['mobile']

			maritalStatus  = userInfo['maritalStatus']

			disability  = userInfo['disability']
			profile_image= userInfo['profile_image']

			khasi_read  = userInfo['khasi_read']
			khasi_write= userInfo['khasi_write']
			khasi_speak  = userInfo['khasi_speak']
			garo_read= userInfo['garo_read']
			garo_write  = userInfo['garo_write']
			garo_speak= userInfo['garo_speak']
			english_read  = userInfo['english_read']
			english_write= userInfo['english_write']
			english_speak  = userInfo['english_speak']
			hindi_read= userInfo['hindi_read']
			hindi_write  = userInfo['hindi_write']
			hindi_speak= userInfo['hindi_speak']
			other_read  = userInfo['other_read']
			other_write= userInfo['other_write']
			other_speak  = userInfo['other_speak']
			training= userInfo['training']
			trainingType= userInfo['trainingType']
			specialization  = userInfo['specialization']
			trainingDuration  = userInfo['trainingDuration']
			completionDate= userInfo['completionDate']

			employed  = userInfo['employed']
			work_experience= userInfo['work_experience']
			employment_prefer  =userInfo['employment_prefer']
			short_training  = userInfo['short_training']
			notice_period= userInfo['notice_period']

			totalMember  =userInfo['totalMember']
			familyIncome  = userInfo['familyIncome']
			dob_calclute  = userInfo['dob_calclute']

			status  = 1
			user_status =dbhelper.GetData().getUserStatus(mobile)
			print user_status
			if user_status==True:
				pass
			else:

				registration_status =dbhelper.GetData().getRegistrationStatusNew(mobile)


				if len(registration_status)>0 and  registration_status[0][0] is not None:

					registration_code=registration_status[0][0]
					db= {'message':'Already Registered',"confirmation":2, "registration_code":registration_code}

				else:
					lastId           =dbhelper.GetData().getLastIDNew()[0][0]
					if lastId:
						newid=str(123+lastId)
					else:
						newid=str(123)


					registration_code = 'MSOPA' + str(mobile[-4:]) + newid
					EditAssign = dbhelper.AddData().addOfflineData(mobile,motherName,secondaryMobile,email,name,alternateNo,parentName,domicile_document,documentUrl,dob,gender,category,govtIdType, govtIdNumber, govtIdImage, higher_education,course, passing_year,pQualification,pCourse,pPassingYear, work_outside,skillsName, health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others, address,houseNo,villageName,city,state,pincode,pAddress1,pAddress2,pVillage,pState,pCity,pPincode,registration_code,user_type,userCity,userState,latitude,longitude,maritalStatus,disability,profile_image,khasi_read,khasi_write,khasi_speak,garo_read,garo_write,garo_speak,english_read,english_write,english_speak,hindi_read,hindi_write,hindi_speak,other_read,other_write,other_speak,training,trainingType,specialization,trainingDuration,completionDate, employed,work_experience,employment_prefer,short_training,notice_period,totalMember,familyIncome,dob_calclute)
					db={'message':'UserDataUpdate',"confirmation":1, "registration_code": registration_code}
					text="Congratulations+!+Your+Form+has+been+Submitted+Succesfully.Your+Registration+No+is '%s'"%(registration_code)

					url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
					print url
					urlfetch.set_default_fetch_deadline(45)
					resp = urlfetch.fetch(url=url,
						method=urlfetch.GET,
						headers={'Content-Type': 'text/html'})

			resp = Response(json.dumps({"response": db,"confirmation":1}))
			return after_request(resp)



@app.route('/api/add/user/data/',methods=['GET','POST'])
def APiAddUserDataNew():
	if request.method=='POST':
		userInfo   = json.loads(request.data)

		mobile  = userInfo['mobile']
		domicile_document= userInfo['domicile_document']
		documentUrl  = ""
		dob= userInfo['dob']
		gender= userInfo['gender']
		# maritalStatus  = userInfo['maritalStatus']
		category= userInfo['category']
		govtIdType= userInfo['govtIdType']
		govtIdOthers= userInfo['govtIdOthers']
		govtIdNumber= userInfo['govtIdNumber']
		govtIdImage= userInfo['govtIdImage']

		higher_education= userInfo['higher_education']
		course= userInfo['course']

		passing_year  = userInfo['passing_year']
		pQualification= userInfo['pQualification']
		pCourse= userInfo['pCourse']
		pPassingYear= userInfo['pPassingYear']
		work_outside= userInfo['work_outside']
		skillsName=userInfo['skillsName']

		health= userInfo['health']
		hospitality  = userInfo['hospitality']
		tourism= userInfo['tourism']
		it  = userInfo['it']
		retail= userInfo['retail']
		manufacturing  = userInfo['manufacturing']
		food= userInfo['food']
		construction= userInfo['construction']
		education= userInfo['education']
		banking= userInfo['banking']
		others= userInfo['others']
		address  = userInfo['address']
		houseNo= userInfo['houseNo']
		villageName  = userInfo['villageName']
		city= userInfo['city']
		state  = userInfo['state']
		pincode= userInfo['pincode']

		pAddress1  = userInfo['pAddress1']
		pAddress2  = userInfo['pAddress2']
		pVillage= userInfo['pVillage']
		pState  = userInfo['pState']
		pCity= userInfo['pCity']
		pPincode  = userInfo['pPincode']
		user_type = userInfo['user_type']


		status  = 1
		registration_status =dbhelper.GetData().getRegistrationStatusNew(mobile)
		print registration_status

		if len(registration_status)>0 and  registration_status[0][0] is not None:

			registration_code=registration_status[0][0]
			db= {'message':'Already Registered',"confirmation":2, "registration_code":registration_code}

		else:
			lastId           =dbhelper.GetData().getLastIDNew()[0][0]
			if lastId:
				newid=str(123+lastId)
			else:
				newid=str(123)


			registration_code = 'MSOPA' + str(mobile[-4:]) + newid



			EditAssign = dbhelper.UpdateData().UpdateUserAddData2(mobile,domicile_document,documentUrl,dob,gender,category,govtIdType, govtIdNumber, govtIdImage, higher_education,course, passing_year,pQualification,pCourse,pPassingYear, work_outside,skillsName, health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others, address,houseNo,villageName,city,state,pincode,pAddress1,pAddress2,pVillage,pState,pCity,pPincode,registration_code,user_type)
			db={'message':'UserDataUpdate',"confirmation":1, "registration_code": registration_code}
			text="Congratulations+!+Your+Form+has+been+Submitted+Succesfully.Your+Registration+No+is '%s'"%(registration_code)

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)

			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})




		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/api/user/data/secondary/',methods=['GET','POST'])
def APiUserDataSecondary():
	if request.method=='POST':
		userInfo   = json.loads(request.data)

		mobile  = userInfo['mobile']

		maritalStatus  = userInfo['maritalStatus']

		disability  = userInfo['disability']
		profile_image= userInfo['profile_image']

		khasi_read  = userInfo['khasi_read']
		khasi_write= userInfo['khasi_write']
		khasi_speak  = userInfo['khasi_speak']
		garo_read= userInfo['garo_read']
		garo_write  = userInfo['garo_write']
		garo_speak= userInfo['garo_speak']
		english_read  = userInfo['english_read']
		english_write= userInfo['english_write']
		english_speak  = userInfo['english_speak']
		hindi_read= userInfo['hindi_read']
		hindi_write  = userInfo['hindi_write']
		hindi_speak= userInfo['hindi_speak']
		other_read  = userInfo['other_read']
		other_write= userInfo['other_write']
		other_speak  = userInfo['other_speak']
		training= userInfo['training']
		trainingType= userInfo['trainingType']
		specialization  = userInfo['specialization']
		trainingDuration  = userInfo['trainingDuration']
		completionDate= userInfo['completionDate']

		employed  = userInfo['employed']
		work_experience= userInfo['work_experience']
		employment_prefer  =userInfo['employment_prefer']
		short_training  = userInfo['short_training']
		notice_period= userInfo['notice_period']

		EditAssign = dbhelper.UpdateData().UpdateUserDataSecondary(mobile,maritalStatus,disability,profile_image,khasi_read,khasi_write,khasi_speak,garo_read,garo_write,garo_speak,english_read,english_write,english_speak,hindi_read,hindi_write,hindi_speak,other_read,other_write,other_speak,training,trainingType,specialization,trainingDuration,completionDate, employed,work_experience,employment_prefer,short_training,notice_period)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/api/user/data/secondary/updated/',methods=['GET','POST'])
def APiUserUpdateSecondary():
	if request.method=='POST':
		userInfo   = json.loads(request.data)

		mobile  = userInfo['mobile']

		maritalStatus  = userInfo['maritalStatus']

		disability  = userInfo['disability']
		profile_image= userInfo['profile_image']

		khasi_read  = userInfo['khasi_read']
		khasi_write= userInfo['khasi_write']
		khasi_speak  = userInfo['khasi_speak']
		garo_read= userInfo['garo_read']
		garo_write  = userInfo['garo_write']
		garo_speak= userInfo['garo_speak']
		english_read  = userInfo['english_read']
		english_write= userInfo['english_write']
		english_speak  = userInfo['english_speak']
		hindi_read= userInfo['hindi_read']
		hindi_write  = userInfo['hindi_write']
		hindi_speak= userInfo['hindi_speak']
		other_read  = userInfo['other_read']
		other_write= userInfo['other_write']
		other_speak  = userInfo['other_speak']
		training= userInfo['training']
		trainingType= userInfo['trainingType']
		specialization  = userInfo['specialization']
		trainingDuration  = userInfo['trainingDuration']
		completionDate= userInfo['completionDate']

		employed  = userInfo['employed']
		work_experience= userInfo['work_experience']
		employment_prefer  =userInfo['employment_prefer']
		short_training  = userInfo['short_training']
		notice_period= userInfo['notice_period']

		totalMember  =userInfo['totalMember']
		familyIncome  = userInfo['familyIncome']


		EditAssign = dbhelper.UpdateData().UpdateSecondary(mobile,maritalStatus,disability,profile_image,khasi_read,khasi_write,khasi_speak,garo_read,garo_write,garo_speak,english_read,english_write,english_speak,hindi_read,hindi_write,hindi_speak,other_read,other_write,other_speak,training,trainingType,specialization,trainingDuration,completionDate, employed,work_experience,employment_prefer,short_training,notice_period,totalMember,familyIncome)
		db={'message':'UserDataUpdate',"confirmation":1}





		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


# resend

@app.route('/api/get/image/list/',methods=['GET'])
def APigetBackgroundImage():
	if request.method=='GET':

		emp_data = dbhelper.GetData().getAllBackgroundImage()
		emp_data_db=[]

		if(len(emp_data))>0:
			for line in emp_data:
				emp_data_dict={}
				emp_data_dict['id']                 = line[0]
				emp_data_dict['imagePath']          = line[1]
				emp_data_dict['imageName']          = line[2]
				emp_data_dict['status']             = line[3]


				emp_data_db.append(emp_data_dict)


		resp = Response(json.dumps({"success": 1, "configure_data": emp_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/resend/otp/', methods=['GET','POST'])
def AddResendOtp():
	if request.method       == 'POST':
		user_data           =json.loads(request.data)
		mobile              = user_data['mobile']
		otp                = user_data['otp']


		text =" Welcome to IPE Global. Your Login OTP is %s."%(str(otp))

		url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)

		urlfetch.set_default_fetch_deadline(45)
		resp = urlfetch.fetch(url=url,
			method=urlfetch.GET,
			headers={'Content-Type': 'text/html'})
		resp = Response(json.dumps({ "response": "success"}))
		return after_request(resp)

# get user data





@app.route('/api/get/admin/data/',methods=['GET','POST'])
def APiGetAdminData():
	if request.method=='POST':

		user_data = dbhelper.GetData().getAdminUserData()
		user_data_db=[]

		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = str(line[0]).encode('utf-8').strip()
				user_data_dict['name']  = str(line[1]).encode('utf-8').strip()
				user_data_dict['email']  = str(line[2]).encode('utf-8').strip()
				user_data_dict['mobile'] = str(line[3]).encode('utf-8').strip()
				user_data_dict['alternateNo']  = str(line[4]).encode('utf-8').strip()
				user_data_dict['parentName']  = str(line[5]).encode('utf-8').strip()
				user_data_dict['domicile_document']= str(line[6]).encode('utf-8').strip()
				user_data_dict['documentUrl']= str(line[7]).encode('utf-8').strip()
				user_data_dict['dob']= str(line[8]).encode('utf-8').strip()
				user_data_dict['gender']= str(line[9]).encode('utf-8').strip()
				user_data_dict['maritalStatus']= str(line[10]).encode('utf-8').strip()
				user_data_dict['category']= str(line[11]).encode('utf-8').strip()
				user_data_dict['disability']= str(line[12]).encode('utf-8').strip()
				user_data_dict['profile_image']= str(line[13]).encode('utf-8').strip()
				user_data_dict['khasi_read']= str(line[14]).encode('utf-8').strip()
				user_data_dict['khasi_write']= str(line[15]).encode('utf-8').strip()
				user_data_dict['khasi_speak']= str(line[16]).encode('utf-8').strip()
				user_data_dict['garo_read']= str(line[17]).encode('utf-8').strip()
				user_data_dict['garo_write']= str(line[18]).encode('utf-8').strip()
				user_data_dict['garo_speak']= str(line[19]).encode('utf-8').strip()
				user_data_dict['english_read']= str(line[20]).encode('utf-8').strip()
				user_data_dict['english_write']= str(line[21]).encode('utf-8').strip()
				user_data_dict['english_speak']= str(line[22]).encode('utf-8').strip()
				user_data_dict['hindi_read']= str(line[23]).encode('utf-8').strip()
				user_data_dict['hindi_write']= str(line[24]).encode('utf-8').strip()
				user_data_dict['hindi_speak']= str(line[25]).encode('utf-8').strip()
				user_data_dict['other_read']= str(line[26]).encode('utf-8').strip()
				user_data_dict['other_write']=str(line[27]).encode('utf-8').strip()
				user_data_dict['other_speak']= str(line[28]).encode('utf-8').strip()
				user_data_dict['higher_education']= str(line[29]).encode('utf-8').strip()
				user_data_dict['passing_year']= str(line[30]).encode('utf-8').strip()
				user_data_dict['training']= str(line[31]).encode('utf-8').strip()
				user_data_dict['employed']= str(line[32]).encode('utf-8').strip()
				user_data_dict['work_experience']= str(line[33]).encode('utf-8').strip()
				# user_data_dict['employment_prefer']= str(line[34]).encode('utf-8').strip()
				user_data_dict['work_outside']= str(line[35]).encode('utf-8').strip()
				user_data_dict['industry']= str(line[36]).encode('utf-8').strip()
				user_data_dict['expectedSalary']= str(line[37]).encode('utf-8').strip()
				user_data_dict['short_training']= str(line[38]).encode('utf-8').strip()
				user_data_dict['notice_period']= str(line[39]).encode('utf-8').strip()
				user_data_dict['address']= str(line[40]).encode('utf-8').strip()
				user_data_dict['houseNo']= str(line[41]).encode('utf-8').strip()
				user_data_dict['landmark']= str(line[42]).encode('utf-8').strip()
				user_data_dict['city']= str(line[43]).encode('utf-8').strip()
				user_data_dict['state']= str(line[44]).encode('utf-8').strip()
				user_data_dict['pincode']= str(line[45]).encode('utf-8').strip()
				user_data_dict['status']= str(line[46]).encode('utf-8').strip()
				user_data_dict['trainingType']= str(line[47]).encode('utf-8').strip()
				user_data_dict['specialization']= str(line[48]).encode('utf-8').strip()
				user_data_dict['trainingDate']= str(line[49]).encode('utf-8').strip()
				user_data_dict['trainingDuration']= str(line[50]).encode('utf-8').strip()
				user_data_dict['completionDate']= str(line[51]).encode('utf-8').strip()
				user_data_dict['willingState']= str(line[52]).encode('utf-8').strip()
				user_data_dict['willingCity']= str(line[53]).encode('utf-8').strip()



				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/api/student/message/', methods=['GET','POST'])
def ApiUserMessage():
	if request.method  == 'POST':
		user_data =json.loads(request.data)
		mobile = user_data['mobile']
		message  = user_data['message']
		text =message
		url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=innobins2&pwd=api@innobins2&sender=innobi&mobile=%s&msg=%s'%(str(mobile),text)
		print url
		urlfetch.set_default_fetch_deadline(45)
		resp = urlfetch.fetch(url=url,
			method=urlfetch.GET,
			headers={'Content-Type': 'text/html'})

		db={'message':'Message Send',"confirmation":1}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)


# travel

@app.route('/api/get/travel/data/',methods=['GET','POST'])
def APiGetTravelData():
	if request.method=='POST':
		user_details  =json.loads(request.data)
		username = user_details['username']
		user_data = dbhelper.GetData().getTravelData(username)
		user_data_db=[]

		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['username']  = line[1]
				user_data_dict['modeOfTravel']  = line[2]
				user_data_dict['from'] = line[3]
				user_data_dict['To']  = line[4]
				user_data_dict['arrival']  = line[5]
				user_data_dict['trainingCenterName']= line[6]
				user_data_dict['centerAddress']= line[7]
				user_data_dict['centerImageUrl']= line[8]
				user_data_dict['coordinatorName']= line[9]
				user_data_dict['coordinatorContact']= line[10]
				user_data_dict['pickupLocation']= line[11]
				user_data_dict['pickupTime']= line[12]
				user_data_dict['pickupThrough']= line[13]
				user_data_dict['departure']= line[14]
				user_data_dict['name']= line[15]
				user_data_dict['trainingCity']= line[16]




				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/user/notice/',methods=['GET','POST'])
def APiGetUserNotice():
	if request.method=='POST':
		user_details  =json.loads(request.data)

		mobile = user_details['mobile']
		message_data = dbhelper.GetData().getUserNotice(mobile)
		message_data_db=[]

		if(len(message_data))>0:
			for line in message_data:
				message_data_dict={}
				message_data_dict['id']  = line[0]
				message_data_dict['mobile']  = line[1]
				message_data_dict['message']  = line[2]
				message_data_dict['titles'] = line[3]
				message_data_dict['dateNow']  = str(line[4])
				message_data_dict['time']  = line[5]

				message_data_db.append(message_data_dict)

		resp = Response(json.dumps({"success": True, "message_data": message_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/event/notice/',methods=['GET','POST'])
def APiGetEventNotice():
	if request.method=='POST':
		event_data = dbhelper.GetData().getEventNotice()
		event_data_db=[]

		if(len(event_data))>0:
			for line in event_data:
				event_data_dict={}
				event_data_dict['id']  = line[0]
				event_data_dict['date']  = line[1]
				event_data_dict['time']  = line[2]
				event_data_dict['venue'] = line[3]
				event_data_dict['coordinatorContact'] = line[4]

				event_data_db.append(event_data_dict)

		resp = Response(json.dumps({"success": True, "event_data": event_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/api/add/travel/data/',methods=['GET','POST'])
def APiaddTravelData():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		username= userInfo['username']
		modeOfTravel = userInfo['modeOfTravel']
		origin = userInfo['origin']
		destination= userInfo['destination']
		arrival       = userInfo['arrival']
		trainingCenterName= userInfo['trainingCenterName']
		centerAddress = userInfo['centerAddress']
		centerImageUrl   = userInfo['centerImageUrl']
		coordinatorName= userInfo['coordinatorName']
		coordinatorContact        = userInfo['coordinatorContact']
		pickupLocation= userInfo    ['pickupLocation']
		pickupTime = userInfo['pickupTime']
		pickupThrough = userInfo['pickupThrough']
		departure = userInfo['departure']
		name = userInfo['Name']
		trainingCity    = userInfo['trainingCity']

		travel_status =dbhelper.GetData().getTravelstatus(username)
		if travel_status ==True:
			out  =dbhelper.UpdateData().updateTravel(username,modeOfTravel,origin,destination,arrival,trainingCenterName,centerAddress,centerImageUrl,coordinatorName,coordinatorContact,pickupLocation,pickupTime,pickupThrough,departure,name,trainingCity)
		else:
			AddUser = dbhelper.AddData().addTravel(username,modeOfTravel,origin,destination,arrival,trainingCenterName,centerAddress,centerImageUrl,coordinatorName,coordinatorContact,pickupLocation,pickupTime,pickupThrough,departure,name,trainingCity)

		db={'message':'User Added',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

# TrainingData

@app.route('/api/add/training/data/',methods=['GET','POST'])
def APiaddTrainData():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile= userInfo['mobile']
		organizationName = userInfo['organizationName']
		individual = userInfo['individual']
		hostel_location= userInfo['hostel_location']
		warden        = userInfo['warden']
		contact_details= userInfo['contact_details']
		buddy_name1 = userInfo['buddy_name1']
		buddy_name2  = userInfo['buddy_name2']
		buddy_name3= userInfo['buddy_name3']
		buddy_name4       = userInfo['buddy_name4']
		trainingName = userInfo['trainingName']
		trainingDuration = userInfo['trainingDuration']
		trainingLocation = userInfo['trainingLocation']
		material_docs_link = userInfo['material_docs_link']
		material_video_link = userInfo['material_video_link']
		buddy_contact1 = userInfo['buddy_contact1']
		buddy_contact2 = userInfo['buddy_contact2']
		buddy_contact3 = userInfo['buddy_contact3']
		buddy_contact4  = userInfo['buddy_contact4']
		startDate = userInfo['startDate']
		endDate = userInfo['endDate']

		training_status =dbhelper.GetData().getTrainingstatus(mobile)
		if training_status ==True:
			out  =dbhelper.UpdateData().updateTraining(mobile,organizationName,individual,hostel_location,warden,contact_details,buddy_name1,buddy_name2,buddy_name3,buddy_name4,trainingName,trainingDuration,trainingLocation,material_docs_link,material_video_link,buddy_contact1,buddy_contact2,buddy_contact3,buddy_contact4,startDate,endDate)
		else:
			AddUser = dbhelper.AddData().addTraining(mobile,organizationName,individual,hostel_location,warden,contact_details,buddy_name1,buddy_name2,buddy_name3,buddy_name4,trainingName,trainingDuration,trainingLocation,material_docs_link,material_video_link,buddy_contact1,buddy_contact2,buddy_contact3,buddy_contact4,startDate,endDate)

		db={'message':'User Added',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)



@app.route('/api/add/insurance/data/',methods=['GET','POST'])
def APiaddInsuranceData():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		username= userInfo['username']
		validFrom = userInfo['validFrom']
		validTo = userInfo['validTo']
		companyLink= userInfo['companyLink']
		insurancePdfLink = userInfo['insurancePdfLink']

		insurance_status =dbhelper.GetData().getInsurancestatus(username)
		if insurance_status ==True:
			out  =dbhelper.UpdateData().updateInsurance(username,validFrom,validTo,companyLink,insurancePdfLink)
		else:
			AddUser = dbhelper.AddData().addInsurance(username,validFrom,validTo,companyLink,insurancePdfLink)

		db={'message':'User Added',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)



@app.route('/api/add/user/feedback/',methods=['GET','POST'])
def APiaddFeedback():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		username= userInfo['username']
		rating = userInfo['rating']
		feedback = userInfo['feedback']
		comment= userInfo['comment']

		AddUser = dbhelper.AddData().addFeedback(username,rating,feedback,comment)

		db={'message':'User Added',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/api/add/user/survey/',methods=['GET','POST'])
def APiaddSurvey():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		username= userInfo['username']
		funded = userInfo['funded']
		deficiencies = userInfo['deficiencies']
		adoptable= userInfo['adoptable']
		recruitment = userInfo['recruitment']
		multiskilling = userInfo['multiskilling']

		AddUser = dbhelper.AddData().addSurvey(username,funded,deficiencies,adoptable,recruitment,multiskilling)

		db={'message':'User Added',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


# Api candidate user update


@app.route('/api/candidate/basic/data/',methods=['GET','POST'])
def APiCandidateBasicData():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		print userInfo
		mobile  = userInfo['mobile']
		domicile_document= userInfo['domicile_document']
		documentUrl  = ""
		dob= userInfo['dob']
		gender= userInfo['gender']
		# maritalStatus  = userInfo['maritalStatus']
		category= userInfo['category']
		govtIdType= userInfo['govtIdType']
		govtIdOthers= userInfo['govtIdOthers']
		govtIdNo= userInfo['govtIdNo']
		govtIdImage= userInfo['govtIdImage']

		EditAssign = dbhelper.UpdateData().UpdateBasicData(mobile,domicile_document,dob,gender,category,govtIdType,govtIdOthers,govtIdNo,govtIdImage)
		db={"success": True,'message':'UserDataUpdate',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

# update qualification
@app.route('/api/candidate/update/qualification/',methods=['GET','POST'])
def APiCandidateQuali():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		print userInfo
		mobile  = userInfo['mobile']
		higher_education= userInfo['higher_education']
		course  = userInfo['course']
		pQualification= userInfo['pQualification']
		pCourse= userInfo['pCourse']
		# maritalStatus  = userInfo['maritalStatus']
		pPassingYear= userInfo['pPassingYear']
		passing_year= userInfo['passing_year']

		EditAssign = dbhelper.UpdateData().UpdateCandidateQuali(mobile,higher_education,course,pQualification,pCourse,pPassingYear,passing_year)
		db={"success": True,'message':'UserDataUpdate',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/api/candidate/address/data/',methods=['GET','POST'])
def APiCandidateAddData():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		address= userInfo['address']
		houseNo  = userInfo['houseNo']
		city= userInfo['city']
		state= userInfo['state']
		pincode  = userInfo['pincode']


		try:
			pAddress1  = userInfo['pAddress1']
		except:
			pAddress1  =''

		try:
			pAddress2  = userInfo['pAddress2']
		except:
			pAddress2  =''

		try:
			pVillage= userInfo['pVillage']
		except:
			pVillage=''

		try:
			pState  = userInfo['pState']
		except:
			pState=''

		try:
			pCity= userInfo['pCity']
		except:
			pCity=''
		try:
			pPincode  = userInfo['pPincode']
		except:
			pPincode=''

		registration_status =dbhelper.GetData().getRegistrationStatusNew(mobile)


		if len(registration_status)>0 and  registration_status[0][0] is not None:

			registration_code=registration_status[0][0]
			db= {'message':'Already Registered',"confirmation":2, "registration_code":registration_code}

		else:
			lastId           =dbhelper.GetData().getLastID()[0][0]
			if lastId:
				newid=str(123+lastId)
			else:
				newid=str(123)



			registration_code = 'MSOPA'  + newid
			EditAssign = dbhelper.UpdateData().UpdateUserAddData(mobile,address,houseNo,city,state,pincode,pAddress1,pAddress2,pVillage,pState,pCity,registration_code)
			db={'message':'UserDataUpdate',"confirmation":1, "registration_code": registration_code}
			text="Congratulations+!+Your+Form+has+been+Submitted+Succesfully.Your+Registration+No+is '%s'"%(registration_code)

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)

			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)



@app.route('/api/user/train/data/',methods=['GET','POST'])
def APiUserTrainData():
	if request.method=='POST':
		userInfo   = json.loads(request.data)

		mobile  = userInfo['mobile']
		khasi_read  = userInfo['khasi_read']
		khasi_write= userInfo['khasi_write']
		khasi_speak  = userInfo['khasi_speak']
		garo_read= userInfo['garo_read']
		garo_write  = userInfo['garo_write']
		garo_speak= userInfo['garo_speak']
		english_read  = userInfo['english_read']
		english_write= userInfo['english_write']
		english_speak  = userInfo['english_speak']
		hindi_read= userInfo['hindi_read']
		hindi_write  = userInfo['hindi_write']
		hindi_speak= userInfo['hindi_speak']
		other_read  = userInfo['other_read']
		other_write= userInfo['other_write']
		other_speak  = userInfo['other_speak']
		training= userInfo['training']
		trainingType= userInfo['trainingType']
		specialization  = userInfo['specialization']
		trainingDate= userInfo['trainingDate']
		trainingDuration  = userInfo['trainingDuration']
		completionDate= userInfo['completionDate']

		EditAssign = dbhelper.UpdateData().UpdateUserTrainData(mobile,khasi_read,khasi_write,khasi_speak,garo_read,garo_write,garo_speak,english_read,english_write,english_speak,hindi_read,hindi_write,hindi_speak,other_read,other_write,other_speak,training,trainingType,specialization,trainingDate,trainingDuration,completionDate)
		db={'message':'UserDataUpdate',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

# train



# employemtn

@app.route('/api/employment/data/',methods=['GET','POST'])
def APiEmploymentData():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		health= userInfo['health']
		hospitality  = userInfo['hospitality']
		tourism= userInfo['tourism']
		it  = userInfo['it']
		retail= userInfo['retail']
		manufacturing  = userInfo['manufacturing']
		food= userInfo['food']
		construction= userInfo['construction']
		education= userInfo['education']
		banking= userInfo['banking']
		others= userInfo['others']
		short_training= userInfo['short_training']



		EditAssign = dbhelper.UpdateData().UpdateEmploymentData(mobile,health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others,short_training)
		db={'message':'UserDataUpdate',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/api/add/upload/document/',methods=['GET','POST'])
def APiuploaddocument():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		stipendStr1= userInfo['stipendStr1']
		stipendStr2  = userInfo['stipendStr2']
		stipendStr3= userInfo['stipendStr3']

		EditAssign = dbhelper.UpdateData().Updatedocuments(mobile,stipendStr1,stipendStr2,stipendStr3)
		db={'message':'UserDataUpdate',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)



@app.route('/api/get/state/list/',methods=['POST'])
def APiStateList():
	if request.method=='POST':


		state_data = dbhelper.GetData().getStateList()
		state_data_db=[]

		if(len(state_data))>0:
			for line in state_data:
				state_data_dict={}
				state_data_dict['state']  = line[0]



				state_data_db.append(state_data_dict)


		resp = Response(json.dumps({"success": 1, "configure_data": state_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/register/id/',methods=['POST'])
def APiGetRegister():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']


		state_data = dbhelper.GetData().getRegisterId(mobile)
		state_data_db=[]

		if(len(state_data))>0:
			for line in state_data:
				state_data_dict={}
				state_data_dict['registrationId']  = line[0]



				state_data_db.append(state_data_dict)


		resp = Response(json.dumps({"success": 1, "configure_data": state_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/api/get/district/list/',methods=['POST'])
def APiDistrictList():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		state  = userInfo['state']

		state_data = dbhelper.GetData().getDistrictList()
		state_data_db=[]

		if(len(state_data))>0:
			for line in state_data:
				state_data_dict={}
				state_data_dict['city']  = line[0]

				state_data_db.append(state_data_dict)


		resp = Response(json.dumps({"success": 1, "configure_data": state_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/form/status/',methods=['POST'])
def APiFormStatus():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']

		user_data = dbhelper.GetData().getFormStatus(mobile)
		user_data_db=[]

		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['formStatus']  = line[0]

				user_data_db.append(user_data_dict)


		resp = Response(json.dumps({"success": 1, "configure_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/additional/status/',methods=['POST'])
def APiAdditionalStatus():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']

		user_data = dbhelper.GetData().getAdditionalStatus(mobile)
		user_data_db=[]

		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['formStatus']  = line[0]

				user_data_db.append(user_data_dict)


		resp = Response(json.dumps({"success": 1, "configure_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


# delete user

@app.route('/api/delete/user/',methods=['GET','POST'])
def APiDeleteUser():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']



		EditAssign = dbhelper.DeleteData().deleteuser(mobile)
		db={'message':'UserDataUpdate',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

# training information
@app.route('/api/get/training/info/',methods=['POST'])
def APiTrainingInfo():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']

		training_data = dbhelper.GetData().getTrainingList(mobile)
		training_data_db=[]

		if(len(training_data))>0:
			for line in training_data:
				training_data_dict={}
				training_data_dict['id']  = line[0]
				training_data_dict['organizationName']  = line[1]
				training_data_dict['individual']  = line[2]
				training_data_dict['hostel_location']  = line[3]
				training_data_dict['warden']  = line[4]
				training_data_dict['contact_details']  = line[5]
				training_data_dict['buddy_name1']  = line[6]
				training_data_dict['buddy_name2']  = line[7]
				training_data_dict['buddy_name3']  = line[8]
				training_data_dict['buddy_name4']  = line[9]
				training_data_dict['mobile']  = line[10]
				training_data_dict['trainingName']  = line[11]
				training_data_dict['trainingDuration']  = line[12]
				training_data_dict['trainingLocation']  = line[13]
				training_data_dict['material_docs_link']  = line[14]
				training_data_dict['material_video_link']  = line[15]
				training_data_dict['buddy_contact1']  = line[16]
				training_data_dict['buddy_contact2']  = line[17]
				training_data_dict['buddy_contact3']  = line[18]
				training_data_dict['buddy_contact4']  = line[19]
				training_data_dict['startDate']  = line[20]
				training_data_dict['endDate']  = line[21]

				training_data_db.append(training_data_dict)


		resp = Response(json.dumps({"success": 1, "configure_data": training_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/api/get/training/',methods=['POST'])
def APiTraiInfo():
	if request.method=='POST':

		training_data = dbhelper.GetData().getTraining()
		training_data_db=[]

		if(len(training_data))>0:
			for line in training_data:
				training_data_dict={}
				training_data_dict['id']  = line[0]
				training_data_dict['organizationName']  = line[1]
				training_data_dict['individual']  = line[2]
				training_data_dict['hostel_location']  = line[3]
				training_data_dict['warden']  = line[4]
				training_data_dict['contact_details']  = line[5]
				training_data_dict['buddy_name1']  = line[6]
				training_data_dict['buddy_name2']  = line[7]
				training_data_dict['buddy_name3']  = line[8]
				training_data_dict['buddy_name4']  = line[9]
				training_data_dict['mobile']  = line[10]
				training_data_dict['trainingName']  = line[11]
				training_data_dict['trainingDuration']  = line[12]
				training_data_dict['trainingLocation']  = line[13]
				training_data_dict['material_docs_link']  = line[14]
				training_data_dict['material_video_link']  = line[15]
				training_data_dict['buddy_contact1']  = line[16]
				training_data_dict['buddy_contact2']  = line[17]
				training_data_dict['buddy_contact3']  = line[18]
				training_data_dict['buddy_contact4']  = line[19]
				training_data_dict['startDate']  = str(line[20])
				training_data_dict['endDate']  = str(line[21])

				training_data_db.append(training_data_dict)


		resp = Response(json.dumps({"success": 1, "configure_data": training_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/api/get/candidate/registration/',methods=['POST'])
def APiTrainingRegistration():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']

		training_data = dbhelper.GetData().getCandidateRegis(mobile)
		training_data_db=[]

		if(len(training_data))>0:
			for line in training_data:
				training_data_dict={}
				training_data_dict['id']  = line[0]
				training_data_dict['validFrom']  = line[1]
				training_data_dict['validTo']  = line[2]
				training_data_dict['companyLink']  = line[3]
				training_data_dict['insurancePdfLink']  = line[4]
				training_data_dict['mobile']  = line[5]
				training_data_dict['candidatesRegistrationId']  = line[6]

				training_data_db.append(training_data_dict)


		resp = Response(json.dumps({"success": 1, "configure_data": training_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/document/info/new/',methods=['POST'])
def APidocumentupdate():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']

		training_data = dbhelper.GetData().getdocumentinfo(mobile)
		training_data_db=[]

		if(len(training_data))>0:
			for line in training_data:
				training_data_dict={}
				training_data_dict['mobile']  = mobile
				training_data_dict['stipendStr1']  = line[0]
				training_data_dict['stipendStr2']  = line[1]
				training_data_dict['stipendStr3']  = line[2]
				training_data_dict['stipendStatus']  = line[3]


				training_data_db.append(training_data_dict)


		resp = Response(json.dumps({"success": 1, "configure_data": training_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


# user details

@app.route('/api/get/user/details/',methods=['GET','POST'])
def APiGetUserDetails():
	if request.method=='POST':
		user_data = dbhelper.GetData().getUserDetails()
		sno = 0
		user_data_db=[]

		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				sno=sno+1
				user_data_dict['id']  = sno
				user_data_dict['name']  = line[1]
				user_data_dict['email']  = str(line[2]).encode('utf-8').strip()
				user_data_dict['mobile'] = line[3]
				user_data_dict['alternateNo']  = line[4]
				try:
					user_data_dict['parentName']  = str(line[5]).encode('utf-8').strip()
				except:
					user_data_dict['parentName']  =''

				user_data_dict['domicile_document']  = line[6]
				user_data_dict['documentUrl'] = line[7]
				user_data_dict['dob']  = line[8]
				user_data_dict['gender']  = line[9]
				user_data_dict['category']  = line[10]
				user_data_dict['govtIdType'] = line[11]
				user_data_dict['govtIdOthersInput'] = line[12]
				user_data_dict['govtIdNo']  = line[13]
				user_data_dict['govtIdImage']  = line[14]
				user_data_dict['higher_education']  = line[15]
				user_data_dict['course'] = line[16]
				user_data_dict['passing_year']  = line[17]
				user_data_dict['pQualification']  = line[18]
				user_data_dict['pCourse'] = line[19]
				user_data_dict['pPassingYear']  = line[20]
				user_data_dict['skillsets']  = line[21]
				user_data_dict['work_outside'] = line[22]
				user_data_dict['health'] = line[23]
				user_data_dict['hospitality']  = line[24]
				user_data_dict['tourism']  = line[25]
				user_data_dict['it'] = line[26]
				user_data_dict['retail'] = line[27]
				user_data_dict['manufacturing']  = line[28]
				user_data_dict['food']  = line[29]
				user_data_dict['construction'] = line[30]
				user_data_dict['education'] = line[31]
				user_data_dict['banking']  = line[32]
				user_data_dict['others']  = line[33]
				try:
					user_data_dict['address'] = str(line[34]).decode('utf8').encode('utf8')
				except:
					user_data_dict['address'] = ''

				try:
					user_data_dict['houseNo'] = str(line[35]).encode('utf-8').strip()
				except:
					user_data_dict['houseNo'] =''
				try:
					user_data_dict['villageName']  = str(line[36]).encode('utf-8').strip()
				except:
					user_data_dict['villageName']  =''


				user_data_dict['city']  = str(line[37]).encode('utf-8').strip()
				user_data_dict['state'] = str(line[38]).encode('utf-8').strip()
				user_data_dict['pincode']  = line[39]
				user_data_dict['registrationId']  = line[40]
				user_data_dict['maritalStatus'] = line[41]
				user_data_dict['disability']  = line[42]
				user_data_dict['profile_image']  = line[43]
				user_data_dict['khasi_read'] = line[44]
				user_data_dict['khasi_write']  = line[45]
				user_data_dict['khasi_speak']  = line[46]
				user_data_dict['garo_read']= line[47]
				user_data_dict['garo_write']= line[48]
				user_data_dict['garo_speak']= line[49]
				user_data_dict['english_read']= line[50]
				user_data_dict['english_write']= line[51]
				user_data_dict['english_speak']= line[52]
				user_data_dict['hindi_read']= line[53]
				user_data_dict['hindi_write']= line[54]
				user_data_dict['hindi_speak']= line[55]
				user_data_dict['other_read']= line[56]
				user_data_dict['other_write']= line[57]
				user_data_dict['other_speak']= line[58]
				user_data_dict['training']= str(line[59]).encode('utf-8').strip()
				try:
					user_data_dict['trainingType']= str(line[60]).encode('utf-8').strip()
				except:
					user_data_dict['trainingType']= ''

				user_data_dict['specialization']= str(line[61]).encode('utf-8').strip()
				user_data_dict['trainingDate']= str(line[62]).encode('utf-8').strip()
				user_data_dict['trainingDuration']= str(line[63]).encode('utf-8').strip()
				user_data_dict['completionDate']= str(line[64]).encode('utf-8').strip()
				user_data_dict['employed']= str(line[65]).encode('utf-8').strip()
				user_data_dict['work_experience']= str(line[66]).encode('utf-8').strip()
				user_data_dict['employment_prefer']= str(line[67]).encode('utf-8').strip()
				user_data_dict['short_training']= str(line[68]).encode('utf-8').strip()
				user_data_dict['notice_period']= str(line[69]).encode('utf-8').strip()
				user_data_dict['status']= str(line[70]).encode('utf-8').strip()
				try:
					user_data_dict['pAddress1']= str(line[71]).encode('utf-8').strip()
				except:
					user_data_dict['pAddress1']=''

				try:
					user_data_dict['pAddress2']=str(line[72]).encode('utf-8').strip()
				except:
					user_data_dict['pAddress2']=''

				try:
					user_data_dict['pVillage']= str(line[73]).encode('utf-8').strip()
				except:
					user_data_dict['pVillage']= ''

				user_data_dict['pState']= 'Meghalaya'
				user_data_dict['pCity']= str(line[75]).encode('utf-8').strip()
				user_data_dict['pPincode']= line[76]
				user_data_dict['createdAt']= str(line[78])




				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/api/attendance/notice/', methods=['GET','POST'])
def fcmCustomerPriceNotice():

	if request.method    == 'POST':
		token_data        =json.loads(request.data)
		print token_data
		deviceLst         =token_data['deviceLst']
		message           = token_data['message']
		titles           = token_data['titles']
		dateNow           = str(date.today())
		print dateNow
		time              = (datetime.now() + timedelta(hours=05,minutes=30)).strftime("%H:%M")

		print time

		fcmTokenList         =dbhelper.GetData().getToken(deviceLst)
		print fcmTokenList
		if len(fcmTokenList)>0:
			for gcmT in fcmTokenList:
				print gcmT[0]
				mobile = gcmT[1]
				UpDateConfigure = dbhelper.AddData().AddNotification(mobile,message,titles,dateNow,time)


				message_data={   "notification":{"action":"Notification","body":message,"title":titles,"imageUrl":"http://s33.postimg.org/slnc2rtwv/logo.png"},





						"to" : gcmT[0]
				}
				form_data = json.dumps(message_data)



				url='https://fcm.googleapis.com/fcm/send'
				urlfetch.set_default_fetch_deadline(45)

				resp = urlfetch.fetch(url=url,
					method=urlfetch.POST,
					payload=form_data,
					headers={"Authorization":"key=AAAAgoXYw2U:APA91bHFLKCcBzp0Jy9ZrRwjJnocYixy9HmsS2uhbbBEi1le91muMJcWV6Omk0gY1zt6jR1hpbG_pF7JQB-V0GGFTfDTFR3GOjjino9-us9MCNP7zSOAP4GQ9rOlywJMPg0Me9zctIcz", "Content-Type":"application/json"}
					)




				print resp.content



			response = Response(json.dumps({"response":{"confirmation": 1}}))
			return after_request(response)

		else:
			response = Response(json.dumps({"response":{"confirmation": 0}}))
			return after_request(response)




@app.route('/api/get/user/data/',methods=['GET','POST'])
def APiGetUserDet():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		user_data = dbhelper.GetData().getUserLogin(mobile)
		sno = 0
		user_data_db=[]

		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				sno=sno+1
				user_data_dict['id']  = sno
				user_data_dict['name']  = line[1]
				user_data_dict['email']  = str(line[2]).encode('utf-8').strip()
				user_data_dict['mobile'] = line[3]
				user_data_dict['alternateNo']  = line[4]
				try:
					user_data_dict['parentName']  = str(line[5]).encode('utf-8').strip()
				except:
					user_data_dict['parentName']  =''
				# user_data_dict['parentName']  = str(line[5]).encode('utf-8').strip()
				user_data_dict['domicile_document']  = line[6]
				user_data_dict['documentUrl'] = line[7]
				user_data_dict['dob']  = line[8]
				user_data_dict['gender']  = line[9]
				user_data_dict['category']  = line[10]
				user_data_dict['govtIdType'] = line[11]
				user_data_dict['govtIdOthersInput'] = line[12]
				user_data_dict['govtIdNo']  = line[13]
				user_data_dict['govtIdImage']  = line[14]
				user_data_dict['higher_education']  = line[15]
				user_data_dict['course'] = line[16]
				user_data_dict['passing_year']  = line[17]
				user_data_dict['pQualification']  = line[18]
				user_data_dict['pCourse'] = line[19]
				user_data_dict['pPassingYear']  = line[20]
				user_data_dict['skillsets']  = line[21]
				user_data_dict['work_outside'] = line[22]
				user_data_dict['health'] = line[23]
				user_data_dict['hospitality']  = line[24]
				user_data_dict['tourism']  = line[25]
				user_data_dict['it'] = line[26]
				user_data_dict['retail'] = line[27]
				user_data_dict['manufacturing']  = line[28]
				user_data_dict['food']  = line[29]
				user_data_dict['construction'] = line[30]
				user_data_dict['education'] = line[31]
				user_data_dict['banking']  = line[32]
				user_data_dict['others']  = line[33]
				try:
					user_data_dict['address'] = str(line[34]).decode('utf8').encode('utf8')
				except:
					user_data_dict['address'] = ''

				try:
					user_data_dict['houseNo'] = str(line[35]).encode('utf-8').strip()
				except:
					user_data_dict['houseNo'] =''
				try:
					user_data_dict['villageName']  = str(line[36]).encode('utf-8').strip()
				except:
					user_data_dict['villageName']  =''


				user_data_dict['city']  = str(line[37]).encode('utf-8').strip()
				user_data_dict['state'] = str(line[38]).encode('utf-8').strip()
				user_data_dict['pincode']  = line[39]
				user_data_dict['registrationId']  = line[40]
				user_data_dict['maritalStatus'] = line[41]
				user_data_dict['disability']  = line[42]
				user_data_dict['profile_image']  = line[43]
				user_data_dict['khasi_read'] = line[44]
				user_data_dict['khasi_write']  = line[45]
				user_data_dict['khasi_speak']  = line[46]
				user_data_dict['garo_read']= line[47]
				user_data_dict['garo_write']= line[48]
				user_data_dict['garo_speak']= line[49]
				user_data_dict['english_read']= line[50]
				user_data_dict['english_write']= line[51]
				user_data_dict['english_speak']= line[52]
				user_data_dict['hindi_read']= line[53]
				user_data_dict['hindi_write']= line[54]
				user_data_dict['hindi_speak']= line[55]
				user_data_dict['other_read']= line[56]
				user_data_dict['other_write']= line[57]
				user_data_dict['other_speak']= line[58]
				user_data_dict['training']= str(line[59]).encode('utf-8').strip()
				try:
					user_data_dict['trainingType']= str(line[60]).encode('utf-8').strip()
				except:
					user_data_dict['trainingType']= ''

				user_data_dict['specialization']= str(line[61]).encode('utf-8').strip()
				user_data_dict['trainingDate']= str(line[62]).encode('utf-8').strip()
				user_data_dict['trainingDuration']= str(line[63]).encode('utf-8').strip()
				user_data_dict['completionDate']= str(line[64]).encode('utf-8').strip()
				user_data_dict['employed']= str(line[65]).encode('utf-8').strip()
				user_data_dict['work_experience']= str(line[66]).encode('utf-8').strip()
				user_data_dict['employment_prefer']= str(line[67]).encode('utf-8').strip()
				user_data_dict['short_training']= str(line[68]).encode('utf-8').strip()
				user_data_dict['notice_period']= str(line[69]).encode('utf-8').strip()
				user_data_dict['status']= str(line[70]).encode('utf-8').strip()
				try:
					user_data_dict['pAddress1']= str(line[71]).encode('utf-8').strip()
				except:
					user_data_dict['pAddress1']=''

				try:
					user_data_dict['pAddress2']=str(line[72]).encode('utf-8').strip()
				except:
					user_data_dict['pAddress2']=''

				try:
					user_data_dict['pVillage']= str(line[73]).encode('utf-8').strip()
				except:
					user_data_dict['pVillage']= ''

				user_data_dict['pState']= 'Meghalaya'
				user_data_dict['pCity']= str(line[75]).encode('utf-8').strip()
				user_data_dict['pPincode']= line[76]
				user_data_dict['createdAt']= str(line[78])
				user_data_dict['motherName']= line[104]
				user_data_dict['secondaryMobile']= line[105]
				user_data_dict['totalMember']= line[106]
				user_data_dict['familyIncome']= line[107]




				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True,"confirmation":1, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/primary/data/',methods=['GET','POST'])
def APiGetPDetails():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		start_date= userInfo['start_date']
		end_date = userInfo['end_date']
		user_data = dbhelper.GetData().getUserPDetails(start_date,end_date)
		sno = 0
		user_data_db=[]

		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				sno=sno+1
				user_data_dict['id']  = sno
				user_data_dict['name']  = line[1]
				user_data_dict['email']  = str(line[2]).encode('utf-8').strip()
				user_data_dict['mobile'] = line[3]
				user_data_dict['alternateNo']  = line[4]
				try:
					user_data_dict['parentName']  = str(line[5]).encode('utf-8').strip()
				except:
					user_data_dict['parentName']  =''
				# user_data_dict['parentName']  = str(line[5]).encode('utf-8').strip()
				user_data_dict['domicile_document']  = line[6]
				user_data_dict['documentUrl'] = line[7]
				user_data_dict['dob']  = line[8]
				user_data_dict['gender']  = line[9]
				user_data_dict['category']  = line[10]
				user_data_dict['govtIdType'] = line[11]
				user_data_dict['govtIdOthersInput'] = line[12]
				user_data_dict['govtIdNo']  = line[13]
				user_data_dict['govtIdImage']  = line[14]
				user_data_dict['higher_education']  = line[15]
				user_data_dict['course'] = line[16]
				user_data_dict['passing_year']  = line[17]
				user_data_dict['pQualification']  = line[18]
				user_data_dict['pCourse'] = line[19]
				user_data_dict['pPassingYear']  = line[20]
				user_data_dict['skillsets']  = line[21]
				user_data_dict['work_outside'] = line[22]
				user_data_dict['health'] = line[23]
				user_data_dict['hospitality']  = line[24]
				user_data_dict['tourism']  = line[25]
				user_data_dict['it'] = line[26]
				user_data_dict['retail'] = line[27]
				user_data_dict['manufacturing']  = line[28]
				user_data_dict['food']  = line[29]
				user_data_dict['construction'] = line[30]
				user_data_dict['education'] = line[31]
				user_data_dict['banking']  = line[32]
				user_data_dict['others']  = line[33]
				try:
					user_data_dict['address'] = str(line[34]).decode('utf8').encode('utf8')
				except:
					user_data_dict['address'] = ''

				try:
					user_data_dict['houseNo'] = str(line[35]).encode('utf-8').strip()
				except:
					user_data_dict['houseNo'] =''
				try:
					user_data_dict['villageName']  = str(line[36]).encode('utf-8').strip()
				except:
					user_data_dict['villageName']  =''


				user_data_dict['city']  = str(line[37]).encode('utf-8').strip()
				user_data_dict['state'] = str(line[38]).encode('utf-8').strip()
				user_data_dict['pincode']  = line[39]
				user_data_dict['registrationId']  = line[40]
				user_data_dict['maritalStatus'] = line[41]
				user_data_dict['disability']  = line[42]
				user_data_dict['profile_image']  = line[43]
				user_data_dict['khasi_read'] = line[44]
				user_data_dict['khasi_write']  = line[45]
				user_data_dict['khasi_speak']  = line[46]
				user_data_dict['garo_read']= line[47]
				user_data_dict['garo_write']= line[48]
				user_data_dict['garo_speak']= line[49]
				user_data_dict['english_read']= line[50]
				user_data_dict['english_write']= line[51]
				user_data_dict['english_speak']= line[52]
				user_data_dict['hindi_read']= line[53]
				user_data_dict['hindi_write']= line[54]
				user_data_dict['hindi_speak']= line[55]
				user_data_dict['other_read']= line[56]
				user_data_dict['other_write']= line[57]
				user_data_dict['other_speak']= line[58]
				user_data_dict['training']= str(line[59]).encode('utf-8').strip()
				try:
					user_data_dict['trainingType']= str(line[60]).encode('utf-8').strip()
				except:
					user_data_dict['trainingType']= ''

				user_data_dict['specialization']= str(line[61]).encode('utf-8').strip()
				user_data_dict['trainingDate']= str(line[62]).encode('utf-8').strip()
				user_data_dict['trainingDuration']= str(line[63]).encode('utf-8').strip()
				user_data_dict['completionDate']= str(line[64]).encode('utf-8').strip()
				user_data_dict['employed']= str(line[65]).encode('utf-8').strip()
				user_data_dict['work_experience']= str(line[66]).encode('utf-8').strip()
				user_data_dict['employment_prefer']= str(line[67]).encode('utf-8').strip()
				user_data_dict['short_training']= str(line[68]).encode('utf-8').strip()
				user_data_dict['notice_period']= str(line[69]).encode('utf-8').strip()
				user_data_dict['status']= str(line[70]).encode('utf-8').strip()
				try:
					user_data_dict['pAddress1']= str(line[71]).encode('utf-8').strip()
				except:
					user_data_dict['pAddress1']=''

				try:
					user_data_dict['pAddress2']=str(line[72]).encode('utf-8').strip()
				except:
					user_data_dict['pAddress2']=''

				try:
					user_data_dict['pVillage']= str(line[73]).encode('utf-8').strip()
				except:
					user_data_dict['pVillage']= ''

				user_data_dict['pState']= 'Meghalaya'
				user_data_dict['pCity']= str(line[75]).encode('utf-8').strip()
				user_data_dict['pPincode']= line[76]
				user_data_dict['createdAt']= str(line[78])





				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True,"confirmation":1,"user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

# candidate

@app.route('/api/get/all/user/',methods=['GET','POST'])
def APiGetAllUserData():
	if request.method=='POST':
		user_data = dbhelper.GetData().getAllUserData()
		user_data_db=[]

		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['name']  = line[0]
				user_data_dict['mobile']  = line[1]


				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True,"confirmation":1,"user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


# Attendance

@app.route('/api/employee/attendance/',methods=['GET','POST'])
def ApiemployeeAttendanceInformation():
	if request.method=='POST':

		configure_data              = json.loads(request.data)
		username                     = configure_data['username']

		startDate1                   = configure_data['startDate']
		endDate1                     = configure_data['endDate']
		startDate = datetime.strptime(startDate1, "%m/%d/%Y").strftime("%Y-%m-%d")
		endDate = datetime.strptime(endDate1, "%m/%d/%Y").strftime("%Y-%m-%d")

		attendance_dict = dbhelper.GetData().getEmployeeAttendanceDetail(username,startDate,endDate)

		start_dt = datetime.strptime(startDate1, "%m/%d/%Y").date()
		end_dt = datetime.strptime(endDate1, "%m/%d/%Y").date()


		attendance_info_data_db = []
		for dt in daterange(start_dt, end_dt):
			_dt_= datetime.strftime(dt, "%m/%d/%Y")
			if str(_dt_) in attendance_dict:
				attendance_info_data_dict = {}
				attendance_info_data_dict['username']                  =attendance_dict[str(_dt_)][1]
				attendance_info_data_dict['date']                     =attendance_dict[str(_dt_)][2]
				attendance_info_data_dict['reportInTime']             =attendance_dict[str(_dt_)][3]
				attendance_info_data_dict['reportOutTime']            =attendance_dict[str(_dt_)][4]
				attendance_info_data_dict['reportInAddress']          =attendance_dict[str(_dt_)][5]
				attendance_info_data_dict['reportOutAddress']         =attendance_dict[str(_dt_)][6]
				attendance_info_data_dict['inAddrInGeoFans']          =attendance_dict[str(_dt_)][7]
				attendance_info_data_dict['outAddrOutGeoFans']        =attendance_dict[str(_dt_)][8]
				if attendance_dict[str(_dt_)][9]=='1':
					attendance_info_data_dict['status']  ='PRESENT'
				elif attendance_dict[str(_dt_)][9]=='2':
					attendance_info_data_dict['status']  ='PRESENT'
				elif attendance_dict[str(_dt_)][9]=='3':
					attendance_info_data_dict['status']  ='OFF'

				attendance_info_data_db.append(attendance_info_data_dict)

			# elif dt.weekday() == 6:
			# 	attendance_info_data_dict = {}
			# 	attendance_info_data_dict['username']                  =username
			# 	attendance_info_data_dict['date']                     =str(_dt_)
			# 	attendance_info_data_dict['reportInTime']             =""
			# 	attendance_info_data_dict['reportOutTime']            =""
			# 	attendance_info_data_dict['reportInAddress']          =""
			# 	attendance_info_data_dict['reportOutAddress']         =""
			# 	attendance_info_data_dict['inAddrInGeoFans']          =""
			# 	attendance_info_data_dict['outAddrOutGeoFans']        =""
			# 	attendance_info_data_dict['status']                   ='WeekendOff'
			# 	attendance_info_data_db.append(attendance_info_data_dict)

			else:
				attendance_info_data_dict = {}
				attendance_info_data_dict['username']                  =username
				attendance_info_data_dict['date']                     =str(_dt_)
				attendance_info_data_dict['reportInTime']             =""
				attendance_info_data_dict['reportOutTime']            =""
				attendance_info_data_dict['reportInAddress']          =""
				attendance_info_data_dict['reportOutAddress']         =""
				attendance_info_data_dict['inAddrInGeoFans']          =""
				attendance_info_data_dict['outAddrOutGeoFans']        =""
				attendance_info_data_dict['status']                   ='ABSENT'
				attendance_info_data_db.append(attendance_info_data_dict)

			# attendance_total_data_dict = {}
			# attendance_total_data_dict['present']                  = present
			# attendance_total_data_dict['absent']                   = absent
			# attendance_total_data_dict['WeekendOff']               = WeekendOff

			# attendance_in_data_db.append(attendance_total_data_dict)









		resp = Response(json.dumps({"success": 1, "attendance_data":attendance_info_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/api/attendance/punchin/',methods=['GET','POST'])
def ApiAddAttendance():
	if request.method=='POST':

		attendance_data         = json.loads(request.data)
		print attendance_data
		username                 = attendance_data['username']
		date                    = attendance_data['date']
		reportInTime            = attendance_data['reportInTime']
		try:
			reportInAddress         = attendance_data['reportInAddress']
		except:
			reportInAddress =""

		inAddrInGeoFans         = attendance_data['inAddrInGeoFans']
		status                  = "1"
		createdAt               = str(datetime.now())
		attendanceStatus      ="Not Approved"



		AddTodayAttendance = dbhelper.AddData().AddAttendance(username,date,reportInTime,reportInAddress,inAddrInGeoFans,status,createdAt,attendanceStatus)
		print AddTodayAttendance
		if AddTodayAttendance==0:
			d={"confirmation":0}
		else:
			d={"confirmation":1}

		resp = Response(json.dumps({"success": True, "datasets":d}))
		return after_request(resp)


@app.route('/api/attendance/punchout/',methods=['GET','POST'])
def APiAttendance():
	if request.method=='POST':
		attendanceInfo = json.loads(request.data)
		username  = attendanceInfo['username']
		reportOutTime = attendanceInfo['reportOutTime']
		try:
			reportOutAddress  = attendanceInfo['reportOutAddress']
		except:
			reportOutAddress=""
		outAddrOutGeoFans = attendanceInfo['outAddrOutGeoFans']
		updatedAt  = str(datetime.now())

		attendance_status          =dbhelper.GetData().getAttendanceStatus(username)
		if attendance_status==True:
			out=dbhelper.UpdateData().updateAttendance(username,reportOutTime,reportOutAddress,outAddrOutGeoFans,updatedAt)
			if out==0:
				d={"confirmation":1}
			else:
				d={"confirmation":0}
		else:
			d={"confirmation":2}




	resp = Response(json.dumps({"success": True, "datasets": d}))
	return after_request(resp)


@app.route('/api/check/attendance/',methods=['GET','POST'])
def ApiAttendanceInformation():
	if request.method=='POST':

		configure_data  = json.loads(request.data)
		username   = configure_data['username']
		now  = datetime.today()
		date  = now.strftime('%m/%d/%Y')


		attendance_info_data = dbhelper.GetData().getAttendanceDetail(username,date)
		attendance_info_data_db = []

		if(len(attendance_info_data))>0:
			for line in attendance_info_data:
				attendance_info_data_dict = {}
				attendance_info_data_dict['username']                  =line[1]
				attendance_info_data_dict['date']                     =line[2]
				attendance_info_data_dict['reportInTime']             =line[3]
				attendance_info_data_dict['reportOutTime']            =line[4]
				attendance_info_data_dict['reportInAddress']          =line[5]
				attendance_info_data_dict['reportOutAddress']         =line[6]
				attendance_info_data_dict['inAddrInGeoFans']          =line[7]
				attendance_info_data_dict['outAddrOutGeoFans']        =line[8]
				attendance_info_data_dict['status']        =line[9]



				attendance_info_data_db.append(attendance_info_data_dict)


		resp = Response(json.dumps({"success": 1, "Attendance_data":attendance_info_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

# api user attendance
@app.route('/api/user/attendance/',methods=['GET','POST'])
def ApiUserAttendance():
	if request.method=='POST':

		attendance_info_data = dbhelper.GetData().getUserAttendance()
		attendance_info_data_db = []

		if(len(attendance_info_data))>0:
			for line in attendance_info_data:
				attendance_info_data_dict = {}
				attendance_info_data_dict['username']                 =line[1]
				attendance_info_data_dict['date']                     =line[2]
				attendance_info_data_dict['reportInTime']             =line[3]
				attendance_info_data_dict['reportOutTime']            =line[4]
				attendance_info_data_dict['reportInAddress']          =line[5]
				attendance_info_data_dict['reportOutAddress']         =line[6]
				attendance_info_data_db.append(attendance_info_data_dict)


		resp = Response(json.dumps({"success": 1, "Attendance_data":attendance_info_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/api/mtrack/file/upload/',methods=['GET','POST'])
def apiMtrackFileUpload():
	if request.method=='POST':
		file_object = request.files['file']

		BUCKET_NAME = 'mtrac-b56ab.appspot.com'
		storage = googleapiclient.discovery.build('storage', 'v1')

		print '**',file_object, type(file_object)
		GCS_UPLOAD_FOLDER = 'skill'

		filename = file_object.filename
		print filename
		string_io_file = StringIO.StringIO(file_object.stream.read())

		fullName = GCS_UPLOAD_FOLDER + '/'+ filename
		print fullName
		body = {
			'name': fullName,
		}

		req = storage.objects().insert(bucket=BUCKET_NAME, body=body, media_body=googleapiclient.http.MediaIoBaseUpload(string_io_file, 'application/octet-stream'))
		response = req.execute()

		resp = Response(json.dumps({"success": True, "datasets": 'Yahoo'}))
		return after_request(resp)


@app.route('/api/youthjobs/file/upload/',methods=['GET','POST'])
def apiyouthFileUpload():
	if request.method=='POST':
		file_object = request.files['file']

		BUCKET_NAME = 'mtrac-b56ab.appspot.com'
		storage = googleapiclient.discovery.build('storage', 'v1')

		print '**',file_object, type(file_object)
		GCS_UPLOAD_FOLDER = 'youthjobs'

		filename = file_object.filename
		print filename
		string_io_file = StringIO.StringIO(file_object.stream.read())

		fullName = GCS_UPLOAD_FOLDER + '/'+ filename
		print fullName
		body = {
			'name': fullName,
		}

		req = storage.objects().insert(bucket=BUCKET_NAME, body=body, media_body=googleapiclient.http.MediaIoBaseUpload(string_io_file, 'application/octet-stream'))
		response = req.execute()

		resp = Response(json.dumps({"success": True, "datasets": 'Yahoo'}))
		return after_request(resp)

# Travel and logistics
@app.route('/api/user/travel/',methods=['GET','POST'])
def ApiUserTravel():
	if request.method=='POST':

		travel_info_data = dbhelper.GetData().getUserTravel()
		travel_info_data_db = []

		if(len(travel_info_data))>0:
			for line in travel_info_data:
				travel_info_data_dict = {}
				travel_info_data_dict['username'] =line[1]
				travel_info_data_dict['modeOfTravel'] =line[2]
				travel_info_data_dict['From'] =line[3]
				travel_info_data_dict['To'] =line[4]
				travel_info_data_dict['arrival'] =line[5]
				travel_info_data_dict['trainingCenterName'] =line[6]
				travel_info_data_dict['centerAddress'] =line[7]
				travel_info_data_dict['centerImageUrl'] =line[8]
				travel_info_data_dict['coordinatorName']  =line[9]
				travel_info_data_dict['coordinatorContact']  =line[10]
				travel_info_data_dict['pickupLocation']  =line[11]
				travel_info_data_dict['pickupTime'] =line[12]
				travel_info_data_dict['pickupThrough']=line[13]
				travel_info_data_dict['departure'] =line[14]
				travel_info_data_dict['name'] =line[15]
				travel_info_data_dict['trainingCity'] =line[16]


				travel_info_data_db.append(travel_info_data_dict)


		resp = Response(json.dumps({"success": 1, "travel_data":travel_info_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/api/get/payment/details/',methods=['GET','POST'])
def APiPaymentDeatils():
	if request.method=='POST':
		payment_data        =json.loads(request.data)
		mobile              =payment_data['mobile']
		current_balance        = dbhelper.GetData().getClosingBalance(mobile)[0][0]
		payment_data                = dbhelper.GetData().getPaymentData(mobile)
		payment_data_db=[]

		if(len(payment_data))>0:
			for line in payment_data:
				payment_data_dict={}
				payment_data_dict['date']                           = line[0]
				payment_data_dict['time']                           = line[1]
				payment_data_dict['payment_id']                     = line[2]
				payment_data_dict['from']                           = line[3]
				payment_data_dict['status']                         = line[4]
				payment_data_dict['mobile']                         = line[5]
				payment_data_dict['recharge_amount']                = line[6]
				payment_data_dict['balanceStatus']                 = line[7]
				payment_data_dict['reason']                         = line[8]
				balance_data                                        = dbhelper.GetData().getClosingBalance(mobile)
				if (len(balance_data))>0:
					payment_data_dict['closing_balance']            = balance_data[0][0]
				else:
					payment_data_dict['closing_balance']            = 0





				payment_data_db.append(payment_data_dict)
		else:
			payment_data_db = {}

		resp = Response(json.dumps({"success": True, "payment_data": payment_data_db,"current_balance": current_balance }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/api/admin/payment/details/',methods=['GET','POST'])
def APiAdminPaymentDeatils():
	if request.method=='POST':
		payment_data        =json.loads(request.data)
		mobile              =payment_data['mobile']

		Balance        = dbhelper.GetData().getClosingBalance(mobile)
		current_balance = Balance[0][0]
		name   = Balance[0][1]

		payment_data                = dbhelper.GetData().getPaymentData(mobile)
		payment_data_db=[]

		if(len(payment_data))>0:
			for line in payment_data:
				payment_data_dict={}
				payment_data_dict['date']                           = line[0]
				payment_data_dict['time']                           = line[1]
				payment_data_dict['payment_id']                     = line[2]
				payment_data_dict['from']                           = line[3]
				payment_data_dict['status']                         = line[4]
				payment_data_dict['mobile']                         = line[5]
				payment_data_dict['recharge_amount']                = line[6]
				if line[7]==1:
					payment_data_dict['balanceStatus'] = 'Credit'
				else:
					payment_data_dict['balanceStatus'] ='Debit'
				payment_data_dict['reason']                         = line[8]
				balance_data                                        = dbhelper.GetData().getClosingBalance(mobile)
				if (len(balance_data))>0:
					payment_data_dict['closing_balance']            = balance_data[0][0]
				else:
					payment_data_dict['closing_balance']            = 0

				payment_data_db.append(payment_data_dict)
		else:
			payment_data_db = {}

		resp = Response(json.dumps({"success": True, "payment_data": payment_data_db,"current_balance": current_balance,"name":name }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/api/admin/partner/balance/', methods=['GET','POST'])
def AdminPartnerBalance():
	if request.method       == 'POST':
		payment_data        =json.loads(request.data)
		mobile              =payment_data['mobile']
		balance             =payment_data['balance']
		promocode           =""
		strDate    = str(date.today())
		dateNow   = datetime.strptime(strDate, "%Y-%m-%d").strftime("%d/%m/%Y")

		time                ="01:55 PM"
		paymentId           ="ServAdmin"
		From                ="Servsimplified "
		balanceStatus              =payment_data['status']
		print balanceStatus


		reason              =payment_data['reason']
		if balanceStatus =="1":
			last=dbhelper.AddData().addAdminBalance(mobile,balance,promocode,dateNow,time,paymentId,From,balanceStatus,reason)
		else:
			last=dbhelper.AddData().addAdminDebitBalance(mobile,balance,promocode,dateNow,time,paymentId,From,balanceStatus,reason)

		if last:
			db={'message':'Payment Added',"confirmation":1}
		else:
			db={'message': 'Payment not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)


@app.route('/api/candidate/data/',methods=['GET','POST'])
def ApiCandidate():
	if request.method=='POST':

		candidate_info_data = dbhelper.GetData().getCandidata()
		candidate_info_data_db = []

		if(len(candidate_info_data))>0:
			for line in candidate_info_data:
				candidate_info_data_dict = {}
				candidate_info_data_dict['name']  =line[0]
				candidate_info_data_dict['mobile'] =line[1]
				candidate_info_data_dict['city']  =line[2]
				candidate_info_data_dict['state'] =line[3]
				candidate_info_data_dict['balance'] =line[4]


				candidate_info_data_db.append(candidate_info_data_dict)


		resp = Response(json.dumps({"success": 1, "Candidate_data":candidate_info_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

# Bank
@app.route('/api/add/user/account/',methods=['GET','POST'])
def APiUserAccount():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		account_holder= userInfo['account_holder']
		account_number  = userInfo['account_number']
		ifsc= userInfo['ifsc']
		bankName= userInfo['bankName']
		pancard= userInfo['pancard']
		check= userInfo['check']
		passbook= userInfo['passbook']


		EditAccount = dbhelper.UpdateData().UpdatePassbook(mobile,account_holder,account_number,ifsc,bankName,pancard,check,passbook)
		db={"success": True,'message':'AccountUpdate',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/api/get/account/info/',methods=['GET','POST'])
def APiAccountUpload():
	if request.method=='POST':
		imageInfo= json.loads(request.data)
		mobile = imageInfo['mobile']
		user_data = dbhelper.GetData().getUserAccount(mobile)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['mobile']  = line[0]
				user_data_dict['account_holder']  = line[1]
				user_data_dict['account_number']  = line[2]
				user_data_dict['ifsc'] = line[3]
				user_data_dict['bankName']  = line[4]
				user_data_dict['pancard']  = line[5]
				user_data_dict['check']  = line[6]
				user_data_dict['passbook']  = line[7]
				user_data_dict['accountStatus']  = line[8]
				user_data_dict['baseUrl']  = "https://storage.googleapis.com/ipeglobal.appspot.com/Document/"


				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/user/summary/',methods=['GET','POST'])
def APiUserSummary():
	if request.method=='POST':
		user_data = dbhelper.GetData().getUserSummary()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['name']  = line[0]
				user_data_dict['email']  = line[1]
				user_data_dict['mobile']  = line[2]
				user_data_dict['registrationId'] = line[3]
				user_data_dict['dob']  = line[4]
				user_data_dict['higher_education']  = line[5]
				user_data_dict['course']  = line[6]
				user_data_dict['employment_prefer'] = line[7]
				user_data_dict['pQualification'] = line[8]

				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/update/user/additional/',methods=['GET','POST'])
def APiUserAdditional():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		maritalStatus= userInfo['maritalStatus']
		category  = userInfo['category']
		disability= userInfo['disability']
		profile_image= userInfo['profile_image']


		EditAccount = dbhelper.UpdateData().UpdateAdditional(mobile,maritalStatus,category,disability,profile_image)
		db={"success": True,'message':'AccountUpdate',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/api/update/user/salary/',methods=['GET','POST'])
def APiUserSalary():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		employed= userInfo['employed']
		employment_prefer  = userInfo['employment_prefer']
		work_experience= userInfo['work_experience']
		short_training= userInfo['short_training']
		notice_period  = userInfo['notice_period']
		companyName= userInfo['companyName']
		workPlace= userInfo['workPlace']
		salary= userInfo['salary']


		EditAccount = dbhelper.UpdateData().UpdateSalary(mobile,employed,employment_prefer,work_experience,short_training,notice_period,companyName,workPlace,salary)
		db={"success": True,'message':'AccountUpdate',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/api/company/response/',methods=['GET','POST'])
def APiCompanyResponse():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		company1= userInfo['company1']
		company2 = userInfo['company2']
		company3= userInfo['company3']
		company4= userInfo['company4']
		response1= userInfo['response1']
		response2 = userInfo['response2']
		response3= userInfo['response3']
		response4= userInfo['response4']


		EditCompany = dbhelper.UpdateData().UpdateCompany(mobile,company1,company2,company3,company4,response1,response2,response3,response4)
		db={"success": True,'message':'AccountUpdate',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/api/company/selection/',methods=['GET','POST'])
def APiCompanySelection():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		print userInfo
		mobile  = userInfo['mobile']
		selectedCompany= userInfo['selectedCompany']
		location = userInfo['location']
		job_role= userInfo['job_role']

		EditCompany = dbhelper.UpdateData().UpdateCompanySelection(mobile,selectedCompany,location,job_role)
		fcmTokenList         =dbhelper.GetData().getSelectedCandToken(mobile)
		if len(fcmTokenList)>0:
			for gcmT in fcmTokenList:
				mobile = gcmT[0]
				# UpDateConfigure = dbhelper.AddData().AddNotification(mobile,message,titles,dateNow,time)
				message_data={   "data":{"action":"Notification","body":mobile,"companyName":selectedCompany,"type":1,"location":location,"job_role":job_role},
							
						"to" : gcmT[0]
				}
				form_data = json.dumps(message_data)
				url='https://fcm.googleapis.com/fcm/send'
				urlfetch.set_default_fetch_deadline(45)

				resp = urlfetch.fetch(url=url,
					method=urlfetch.POST,
					payload=form_data,
					headers={"Authorization":"key=AAAAuLvty7k:APA91bHBHNv4UCwpR9p5WJgMra7On8AKssGS4GFjRAcncvEWqMXNk4VA-hqv-B6n1fPf9uiNI1DGocIDWKfpDRb-BbNEm5yidezzhYhW4aePLABKOnV4z6Nm1yCtn7rr6H3yh4t8DykW", "Content-Type":"application/json"}
					)




				print resp.content
		db={"success": True,'message':'AccountUpdate',"confirmation":1}


		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/api/candidate/ticket/',methods=['GET','POST'])
def APiCandidateTicket():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		print userInfo
		mobile  = userInfo['mobile']
		name= userInfo['name']
		date = userInfo['date']
		time= userInfo['time']
		pdfUrl = userInfo['pdfUrl']

		AddTicket = dbhelper.AddData().AddTicket(mobile,name,date,time,pdfUrl)
		fcmTokenList         =dbhelper.GetData().getSelectedCandToken(mobile)
		if len(fcmTokenList)>0:
			for gcmT in fcmTokenList:
				mobile = gcmT[0]
				# UpDateConfigure = dbhelper.AddData().AddNotification(mobile,message,titles,dateNow,time)
				message_data={   "data":{"action":"Notification","body":mobile,"name":name,"type":2,"date":date,"time":time,"pdfUrl":pdfUrl},
							
						"to" : gcmT[0]
				}
				form_data = json.dumps(message_data)
				url='https://fcm.googleapis.com/fcm/send'
				urlfetch.set_default_fetch_deadline(45)

				resp = urlfetch.fetch(url=url,
					method=urlfetch.POST,
					payload=form_data,
					headers={"Authorization":"key=AAAAuLvty7k:APA91bHBHNv4UCwpR9p5WJgMra7On8AKssGS4GFjRAcncvEWqMXNk4VA-hqv-B6n1fPf9uiNI1DGocIDWKfpDRb-BbNEm5yidezzhYhW4aePLABKOnV4z6Nm1yCtn7rr6H3yh4t8DykW", "Content-Type":"application/json"}
					)


		db={"success": True,'message':'AccountUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/api/get/ticket/info/',methods=['GET','POST'])
def APiTicketInfo():
	if request.method=='POST':
		imageInfo= json.loads(request.data)
		mobile = imageInfo['mobile']
		user_data = dbhelper.GetData().getTicket(mobile)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['mobile']  = line[1]
				user_data_dict['name']  = line[2]
				user_data_dict['date'] = line[3]
				user_data_dict['time']  = line[4]
				user_data_dict['pdfUrl']  = line[5]
				user_data_dict['createdAt']=str(line[6])
				
				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/upload/document/',methods=['GET','POST'])
def APiUploadDocument():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		addressproof= userInfo['addressproof']
		birthcert = userInfo['birthcert']
		castcert= userInfo['castcert']
		policecert= userInfo['policecert']
		healthcert=userInfo['healthcert']


		EditCompany = dbhelper.UpdateData().UpdateDocument(mobile,addressproof,birthcert,castcert,policecert,healthcert)
		db={"success": True,'message':'AccountUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)



@app.route('/api/upload/document/new/',methods=['GET','POST'])
def APiUploadDocumentNew():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		addressproof= userInfo['addressproof']
		birthcert = userInfo['birthcert']
		castcert= userInfo['castcert']
		policecert= userInfo['policecert']
		healthcert=userInfo['healthcert']
		declaircert=userInfo['declaircert']
		try:
			mobdeclarecert= userInfo['mobdeclarecert']
		except:
			mobdeclarecert= ''

		EditCompany = dbhelper.UpdateData().UpdateDocumentNew(mobile,addressproof,birthcert,castcert,policecert,healthcert,declaircert,mobdeclarecert)
		db={"success": True,'message':'AccountUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/api/candidate/response/new/',methods=['GET','POST'])
def APiUploadACandidateNew():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		companyName= userInfo['companyName']
		last   =dbhelper.AddData().addResponse(mobile,companyName)
		if last:
			db={'message':'Response Added',"confirmation":1}
		else:
			db={'message': 'Response not added', "confirmation":0}


		db={"success": True,'message':'AccountUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/api/user/print/status/',methods=['GET','POST'])
def APiPrintStatus():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		strDate = str(date.today())

		EditStatus = dbhelper.UpdateData().UpdatePrintStatus(mobile,strDate)
		db={"success": True,'message':'AccountUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/api/get/document/info/',methods=['GET','POST'])
def APiImageFileUpload():
	if request.method=='POST':
		imageInfo= json.loads(request.data)
		mobile = imageInfo['mobile']
		user_data = dbhelper.GetData().getUserDocument(mobile)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['addressproof']  = line[0]
				user_data_dict['birthcert']  = line[1]
				user_data_dict['castcert']  = line[2]
				user_data_dict['policecert'] = line[3]
				user_data_dict['healthcert']  = line[4]
				user_data_dict['documentStatus']  = line[5]
				user_data_dict['declaircert']=line[6]
				user_data_dict['baseUrl']  = "https://storage.googleapis.com/ipeglobal.appspot.com/Document/"


				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)






# Admin Login
@app.route('/api/admin/post/login/',methods=['GET','POST'])
def ApiAdminLoginData():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		username = configure_data['username']
		password= configure_data['password']
		user_type= configure_data['user_type']
		user_status =dbhelper.GetData().getUserLoginstatus(username)
		print user_status
		if user_status==True:
			login_info_data = dbhelper.GetData().PostAdmintLoginData(username,user_type)
			login_info_data_db = []

			if(len(login_info_data))>0:
				for line in login_info_data:
					login_info_data_dict = {}
					login_info_data_dict['id'] =line[0]
					login_info_data_dict['name'] =line[2]

					login_info_data_dict['username'] =line[1]
					login_info_data_dict['password']  =line[3]
					login_info_data_dict['user_type']=line[4]
					login_info_data_dict['status']=line[5]



					login_info_data_db.append(login_info_data_dict)

			if(password==login_info_data[0][3]):
				resp = Response(json.dumps({"success": 1, "configure_data":login_info_data[0], "datasets":login_info_data_db}))
			else:
				resp = Response(json.dumps({"success": 0}))




		else:
			resp = Response(json.dumps({"success": 2}))


		resp.headers['Content-type']='application/json'
		return after_request(resp)


# Report section

@app.route('/api/get/registration/report/',methods=['GET','POST'])
def APiGetRegistrationReport():
	if request.method=='POST':
		user_data = dbhelper.GetData().getUserDetails()
		dateNow = str(datetime.now())
		now = datetime.today()
		workingDays = now.strftime('%d/%m/%Y')
		date_format = "%d/%m/%Y"
		user_data_db=[]

		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['name']  = line[1]
				user_data_dict['email']  = line[2]
				user_data_dict['mobile'] = line[3]
				user_data_dict['alternateNo']  = line[4]
				try:
					user_data_dict['parentName']  = str(line[5]).encode('utf-8').strip()
				except:
					user_data_dict['parentName']  =''
				# user_data_dict['parentName']  = line[5]
				user_data_dict['domicile_document']  = line[6]
				user_data_dict['dob']  = line[8]
				try:
					a = datetime.strptime(line[8], date_format)
				except:
					a=datetime.strptime(workingDays, date_format)

				b = datetime.strptime(workingDays, date_format)
				delta = b - a
				saurabh=round(delta.days/365.25)
				try:
					user_data_dict['age']  = str(saurabh)+'years'
				except:
					user_data_dict['age']  =''

				user_data_dict['gender']  = line[9]
				user_data_dict['category']  = line[10]
				user_data_dict['higher_education']  = line[15]
				user_data_dict['course'] = line[16]
				user_data_dict['passing_year']  = line[17]
				user_data_dict['pQualification']  = line[18]
				user_data_dict['pCourse'] = line[19]
				user_data_dict['pPassingYear']  = line[20]
				user_data_dict['skillsets']  = line[21]
				user_data_dict['work_outside'] = line[22]
				user_data_dict['construction'] = line[30]
				user_data_dict['education'] = line[31]
				user_data_dict['banking']  = line[32]
				user_data_dict['others']  = line[33]
				user_data_dict['createdDate']= datetime.strptime(line[94], "%Y-%m-%d %H:%M").strftime("%d/%m/%Y")

				try:
					user_data_dict['address'] = str(line[34]).decode('utf8').encode('utf8')
				except:
					user_data_dict['address'] = ''

				try:
					user_data_dict['houseNo'] = str(line[35]).encode('utf-8').strip()
				except:
					user_data_dict['houseNo'] =''
				try:
					user_data_dict['villageName']  = str(line[36]).encode('utf-8').strip()
				except:
					user_data_dict['villageName']  =''


				user_data_dict['city']  = str(line[37]).encode('utf-8').strip()
				user_data_dict['state'] = str(line[38]).encode('utf-8').strip()
				user_data_dict['pincode']  = line[39]
				user_data_dict['registrationId']  = line[40]
				user_data_dict['maritalStatus'] = line[41]
				user_data_dict['disability']  = line[42]
				user_data_dict['profile_image']  = line[43]
				user_data_dict['training']= str(line[59]).encode('utf-8').strip()
				try:
					user_data_dict['trainingType']= str(line[60]).encode('utf-8').strip()
				except:
					user_data_dict['trainingType']= ''

				user_data_dict['specialization']= str(line[61]).encode('utf-8').strip()
				user_data_dict['trainingDate']= str(line[62]).encode('utf-8').strip()
				user_data_dict['trainingDuration']= str(line[63]).encode('utf-8').strip()
				user_data_dict['completionDate']= str(line[64]).encode('utf-8').strip()
				user_data_dict['employed']= str(line[65]).encode('utf-8').strip()
				user_data_dict['work_experience']= str(line[66]).encode('utf-8').strip()
				user_data_dict['employment_prefer']= str(line[67]).encode('utf-8').strip()
				user_data_dict['short_training']= str(line[68]).encode('utf-8').strip()
				user_data_dict['notice_period']= str(line[69]).encode('utf-8').strip()
				user_data_dict['status']= str(line[70]).encode('utf-8').strip()
				try:
					user_data_dict['pAddress1']= str(line[71]).encode('utf-8').strip()
				except:
					user_data_dict['pAddress1']=''

				try:
					user_data_dict['pAddress2']=str(line[72]).encode('utf-8').strip()
				except:
					user_data_dict['pAddress2']=''

				try:
					user_data_dict['pVillage']= str(line[73]).encode('utf-8').strip()
				except:
					user_data_dict['pVillage']= ''

				user_data_dict['pState']= str(line[74]).encode('utf-8').strip()
				user_data_dict['pCity']= str(line[75]).encode('utf-8').strip()
				user_data_dict['pPincode']= line[76]
				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


# selection report
@app.route('/api/get/selection/report/',methods=['GET','POST'])
def APiGetSelectionReport():
	if request.method=='POST':
		user_data = dbhelper.GetData().getUserSelection()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['name']  = line[0]
				user_data_dict['email']  = line[1]
				user_data_dict['mobile']  = line[2]
				user_data_dict['company1'] = line[3]
				user_data_dict['company2']  = line[4]
				user_data_dict['company3']  = line[5]
				user_data_dict['company4']  = line[6]
				user_data_dict['response1'] = line[7]
				user_data_dict['response2']  = line[8]
				user_data_dict['response3']  = line[9]
				user_data_dict['response4']  = line[10]

				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/api/get/youth/analysis/',methods=['GET','POST'])
def APiGetAnalysisReport():
	if request.method=='POST':
		user_data = dbhelper.GetData().getUserAnalysis()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['total']  = line[0]
				user_data_dict['selected']  = line[1]
				user_data_dict['male']  = line[2]
				user_data_dict['female'] = line[3]
				user_data_dict['tweleth']  = line[4]
				user_data_dict['graduation']  = line[5]
				user_data_dict['postgraduation']  = line[6]
				user_data_dict['tenth'] = line[7]
				user_data_dict['below'] = 0
				user_data_dict['MaleSelected']  = line[8]
				user_data_dict['FemaleSelected'] = line[9]
				user_data_dict['FemalePostGraduation']  = line[10]
				user_data_dict['MalePostGraduation'] = line[11]
				user_data_dict['MaleGraduation']  = line[12]
				user_data_dict['FemaleGraduation']  = line[13]
				user_data_dict['Female12'] = line[14]
				user_data_dict['Male12'] = line[15]
				user_data_dict['Total12'] = line[16]
				user_data_dict['Female10'] = line[17]
				user_data_dict['Male10'] = line[18]
				user_data_dict['Total10'] = line[19]
				user_data_dict['YetToInterview']  = 350
				user_data_dict['YetToInterviewFemale'] = 145
				user_data_dict['YetToInterviewMale']  = 205
				user_data_dict['InterviewNotSelected'] = 690
				user_data_dict['InterviewNotSelectedMale'] = 390
				user_data_dict['InterviewNotSelectedFemale'] = 300


				user_data_db.append(user_data_dict)

		resp = Response(json.dumps({"success": True, "user_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/youth/city/',methods=['GET','POST'])
def APiGetCity():
	if request.method=='POST':
		city_data = dbhelper.GetData().getCompanyCity()
		city_data_db=[]
		if(len(city_data))>0:
			for line in city_data:
				city_data_dict={}
				city_data_dict['city']  = line[0]

				city_data_db.append(city_data_dict)

		resp = Response(json.dumps({"success": True, "city_data": city_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/youth/company/',methods=['GET','POST'])
def APiGetCompany():
	if request.method=='POST':
		company_data = dbhelper.GetData().getYouthCompany()
		company_data_db=[]
		if(len(company_data))>0:
			for line in company_data:
				company_data_dict={}
				company_data_dict['companyName']  = line[0]
				company_data_db.append(company_data_dict)

		resp = Response(json.dumps({"success": True, "company_data": company_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/city/company/',methods=['GET','POST'])
def APiGetCityCompany():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		city = configure_data['city']
		total_data = dbhelper.GetData().gettotalCompany(city)
		company_data = dbhelper.GetData().getcityCompany(city)
		company_data_db=[]
		if(len(company_data))>0:
			for line in company_data:
				company_data_dict={}
				company_data_dict['totalCandidate']  = line[0]
				company_data_dict['companyName']  = line[1]

				company_data_db.append(company_data_dict)

		resp = Response(json.dumps({"success": True, "company_data": company_data_db,"total_candidate": total_data }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/company/city/',methods=['GET','POST'])
def APiGetCompanyCity():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		company = configure_data['company']
		company_data = dbhelper.GetData().getCompanyCity2(company)
		total_data = dbhelper.GetData().getTotalCand(company)[0][0]
		company_data_db=[]
		if(len(company_data))>0:
			for line in company_data:
				company_data_dict={}
				company_data_dict['totalCandidate']  = line[0]
				company_data_dict['city']  = line[1]

				company_data_db.append(company_data_dict)

		resp = Response(json.dumps({"success": True, "city_data": company_data_db, "total_candidate": total_data}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/company/details/',methods=['GET','POST'])
def APiGetCompanyDetails():
	if request.method=='POST':
		total_data = dbhelper.GetData().getCompanyName()
		company_data_db=[]
		if(len(total_data))>0:
			for line in total_data:
				company_data_dict={}
				company_data_dict['id']  = line[0]
				company_data_dict['companyName']  = line[1]
				company_data_dict['vacancy']=line[2]


				company_data_db.append(company_data_dict)

		resp = Response(json.dumps({"success": True, "company_data": company_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/api/get/block/list/',methods=['GET','POST'])
def APiGetBlockList():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		district = configure_data['district']
		district_data = dbhelper.GetData().getblockList(district)
		district_data_db=[]
		if(len(district_data))>0:
			for line in district_data:
				district_data_dict={}
				district_data_dict['block']  = str(line[0]).encode('utf-8').strip()

				district_data_db.append(district_data_dict)

		resp = Response(json.dumps({"success": True, "block_data": district_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/api/candidate/check/auth/', methods=['GET','POST'])
def CheckCustomerAuth():
	if request.method       == 'POST':
		user_data =json.loads(request.data)
		mobile= user_data['mobile']
		otp= user_data['otp']
		AddCustomer= dbhelper.GetData().getUserLogin(mobile)
		if len(AddCustomer)==0:
			db={'message':'User Not Exist',"confirmation":0}
			# text="Your+OTP+is+:+%s+Note+:+Please+ DO+NOT+SHARE+this+OTP+with+anyone."%(str(otp))
			text ="Your+OTP+ %s+for+MYN+Registration."%(str(otp))
			mobile="91"+str(mobile)
			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})
		else:
			db={'message': 'User Already Exist', "confirmation":1}


		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)


@app.route('/api/user/sos/call/', methods=['GET','POST'])
def SOSCall():
	if request.method       == 'POST':
		user_data =json.loads(request.data)
		mobile= user_data['mobile']
		name= user_data['name']
		address = user_data['address']
		admin_data = dbhelper.GetData().getadminMobile()
		if(len(admin_data))>0:
			for line in admin_data:
				admin_data_dict={}
				admin_data_dict['mobile']  = line[0]

				text =" Hi+I+am+%s+,+I+have+some+kind+of+stress+or+trouble+.+Please+contact+me+asap+on+:+%s+Location+:+ %s."%(str(name),str(mobile),str(address))
				url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(line[0]),text)
				urlfetch.set_default_fetch_deadline(45)
				resp = urlfetch.fetch(url=url,
					method=urlfetch.GET,
					headers={'Content-Type': 'text/html'})

		resp = Response(json.dumps({ "response": "success"}))
		return after_request(resp)

@app.route('/api/attendance/off/',methods=['GET','POST'])
def ApiAddAttendanceoff():
	if request.method=='POST':

		attendance_data         = json.loads(request.data)
		print attendance_data
		username                 = attendance_data['username']
		date                    = attendance_data['date']
		reportInTime            = attendance_data['reportInTime']
		try:
			reportInAddress         = attendance_data['reportInAddress']
		except:
			reportInAddress =""

		inAddrInGeoFans         = attendance_data['inAddrInGeoFans']
		status                  = "3"
		createdAt               = str(datetime.now())
		attendanceStatus      ="Off"
		AddTodayAttendance = dbhelper.AddData().AddAttendance(username,date,reportInTime,reportInAddress,inAddrInGeoFans,status,createdAt,attendanceStatus)
		print AddTodayAttendance
		if AddTodayAttendance==0:
			d={"confirmation":0}
		else:
			d={"confirmation":1}

		resp = Response(json.dumps({"success": True, "datasets":d}))
		return after_request(resp)

# @app.route('/api/get/attendance/summary/',methods=['POST'])
# def APigetSummaryList():
#   if request.method=='POST':
#       strDate = str(date.today())
#       dateNow  = datetime.strptime(strDate, "%Y-%m-%d").strftime("%m/%d/%Y")
#       emp_data = dbhelper.GetData().getAttendanceSummary(dateNow)
#       present= emp_data[0][0]
#       total = emp_data[0][1]
#       absent = total-present
#       emp_data_db=[]
#       if(len(emp_data))>0:
#           for line in emp_data:
#               emp_data_dict={}
#               emp_data_dict['present'] = line[0]
#               emp_data_dict['total']  = line[1]
#               emp_data_dict['absent']  = absent
#               emp_data_db.append(emp_data_dict)

#       resp = Response(json.dumps({"success": 1, "configure_data": emp_data_db }))
#       resp.headers['Content-type']='application/json'
#       return after_request(resp)

@app.route('/api/get/complain/details/',methods=['GET','POST'])
def APiGetComplain():
	if request.method=='POST':
		complain_data = dbhelper.GetData().getcomplain()
		complain_data_db=[]
		if(len(complain_data))>0:
			for line in complain_data:
				complain_data_dict={}
				complain_data_dict['id']  = line[0]
				complain_data_dict['category']  = line[1]
				# complain_data_dict['sub_category']=line[2]


				complain_data_db.append(complain_data_dict)

		resp = Response(json.dumps({"success": True, "complain_data": complain_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/complain/list/',methods=['GET','POST'])
def APicomplainList():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		Id = configure_data['id']
		complain_data = dbhelper.GetData().getcomplainList(Id)
		complain_data_db=[]
		if(len(complain_data))>0:
			for line in complain_data:
				complain_data_dict={}
				complain_data_dict['id']  = line[0]

				complain_data_dict['sub_category']  = line[1]

				complain_data_db.append(complain_data_dict)

		resp = Response(json.dumps({"success": True, "complain_data": complain_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/api/add/user/complain/',methods=['GET','POST'])
def APiAddcomplain():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile  = userInfo['mobile']
		category= userInfo['category']
		subcategory = userInfo['subcategory']
		complain= userInfo['complain']
		name= userInfo['name']
		lastId           =dbhelper.GetData().getComplainID()[0][0]
		if lastId:
			newid=str(123+lastId)
		else:
			newid=str(123)
		complainId = 'CRN'  + newid

		AddComplain = dbhelper.AddData().AddComplain(mobile,category,subcategory,complain,name,complainId)
		db={"success": True,'message':'Complain Added',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/api/add/admin/reply/',methods=['GET','POST'])
def APiAddReply():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		complainId = userInfo['complainId']
		reply = userInfo['reply']
		EditCompany = dbhelper.UpdateData().UpdateReply(complainId,reply)

		# AddComplain = dbhelper.AddData().AddComplain(mobile,category,subcategory,complain,name,complainId)
		db={"success": True,'message':'Complain Added',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)



@app.route('/api/add/cand/company/response/',methods=['GET','POST'])
def APiAddCandResponse():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		mobile = userInfo['mobile']
		company = userInfo['company']
		status = userInfo['status']
		EditCompany = dbhelper.UpdateData().UpdateStuRes(mobile,company,status)

		AddComplain = dbhelper.AddData().AddStuResponse(mobile,company,status)
		db={"success": True,'message':'Complain Added',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/api/get/complain/status/list/',methods=['GET','POST'])
def APicomplainListStatus():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		mobile = configure_data['mobile']
		complain_data = dbhelper.GetData().getcomplainListData(mobile)
		complain_data_db=[]
		if(len(complain_data))>0:
			for line in complain_data:
				complain_data_dict={}
				complain_data_dict['id']  = line[0]
				complain_data_dict['mobile']  = line[1]
				complain_data_dict['subcategory']  = line[2]
				complain_data_dict['complain']  = line[3]
				complain_data_dict['name']  = line[4]
				complain_data_dict['category']  = line[5]
				complain_data_dict['status']  = line[6]
				complain_data_dict['complainId']  = line[7]
				complain_data_dict['reply']  = line[8]

				complain_data_db.append(complain_data_dict)

		resp = Response(json.dumps({"success": True, "complain_data": complain_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/api/get/complain/admin/list/',methods=['GET','POST'])
def APicomplainAdminListStatus():
	if request.method=='POST':
		complain_data = dbhelper.GetData().getcomplainListAdmin()
		complain_data_db=[]
		if(len(complain_data))>0:
			for line in complain_data:
				complain_data_dict={}
				complain_data_dict['id']  = line[0]
				complain_data_dict['mobile']  = line[1]
				complain_data_dict['subcategory']  = line[2]
				complain_data_dict['complain']  = line[3]
				complain_data_dict['name']  = line[4]
				complain_data_dict['category']  = line[5]
				complain_data_dict['status']  = line[6]
				complain_data_dict['complainId']  = line[7]
				complain_data_dict['reply']  = line[8]

				complain_data_db.append(complain_data_dict)

		resp = Response(json.dumps({"success": True, "complain_data": complain_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)



# enternuship


@app.route('/api/add/enterunship/',methods=['GET','POST'])
def APiaddenterunship():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		name= userInfo['name']
		email = userInfo['email']
		mobile = userInfo['mobile']
		alternateNo= userInfo['alternateNo']
		parentName      = userInfo['parentName']
		otp      = userInfo['otp']
		user_status =dbhelper.GetData().getEnterunshipStatus(mobile)
		print user_status
		if user_status==True:
			db={'message':'User Already Exist',"confirmation":0}
			resp = Response(json.dumps({"response": db}))
			return after_request(resp)
		else:
			AddUser = dbhelper.AddData().addEnterunship(name,email,mobile,alternateNo,parentName)

			db={'message':'User Added',"confirmation":1,"mobile":mobile,"name":name,"email":email,"otp":otp}

			text ="User+has+been+registered+successfully.Your+Login+OTP+is+ %s."%(str(otp))

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			print url
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})
			respp = Response(json.dumps({"response": db}))
			return after_request(respp)


@app.route('/api/enterunship/login/', methods=['GET','POST'])
def ApienterunshipLogin():
	if request.method  == 'POST':
		user_data =json.loads(request.data)
		mobile = user_data['mobile']
		otp  = user_data['otp']

		User= dbhelper.GetData().getenterunshipLogin(mobile)

		if len(User)>0:

			name = User[0][0]
			email = User[0][1]

			mobile=User[0][2]
			alternateNo=User[0][3]
			parentName = User[0][4]
			status= 1
			try:
				image_url=User[0][6]
			except:
				image_url=''

			if User[0][7] is None:

				registrationId=""
			else:
				registrationId=User[0][7]

			if User[0][6] is None:
				image_url=""
			else:
				image_url=image_url

			userType='enterunship'



			text =" Welcome+to+IPE+GLOBAL. Your+Login+OTP+is+ %s."%(str(otp))

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)
			print url
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})



			db={'message':'User Exist',"confirmation":1,"name":name,"mobile":mobile,"status":status,"otp":otp, "email":email,"image_url":image_url,"registrationId":registrationId,"userType":userType}
			print db
		else:
			db={'message': 'User Not Exist', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)


@app.route('/api/add/enterunship/data/',methods=['GET','POST'])
def APiAddenternsDataNew():
	if request.method=='POST':
		userInfo   = json.loads(request.data)
		print userInfo
		mobile=userInfo['mobile']
		imageName=userInfo['imageName']
		enterpriseNature=userInfo['enterpriseNature']
		ventureName=userInfo['ventureName']
		relevantExperience=userInfo['relevantExperience']
		industry=userInfo['industry']
		ethnicity=userInfo['ethnicity']
		martialStatus=userInfo['martialStatus']
		dob=userInfo['dob']
		category=userInfo['category']
		disability=userInfo['disability']
		disabilityNature=userInfo['disabilityNature']
		houseNo=userInfo['houseNo']
		streetName=userInfo['streetName']
		locality=userInfo['locality']
		village=userInfo['village']
		block=userInfo['block']
		district=userInfo['district']
		state=userInfo['state']
		pin=userInfo['pin']
		try:
			language=userInfo['language']
		except:
			language=''
		aadharNo=userInfo['aadharNo']
		acedamicQualification=userInfo['acedamicQualification']
		professionalQualification=userInfo['professionalQualification']
		specailization=userInfo['specailization']
		ongoingCourse=userInfo['ongoingCourse']
		relevantCertification=userInfo['relevantCertification']
		training=userInfo['training']
		trainingType=userInfo['trainingType']
		subject=userInfo['subject']
		trainingDuration=userInfo['trainingDuration']
		instituteName=userInfo['instituteName']
		computerSkill=userInfo['computerSkill']
		currentOccupation=userInfo['currentOccupation']
		currentCompany=userInfo['currentCompany']
		employedSince=userInfo['employedSince']
		workPlace=userInfo['workPlace']
		monthlyIncome=userInfo['monthlyIncome']
		selfEmployment=userInfo['selfEmployment']
		startedSince=userInfo['startedSince']
		placeOfself=userInfo['placeOfself']
		monthlyEarning=userInfo['monthlyEarning']
		readyPurposal=userInfo['readyPurposal']
		readyPlan=userInfo['readyPlan']
		bussinessPlan=userInfo['bussinessPlan']
		profitabilityPlan=userInfo['profitabilityPlan']
		identifya=userInfo['identifya']
		identifyb=userInfo['identifyb']
		identifyc=userInfo['identifyc']
		identifyd=userInfo['identifyd']
		marketPlan=userInfo['marketPlan']
		developingPlan=userInfo['developingPlan']
		marketingPlana=userInfo['marketingPlana']
		marketingPlanb=userInfo['marketingPlanb']
		marketingPlanc=userInfo['marketingPlanc']
		marketingPland=userInfo['marketingPland']
		procurementPlan=userInfo['procurementPlan']
		supportProcurement=userInfo['supportProcurement']
		identityChallenge1=userInfo['identityChallenge1']
		identityChallenge2=userInfo['identityChallenge2']
		identityChallenge3=userInfo['identityChallenge3']
		identityChallenge4=userInfo['identityChallenge4']
		financialPlan=userInfo['financialPlan']
		sourceFinance=userInfo['sourceFinance']
		securingFinace=userInfo['securingFinace']
		identitySecure1=userInfo['identitySecure1']
		identitySecure2=userInfo['identitySecure2']
		identitySecure3=userInfo['identitySecure3']
		venture=userInfo['venture']
		additionalInformation=userInfo['additionalInformation']
		registartionCode=userInfo['registartionCode']
		gender=userInfo['gender']
		khasi=userInfo['khasi']
		garo=userInfo['garo']
		english=userInfo['english']
		hindi=userInfo['hindi']
		others=userInfo['others']
		venture1=userInfo['venture1']
		venture2=userInfo['venture2']
		venture3=userInfo['venture3']
		venture4=userInfo['venture4']
		venture5=userInfo['venture5']
		venture6=userInfo['venture6']
		venture7=userInfo['venture7']
		venture8=userInfo['venture8']
		venture9=userInfo['venture9']




		status  = 1
		registration_status =dbhelper.GetData().getRegistrationEnter(mobile)
		print registration_status

		if len(registration_status)>0 and  registration_status[0][0] is not None:

			registartionCode=registration_status[0][0]
			db= {'message':'Already Registered',"confirmation":2, "registration_code":registartionCode}

		else:
			lastId           =dbhelper.GetData().getLastEnter()[0][0]
			if lastId:
				newid=str(123+lastId)
			else:
				newid=str(123)


			registartionCode = 'MSOPA' + str(mobile[-4:]) + newid



			EditAssign = dbhelper.UpdateData().UpdateEnter(mobile,imageName,enterpriseNature,	ventureName,	relevantExperience,	industry,	ethnicity,	martialStatus,	dob,	category,	disability,	disabilityNature,	houseNo,	streetName,	locality,	village,	block,	district,	state,	pin,	language,	aadharNo,	acedamicQualification,	professionalQualification,	specailization,	ongoingCourse,	relevantCertification,	training,	trainingType,	subject,	trainingDuration,	instituteName,	computerSkill,	currentOccupation,	currentCompany,	employedSince,	workPlace,	monthlyIncome,	selfEmployment,	startedSince,	placeOfself,	monthlyEarning,	readyPurposal,	readyPlan,	bussinessPlan,	profitabilityPlan,	identifya,	identifyb,	identifyc,	identifyd,	marketPlan,	developingPlan,	marketingPlana,	marketingPlanb,	marketingPlanc,	marketingPland,	procurementPlan,	supportProcurement,	identityChallenge1,	identityChallenge2,	identityChallenge3,	identityChallenge4,	financialPlan,	sourceFinance,	securingFinace,	identitySecure1,	identitySecure2,	identitySecure3,	venture,	additionalInformation,	registartionCode,gender,khasi,garo,english,hindi,others, venture1, venture2, venture3, venture4, venture5, venture6, venture7, venture8, venture9)
			db={'message':'UserDataUpdate',"confirmation":1, "registration_code": registartionCode}
			text="Congratulations+!+Your+Form+has+been+Submitted+Succesfully.Your+Registration+No+is '%s'"%(registartionCode)

			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=LKINMB&mobile=%s&msg=%s'%(str(mobile),text)

			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})




		resp = Response(json.dumps({"response": db}))
		return after_request(resp)



@app.route('/api/get/youth/summary/list/',methods=['GET','POST'])
def APiYouthSummary():
	if request.method=='POST':
		youth_data = dbhelper.GetData().getYouthSummaryData()
		youth_data_db=[]
		if(len(youth_data))>0:
			for line in youth_data:
				youth_data_dict={}
				youth_data_dict['registered']  = line[0]
				youth_data_dict['male']  = line[1]
				youth_data_dict['female']  = line[2]
				youth_data_dict['disable']  = line[3]
				
				youth_data_db.append(youth_data_dict)

		resp = Response(json.dumps({"success": True, "youth_data": youth_data_db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


	
