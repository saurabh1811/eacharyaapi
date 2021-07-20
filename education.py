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
import educationcloudDbHandler as dbhelper
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



# registration
@app.route('/education/class/elearningstudent/',methods=['GET','POST'])
def educationaddelearningstudent():
	if request.method=='POST':
		elearning   = json.loads(request.data)
		

		mobile               = elearning['mobile']
		name                 = elearning['name']
		email                = elearning['email']
		invite_code          = elearning['invite_code']
		try:
			otp = "1234"
		except:
			otp="1234"

		UserStatus  = dbhelper.GetData().getCandidateAuthStatus(mobile)

		if UserStatus==True:
			db={'message':'User Already Exist',"confirmation":0}
		else:
			lastId             =dbhelper.GetData().getPartnerLastID()[0][0]
			if lastId:
				newid=str(123+lastId)
			else:
				newid=str(123)
			cellPhone = mobile
			referalCode = 'SERVP' + str(cellPhone[-4:]) + newid
			Adduser = dbhelper.AddData().addclasselearningstudent(mobile,name,email,invite_code,referalCode)
			db={'message':'User added',"confirmation":1}
			text =" Welcome+to+ elearning.+ Your +Login+ OTP is %s."%(str(otp))
			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=INOBIN&mobile=%s&msg=%s'%(str(mobile),text)
			print url
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})
		
				
		resp = Response(json.dumps({"success": db, "mobile":mobile,"otp":otp, "name":name, "email":email, "invite_code":invite_code}))
		return after_request(resp)








# Exam Name

@app.route('/education/get/exam/name/',methods=['POST'])
def educationexamListing():
	if request.method=='POST':
		user_data           =json.loads(request.data)
		mobile              = user_data['mobile']
		user_data = dbhelper.GetData().getexamList()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
			   
				user_data_dict['id']                = line[0]
				exam_status = dbhelper.GetData().getuserexamstatus(mobile,line[0])
				user_data_dict['exam_status']=exam_status
				user_data_dict['questionId']                = line[0]
				user_data_dict['exam_name']         = line[1]
				user_data_dict['exam_description']  = line[2]
				user_data_dict['createdAt']        = str(line[5])
				user_data_dict['duration']  = line[6]
				user_data_dict['endDate']        = str(line[7])
				user_data_dict['retake']  = line[8]
				user_data_dict['mobile']  = mobile
				
				
				
				
				user_data_db.append(user_data_dict)

				
		resp = Response(json.dumps({"success": 1, "configure_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/exam/name/new/',methods=['POST'])
def educationexamListingnew():
	if request.method=='POST':
		user_data = dbhelper.GetData().getexamList()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
			   
				user_data_dict['id']                = line[0]
				user_data_dict['questionId']                = line[0]
				user_data_dict['exam_name']         = line[1]
				user_data_dict['exam_description']  = line[2]
				user_data_dict['createdAt']        = str(line[5])
				user_data_dict['duration']  = line[6]
				user_data_dict['endDate']        = str(line[7])
				user_data_dict['retake']  = line[8]

				user_data_db.append(user_data_dict)

				
		resp = Response(json.dumps({"success": 1, "configure_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)		      






# Candidate Authentication

@app.route('/education/check/candidate/auth/', methods=['GET','POST'])
def AddCheckStatus():
	if request.method       == 'POST':
		user_data           =json.loads(request.data)
		mobile              = user_data['mobile']
		otp                 = "1234"
			
		UserStatus  = dbhelper.GetData().getCandidateAuthStatus(mobile)

		if UserStatus== True:
			user_data = dbhelper.GetData().getloginnew(mobile)
			status=user_data[0][11]
			categoryId=user_data[0][6]
			try:
				categoryName = dbhelper.GetData().getexamcategorybyid(categoryId)[0][1]
			except:
				categoryName=''

			subcategoryId=user_data[0][7]
			try:
				subCategoryName = dbhelper.GetData().getexamSubcategorybyid(subcategoryId)[0][1]
			except:
				subCategoryName=''

			name=user_data[0][2]
			email=user_data[0][3]
			imageName=user_data[0][10]
			
					
			db={'message':'User Already Exist',"confirmation":1,"status":status,"categoryId":categoryId,"subcategoryId":subcategoryId,"name":name,"email":email,"imageName":imageName,"categoryName":categoryName,"subCategoryName":subCategoryName}
			text =" Welcome+to+ elearning.+ Your +Login+ OTP + is + %s."%(str(otp))
			url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=INOBIN&mobile=%s&msg=%s'%(str(mobile),text)
			print url
			urlfetch.set_default_fetch_deadline(45)
			resp = urlfetch.fetch(url=url,
				method=urlfetch.GET,
				headers={'Content-Type': 'text/html'})

		else:
			db={'message':'User Not Exist', "confirmation":0}


		resp = Response(json.dumps({ "response": db, "mobile":mobile}))
		return after_request(resp)


	

# resend OTP



@app.route('/education/resend/otp/', methods=['GET','POST'])
def ApiResendOtp():
	if request.method  == 'POST':
		user_data =json.loads(request.data)
		mobile = user_data['mobile']
		otp  = "1234"
		print otp
		
		
		text =" Welcome+to+E-LEARNING. Your+Login+OTP+is+ %s."%(str(otp))


		url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=INOBIN&mobile=%s&msg=%s'%(str(mobile),text)
		print url
		urlfetch.set_default_fetch_deadline(45)
		resp = urlfetch.fetch(url=url,
			method=urlfetch.GET,
			headers={'Content-Type': 'text/html'})
		db={'message':'User Exist',"confirmation":1,"mobile":mobile,"otp":otp}
		
		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)





# adding fcm token

@app.route('/education/add/token/',methods=['GET','POST'])
def educationAddToken():
	if request.method=='POST':
		token_data = json.loads(request.data)
		mobile = token_data['mobile']
		fcmToken= token_data['fcmToken']
	   
		update              =dbhelper.DeleteData().deleteToken(mobile)

		last                =dbhelper.AddData().addToken(mobile,fcmToken)
		if last:
			db={'message':'Token Added',"confirmation":1}
		else:
			db={'message': 'Token not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db, "mobile":mobile,"fcmToken":fcmToken}))
		return after_request(resp)


@app.route('/education/add/student/register/',methods=['GET','POST'])
def APiaddStudentregister():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		mobile=userinfo['mobile']
		name=userinfo['name']
		email=userinfo['email']
		inviteCode=userinfo['inviteCode']
		className=userinfo['className']
		city=userinfo['city']
		school=userinfo['school']
		boardName=userinfo['boardName']
		preparingForExam=userinfo['preparingForExam']
		
		
		AddUser = dbhelper.AddData().addUserregister(mobile,name,email,inviteCode,className,city,school,boardName,preparingForExam)

		if AddUser==0:
			d={"confirmation":1}
		else:
			d={"confirmation":0}
		# db={'message':'Rating Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","mobile":mobile,"name":name,"email":email,"inviteCode":inviteCode,"className":className,"city":city,"school":school,"boardName":boardName,"preparingForExam":preparingForExam,"confirmation":d}))
		return after_request(resp)

@app.route('/education/add/student/feedback/',methods=['GET','POST'])
def APiaddStudentregister2():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		username=userinfo['username']
		url=userinfo['url']
		feedback=userinfo['feedback']
		AddUser = dbhelper.AddData().addFeedback(username,url,feedback)

		if AddUser==0:
			d={"confirmation":1}
		else:
			d={"confirmation":0}
		db={'message':'Rating Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","confirmation":d}))
		return after_request(resp)

@app.route('/education/get/student/register/',methods=['GET','POST'])
def APiGetregister():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile=userinfo['mobile']
		user_data = dbhelper.GetData().getregister(mobile)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['mobile']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['email']=line[3]
				user_data_dict['inviteCode']=line[4]
				user_data_dict['className']  = line[5]
				user_data_dict['school']=line[6]
				user_data_dict['city']=line[7]
				user_data_dict['boardName']=line[8]
				user_data_dict['preparingForExam']=line[9]
				user_data_dict['imageName']=line[10]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/add/contact/us/',methods=['GET','POST'])
def APiaddusercontact():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		name=userinfo['name']
		mobile=userinfo['mobile']
		email=userinfo['email']
		pinCode=userinfo['pinCode']
		feedback=userinfo['feedback']
		
		AddUser = dbhelper.AddData().addUsercontact(name,mobile,email,pinCode,feedback)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)

# @app.route('/education/add/previous/paper/',methods=['GET','POST'])
# def APiadduserpreviousPaper():
# 	if request.method=='POST':
# 		userinfo   = json.loads(request.data)
		
		
# 		imageUrl=userinfo['imageUrl']
# 		examName=userinfo['examName']
# 		noOfSeat=userinfo['noOfSeat']
# 		noOfQuestion=userinfo['noOfQuestion']
# 		marks=userinfo['marks']
# 		subjectList=userinfo['subjectList']
		
# 		AddUser = dbhelper.AddData().addUserpreviousPaper(imageUrl,examName,noOfSeat,noOfQuestion,marks,subjectList)
# 		db={'message':'User Added',"confirmation":1}
		
# 		resp = Response(json.dumps({"response":"success","imageUrl":imageUrl,"examName":examName,"noOfSeat":noOfSeat,"noOfQuestion":noOfQuestion,"marks":marks,"subjectList":subjectList}))
# 		return after_request(resp)

@app.route('/education/get/previous/paper/',methods=['GET','POST'])
def APiGetexampreviousPaper():
	if request.method=='POST':
		# userinfo   = json.loads(request.data)
		user_data = dbhelper.GetData().getexampreviousPaper()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['imageUrl']=line[1]
				user_data_dict['examName']=line[2]
				user_data_dict['noOfSeat']=line[3]
				user_data_dict['noOfQuestion']=line[4]
				user_data_dict['mark']  = line[5]
				user_data_dict['subjectList']=line[6]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/add/test/series/',methods=['GET','POST'])
def APiaddusertestseries():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		imageUrl=userinfo['imageUrl'].replace(" ","_")
		examName=userinfo['examName']
		noOfSeat=userinfo['noOfSeat']
		noOfQuestion=userinfo['noOfQuestion']
		marks=userinfo['marks']
		subjectList=userinfo['subjectList']
		
		
		AddUser = dbhelper.AddData().addUsertestseries(imageUrl,examName,noOfSeat,noOfQuestion,marks,subjectList)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","imageUrl":imageUrl,"examName":examName,"noOfSeat":noOfSeat,"noOfQuestion":noOfQuestion,"marks":marks,"subjectList":subjectList}))
		return after_request(resp)

@app.route('/education/get/test/series/',methods=['GET','POST'])
def APiGettestseries():
	if request.method=='POST':
		# userinfo   = json.loads(request.data)
		user_data = dbhelper.GetData().getexamtestseries()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['imageUrl']=line[1]
				user_data_dict['examName']=line[2]
				user_data_dict['noOfSeat']=line[3]
				user_data_dict['noOfQuestion']=line[4]
				user_data_dict['mark']  = line[5]
				user_data_dict['subjectList']=line[6]
				user_data_dict['status']=line[8]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/update/test/series/',methods=['GET','POST'])
def APiUserupdateseries():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		imageUrl=userinfo['imageUrl'].replace(" ","_")
		examName=userinfo['examName']
		noOfSeat=userinfo['noOfSeat']
		noOfQuestion=userinfo['noOfQuestion']
		marks=userinfo['marks']
		subjectList=userinfo['subjectList']

		
		EditAssign = dbhelper.UpdateData().Updateusertest(Id,imageUrl,examName,noOfSeat,noOfQuestion,marks,subjectList)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/delete/test/series/',methods=['GET','POST'])
def ApiAddtest():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().Deletetest(Id)

		if update:
			db={'message':'exam deleted',"confirmation":1}
		else:
			db={'message': 'exam not deleted', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

@app.route('/education/active/test/series/',methods=['GET','POST'])
def APiactiveupdatetest():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		
		EditAssign = dbhelper.UpdateData().Updateactivetest(Id)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/deactive/test/series/',methods=['GET','POST'])
def APideactiveupdateseries():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		
		EditAssign = dbhelper.UpdateData().Updatedeactiveseries(Id)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)						


@app.route('/education/active/live/classes/',methods=['GET','POST'])
def APiactiveupdate():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		
		EditAssign = dbhelper.UpdateData().UpdateactiveClass(Id)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/deactive/live/classes/',methods=['GET','POST'])
def APideactiveupdate():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		
		EditAssign = dbhelper.UpdateData().UpdatedeactiveClass(Id)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)		


@app.route('/education/add/question/list/',methods=['GET','POST'])
def APiaddquestionlist():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		question=userinfo['question']
		optionA=userinfo['optionA']
		optionB=userinfo['optionB']
		optionC=userinfo['optionC']
		optionD=userinfo['optionD']
		correctAns=userinfo['correctAns']
		try:
			imageUrl=userinfo['imageUrl'].replace(" ","_")
		except:
			imageUrl=""
		examId=userinfo['examId']
		description=userinfo['description']
		marks=userinfo['marks']
		negativeMarks=userinfo['negativeMarks']
		
		AddUser = dbhelper.AddData().addUserquestionlist(question,optionA,optionB,optionC,optionD,correctAns,imageUrl,examId,description,marks,negativeMarks)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","question":question,"optionA":optionA,"optionB":optionB,"optionC":optionC,"optionD":optionD,"correctAns":correctAns,"imageUrl":imageUrl}))
		return after_request(resp)


@app.route('/education/add/question/excel/data/',methods=['GET','POST'])
def APiHawellData():
	if request.method=='POST':

		hawell_data= json.loads(request.data)
		print '***',hawell_data
		hawell_data2=hawell_data['serv_data']
		email=hawell_data['email']
		examId = hawell_data['examId']




		for list2 in hawell_data2[1:]:
			question = list2[1]
			optionA	 = list2[2]
			optionB = list2[3]
			optionC = list2[4]
			optionD = list2[5]
			correctAns = list2[6]
			description	 = list2[7]
			marks	 = list2[8]
			negativeMarks	 = list2[9]
			createdBy = email
			examId	= examId
			

			AddBooking = dbhelper.AddData().addUserquestionExcel(question,optionA,optionB,optionC,optionD,correctAns,description,createdBy,examId,marks,negativeMarks)
			
		resp = Response(json.dumps({"success": True}))
		return after_request(resp)

@app.route('/education/get/question/exam/',methods=['GET','POST'])
def APiGetquestionExam():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		examId= userinfo['examId']
		user_data = dbhelper.GetData().getquestionExam(examId)
		user_data_db=[]
		if(len(user_data))>0:
			count=0
			for line in user_data:
				count=count+1
				user_data_dict={}
				user_data_dict['id']  = count
				user_data_dict['questionId']  = line[0]
				user_data_dict['question']=line[1]
				user_data_dict['optionA']=line[2]
				user_data_dict['optionB']=line[3]
				user_data_dict['optionC']=line[4]
				user_data_dict['optionD']=line[5]
				user_data_dict['correctAns']  = line[6]
				user_data_dict['setNo']=line[7]
				user_data_dict['description']=line[9]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/student/doubt/',methods=['GET','POST'])
def APiGetStudentDoubt():
	if request.method=='POST':
		user_data = dbhelper.GetData().getstudentDoubt()
		user_data_db=[]
		if(len(user_data))>0:
			count=0
			for line in user_data:
				count=count+1
				user_data_dict={}
				user_data_dict['mobile']  = line[0]
				user_data_dict['name']  = line[1]
				user_data_dict['email']=line[2]
				lastmessage = dbhelper.GetData().getlastmessage(line[0])
				user_data_dict['createdAt']=str(line[3])
				user_data_dict['message']=lastmessage[0][1]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "doubt_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/question/list/',methods=['GET','POST'])
def APiGetquestionlist():
	if request.method=='POST':
		# userinfo   = json.loads(request.data)
		user_data = dbhelper.GetData().getquestionlist()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['questionId']  = line[0]
				user_data_dict['question']=line[1]
				user_data_dict['optionA']=line[2]
				user_data_dict['optionB']=line[3]
				user_data_dict['optionC']=line[4]
				user_data_dict['optionD']=line[5]
				user_data_dict['correctAns']  = line[6]
				user_data_dict['setNo']=line[7]
				user_data_dict['imageUrl']=line[8]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/add/bookmark/question/',methods=['GET','POST'])
def APiaddquestionbookmark():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		question=userinfo['question']
		optionA=userinfo['optionA']
		optionB=userinfo['optionB']
		optionC=userinfo['optionC']
		optionD=userinfo['optionD']
		correctAns=userinfo['correctAns']
		setNo=userinfo['setNo']
		mobile=userinfo['mobile']
		
		AddUser = dbhelper.AddData().addUserquestionbookmark(question,optionA,optionB,optionC,optionD,correctAns,setNo,mobile)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","question":question,"optionA":optionA,"optionB":optionB,"optionC":optionC,"optionD":optionD,"correctAns":correctAns,"setNo":setNo,"mobile":mobile}))
		return after_request(resp)

@app.route('/education/get/bookmark/question/',methods=['GET','POST'])
def APiGetquestionbookmark():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile=userinfo['mobile']
		user_data = dbhelper.GetData().getquestionbookmark(mobile)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['question']=line[1]
				user_data_dict['optionA']=line[2]
				user_data_dict['optionB']=line[3]
				user_data_dict['optionC']=line[4]
				user_data_dict['optionD']=line[5]
				user_data_dict['correctAns']  = line[6]
				user_data_dict['setNo']=line[7]
				user_data_dict['mobile']=line[8]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/add/file/upload/',methods=['GET','POST'])
def apiMtrackFileUpload():
	if request.method=='POST':
		file_object = request.files['file']
		
		BUCKET_NAME = 'smart-howl-286211.appspot.com'
		storage = googleapiclient.discovery.build('storage', 'v1')
		
		print '**',file_object, type(file_object)
		GCS_UPLOAD_FOLDER = 'courseimage' 
		
		filename = file_object.filename.replace(" ","_")
		file_object.filename=file_object.filename.replace(" ","_")
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



@app.route('/education/add/bookmark/live/',methods=['GET','POST'])
def APiaddlivebookmark():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		bookmarkType=userinfo['bookmarkType']
		name=userinfo['name']
		url=userinfo['url']
		username=userinfo['username']
		videoId=userinfo['videoId']
		status=1
		
		AddUser = dbhelper.AddData().addUserlivebookmark(bookmarkType,name,url,username,status,videoId)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","bookmarkType":bookmarkType,"name":name,"url":url,"username":username,"videoId":videoId,"status":1}))
		return after_request(resp)

@app.route('/education/get/bookmark/live/',methods=['GET','POST'])
def APiGetlivebookmark():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		username=userinfo['username']
		user_data = dbhelper.GetData().getbookmarklive(username)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['bookmarkType']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['url']=line[3]
				user_data_dict['username']=line[4]
				user_data_dict['status']=line[5]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)	

@app.route('/education/teacher/post/login/',methods=['GET','POST'])
def ApiTeacherLogin():
	if request.method=='POST':
		print 'data', request.data
		configure_data = json.loads(request.data)
		email = configure_data['json_data']['email']
		password= configure_data['json_data']['password']
		login_info_data = dbhelper.GetData().PostTeacherLogin(email)
		login_info_data_db = []

		if(len(login_info_data))>0:
			for line in login_info_data:
				login_info_data_dict = {}
				login_info_data_dict['id']   =line[0]
				login_info_data_dict['password']  =line[1]
				login_info_data_dict['name']  =str(line[2]).upper()
				login_info_data_dict['mobile'] =line[3]
				login_info_data_dict['email'] =line[4]
				login_info_data_dict['status']=line[5]
				login_info_data_dict['subject']=line[6]
				login_info_data_dict['schoolCode']=line[7]
				  
				login_info_data_db.append(login_info_data_dict)

			if(password==login_info_data[0][1]):
				resp = Response(json.dumps({"success": 1,"configure_data":login_info_data[0], "datasets":login_info_data_db}))
			else:
				resp = Response(json.dumps({"success": 2}))

		else:
			resp = Response(json.dumps({"success": 0}))
			
		resp.headers['Content-type']='application/json'
		return after_request(resp)		


@app.route('/education/add/teacher/details/',methods=['GET','POST'])
def APiaddTeacherdetails():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		teacherName=userinfo['teacherName']
		schoolCode=userinfo['schoolCode']
		subject=userinfo['subject']
		phone_no=userinfo['phone_no']
		email=userinfo['email']
		password=userinfo['password']
		status=1
		image=userinfo['image']
		
		AddUser = dbhelper.AddData().addteacherdetails(teacherName,schoolCode,subject,phone_no,email,password,status,image)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)

@app.route('/education/get/teacher/details/',methods=['GET','POST'])
def APiGetteacherdetails():
	if request.method=='POST':
		user_data = dbhelper.GetData().getteacherdetails()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['teacherName']=line[1]
				user_data_dict['schoolCode']=line[2]
				user_data_dict['subject']=line[3]
				user_data_dict['phone_no']=line[4]
				user_data_dict['email']=line[5]
				user_data_dict['password']=line[6]
				user_data_dict['status']=line[7]
				user_data_dict['image']='https://storage.googleapis.com/courseimage/'+str(line[8])
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/teacher/profile/',methods=['GET','POST'])
def APiGetteacherProfile():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		email=userinfo['email']
		user_data = dbhelper.GetData().getteacherProfile(email)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['teacherName']=line[1]
				user_data_dict['schoolCode']=line[2]
				user_data_dict['subject']=line[3]
				user_data_dict['phone_no']=line[4]
				user_data_dict['email']=line[5]
				user_data_dict['password']=line[6]
				user_data_dict['status']=line[7]
				user_data_dict['image']='https://storage.googleapis.com/courseimage/'+str(line[8])
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/update/teacher/details/',methods=['GET','POST'])
def APiUserupdateteacher():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		teacherName=userinfo['teacherName']
		schoolCode=userinfo['schoolCode']
		subject=userinfo['subject']
		phone_no=userinfo['phone_no']
		email=userinfo['email']
		password=userinfo['password']
		image=userinfo['image']
		
		
		EditAssign = dbhelper.UpdateData().Updateteacherdetails(Id,teacherName,schoolCode,subject,phone_no,email,password,image)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/delete/teacher/Details/',methods=['GET','POST'])
def Apiremoveteacher():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['Id']
	   
		update              =dbhelper.DeleteData().DeleteRemoveteacher(Id)

		if update:
			db={'message':'Data Added',"confirmation":1}
		else:
			db={'message': 'Data not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)							

@app.route('/education/add/subject/list/',methods=['GET','POST'])
def APiaddsubjectlist():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		className=userinfo['className']
		boardName=userinfo['boardName']
		
		AddUser = dbhelper.AddData().addUsersubjectlist(className,boardName)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","className":className}))
		return after_request(resp)		

@app.route('/education/get/subject/list/',methods=['GET','POST'])
def APiGetsubjectlist():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		className=userinfo['className']
		boardName=userinfo['boardName']
		user_data = dbhelper.GetData().getsubjectlist(className,boardName)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['className']=line[1]
				user_data_dict['boardName']=line[2]
				user_data_dict['subjectName']=line[3]
				user_data_dict['noOfChapter']=line[4]
				user_data_dict['imageUrl']=line[5]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)				

@app.route('/education/add/recommended/video/',methods=['GET','POST'])
def APiaddrecommended():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		imageUrl=userinfo['imageUrl'].replace(" ","_")
		title=userinfo['title']
		date=userinfo['date']
		time=userinfo['time']
		videoUrl=userinfo['videoUrl']
		description=userinfo['description']
		subjectName=userinfo['subjectName']
		
		AddUser = dbhelper.AddData().addrecommended(imageUrl,title,date,time,videoUrl,description,subjectName)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","imageUrl":imageUrl,"title":title,"date":date,"time":time,"videoUrl":videoUrl,"description":description,"subjectName":subjectName}))
		return after_request(resp)

@app.route('/education/get/recommended/video/',methods=['GET','POST'])
def APiGetrecommended():
	if request.method=='POST':
		# userinfo   = json.loads(request.data)
		user_data = dbhelper.GetData().getrecommended()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['imageUrl']=line[1]
				user_data_dict['title']=line[2]
				user_data_dict['date']=line[3]
				user_data_dict['time']=line[4]
				user_data_dict['videoUrl']=str(line[5])+'?rel=0&amp;modestbranding=1&amp;showinfo=0'
				user_data_dict['description']  = line[6]
				user_data_dict['subjectName']=line[7]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)	


@app.route('/education/get/school/bycity/',methods=['GET','POST'])
def APiGetSchoolCity():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		city = userinfo['city']
		user_data = dbhelper.GetData().getSchoolCity(city)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['school']=line[1]
				user_data_dict['city']=line[2]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/student/profile/',methods=['GET','POST'])
def APiGetstudentprofile():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile = userinfo['mobile']
		user_data = dbhelper.GetData().getstudentprofile(mobile)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['mobile']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['class']  = line[3]
				user_data_dict['school']=line[4]
				user_data_dict['city']=line[5]
				user_data_dict['board']  = line[6]
				user_data_dict['prepairingExam']  = line[7]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/add/pricing/',methods=['GET','POST'])
def APiaddpricing():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		price=userinfo['price']
		className=userinfo['className']
		year=userinfo['year']
		
		AddUser = dbhelper.AddData().addpricing(price,className,year)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","price":price,"className":className,"year":year}))
		return after_request(resp)		

@app.route('/education/get/pricing/',methods=['GET','POST'])
def APiGetpricing():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		className=userinfo['className']
		year=userinfo['year']
		user_data = dbhelper.GetData().getpricing(className,year)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['price']=line[1]
				user_data_dict['className']=line[2]
				user_data_dict['year']=line[3]
				user_data_dict['advancePlan']=line[4]
				user_data_dict['ultimatePlan']=line[5]
				user_data_dict['masterPlan']=line[6]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/pricing/new/',methods=['GET','POST'])
def APiGetpricingnew():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		className=userinfo['className']
		user_data = dbhelper.GetData().getpricingnew(className)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['price']=line[1]
				user_data_dict['className']=line[2]
				user_data_dict['year']=line[3]
				user_data_dict['advancePlan']=line[4]
				user_data_dict['ultimatePlan']=line[5]
				user_data_dict['masterPlan']=line[6]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/pricing/simple/',methods=['GET','POST'])
def APiGetpricingsimple():
	if request.method=='POST':
		user_data = dbhelper.GetData().getpricingsimple()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['price']=line[1]
				user_data_dict['className']=line[2]
				user_data_dict['year']=line[3]
				user_data_dict['advancePlan']=line[4]
				user_data_dict['ultimatePlan']=line[5]
				user_data_dict['masterPlan']=line[6]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)				

@app.route('/education/add/login/',methods=['GET','POST'])
def APiadduserlogin():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		mobile=userinfo['mobile']
		name=userinfo['name']
		email=userinfo['email']
		inviteCode=userinfo['inviteCode']
		className=userinfo['className']
		city=userinfo['city']
		school=userinfo['school']
		boardName=userinfo['boardName']
		preparingForExam=userinfo['preparingForExam']
		
		AddUser = dbhelper.AddData().adduserlogin(mobile,name,email,inviteCode,className,city,school,boardName,preparingForExam)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","mobile":mobile,"name":name,"email":email,"inviteCode":inviteCode,"className":className,"city":city,"school":school,"boardName":boardName,"preparingForExam":preparingForExam}))
		return after_request(resp)		

@app.route('/education/get/Login/',methods=['GET','POST'])
def APiGgetlogin():
	if request.method=='POST':
		# userinfo   = json.loads(request.data)
		user_data = dbhelper.GetData().getloginnew2()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['mobile']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['email']  = line[3]
				user_data_dict['inviteCode']=line[4]
				user_data_dict['className']=line[5]
				user_data_dict['city']  = line[6]
				user_data_dict['school']  = line[7]
				user_data_dict['boardName']  = line[8]
				user_data_dict['preparingForExam']  = line[9]
				user_data_dict['imageName']  = line[10]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)		


@app.route('/education/update/login/',methods=['GET','POST'])
def APiUserupdatelogin():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		mobile=userinfo['mobile']
		name=userinfo['name']
		email=userinfo['email']
		inviteCode=userinfo['inviteCode']
		imageName=userinfo['imageName']
		

		
		EditAssign = dbhelper.UpdateData().Updateuserlogin(Id,mobile,name,email,inviteCode,imageName)
		db={'message':'UserDataUpdate',"confirmation":1,"Id":Id,"mobile":mobile,"name":name,"email":email,"inviteCode":inviteCode,"imageName":imageName}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)		


@app.route('/education/candidate/data/',methods=['GET','POST'])
def APiUserupdatelogin2():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		mobile=userinfo['mobile']
		className=userinfo['className']
		boardName=userinfo['boardName']
		try:
			preparingForExam=userinfo['preparingForExam']
		except:
			preparingForExam=''

		categoryId=userinfo['categoryId']
		subCategoryId=userinfo['subCategoryId']
		
		EditAssign = dbhelper.UpdateData().UpdateuserData2(mobile,className,boardName,preparingForExam,categoryId,subCategoryId)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/update/user/data/',methods=['GET','POST'])
def APiUserupdateloginuser():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		mobile=userinfo['mobile']
		name=userinfo['name']
		email=userinfo['email']
		className=userinfo['className']
		boardName=userinfo['boardName']
		preparingForExam=userinfo['preparingForExam']
		inviteCode=userinfo['inviteCode']
		
		EditAssign = dbhelper.UpdateData().UpdateuserDatauser(Id,mobile,name,email,className,boardName,preparingForExam,inviteCode)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)		

@app.route('/education/delete/login/',methods=['GET','POST'])
def ApiAddlogin():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeleteDatastudent(Id)

		if update:
			db={'message':'Data Added',"confirmation":1}
		else:
			db={'message': 'Data not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)	

@app.route('/education/remove/bookmark/',methods=['GET','POST'])
def ApiremoveBookmark():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['Id']
	   
		update              =dbhelper.DeleteData().DeleteRemovebook(Id)

		if update:
			db={'message':'Data Added',"confirmation":1}
		else:
			db={'message': 'Data not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

@app.route('/education/delete/subject/concept/',methods=['GET','POST'])
def ApiremoveBookmarksub():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().Deletesubjectconcept(Id)

		if update:
			db={'message':'Data Added',"confirmation":1}
		else:
			db={'message': 'Data not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

@app.route('/education/delete/chapter/story/',methods=['GET','POST'])
def ApiremoveBookmarkchapter():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().Deletechapterstory(Id)

		if update:
			db={'message':'Data Added',"confirmation":1}
		else:
			db={'message': 'Data not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)								

@app.route('/education/get/login/details/',methods=['GET','POST'])
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

@app.route('/education/delete/video/',methods=['GET','POST'])
def ApiAddToken():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeleteData2(Id)

		if update:
			db={'message':'Token Added',"confirmation":1}
		else:
			db={'message': 'Token not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

#complain details:	

@app.route('/education/get/complain/details/',methods=['GET','POST'])
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

@app.route('/education/get/complain/list/',methods=['GET','POST'])
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


@app.route('/education/add/user/complain/',methods=['GET','POST'])
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

@app.route('/education/add/admin/reply/',methods=['GET','POST'])
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



@app.route('/education/get/complain/status/list/',methods=['GET','POST'])
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

@app.route('/education/get/complain/admin/list/',methods=['GET','POST'])
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

@app.route('/education/user/status/summary/',methods=['POST'])
def APigetSummaryList():
	if request.method=='POST':
		
		user_data = dbhelper.GetData().getUserSummary()
		
		user_data_db=[]
		
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['liveClasses']                    = line[0]
				user_data_dict['testSeries']                     = line[1]
				user_data_dict['registration']                   = line[2]
				user_data_dict['subjectList']                    = line[3]
				user_data_dict['teacherList']                    =line[4]
				user_data_dict['doubtList']                    =line[5]
				
				
				user_data_db.append(user_data_dict)

				
		resp = Response(json.dumps({"success": 1, "configure_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

# category

@app.route('/education/add/master/category/',methods=['GET','POST'])
def APiaddmaster():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		name=userinfo['name']
		description=userinfo['description']
		createdBy=userinfo['createdBy']
		
		
		AddUser = dbhelper.AddData().addUsercategory(name,description,createdBy)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","name":name,"description":description,"createdBy":createdBy}))
		return after_request(resp)

@app.route('/education/add/sub/category/',methods=['GET','POST'])
def APiaddmastersub():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		name=userinfo['name']
		description=userinfo['description']
		createdBy=userinfo['createdBy']
		categoryId=userinfo['categoryId']
		# logo=userinfo['logo']
		
		
		AddUser = dbhelper.AddData().addUsersubcategory(name,description,createdBy,categoryId)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","name":name,"description":description,"createdBy":createdBy,"categoryId":categoryId}))
		return after_request(resp)

@app.route('/education/add/last/category/',methods=['GET','POST'])
def APiaddmasterlast():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		name=userinfo['name']
		description=userinfo['description']
		createdBy=userinfo['createdBy']
		subCategoryId=userinfo['subCategoryId']
		categoryId=userinfo['categoryId']
		overview = userinfo['overview'].replace("'","")
		
		
		AddUser = dbhelper.AddData().addUserlastcategory(name,description,createdBy,subCategoryId,categoryId,overview)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","name":name,"description":description,"createdBy":createdBy,"subCategoryId":subCategoryId,"categoryId":categoryId}))
		return after_request(resp)

@app.route('/education/add/course/category/',methods=['GET','POST'])
def APiaddmastercourse():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		name=userinfo['name']
		description=userinfo['description']
		subCategoryId=userinfo['subCategoryId']
		categoryId=userinfo['categoryId']
		try:
			imageUrl=userinfo['imageUrl'].replace(" ","_")
		except:
			imageUrl=''

		chapter=userinfo['chapter']
		overview=userinfo['overview'].replace("'","")
		
		
		AddUser = dbhelper.AddData().addUsercorsecategory(name,description,subCategoryId,categoryId,imageUrl,chapter,overview)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","name":name,"description":description,"subCategoryId":subCategoryId,"categoryId":categoryId,"imageUrl":imageUrl,"chapter":chapter,"overview":overview}))
		return after_request(resp)


@app.route('/education/add/exam/details/',methods=['GET','POST'])
def APiaddmastercourseexamdetails():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		field=userinfo['field']
		eligibility=userinfo['eligibility']
		subjects=userinfo['subjects']
		applicants=userinfo['applicants']
		qualified=userinfo['qualified']
		questionsType=userinfo['questionsType']
		paperPattern=userinfo['paperPattern']
		colleges=userinfo['colleges']
		difficultyLevel=userinfo['difficultyLevel']
		prepareTime=userinfo['prepareTime']
		whens=userinfo['whens']
		examId=userinfo['examId']
		
		
		AddUser = dbhelper.AddData().addUsercorsecategoryexamdetails(field,eligibility,subjects,applicants,qualified,questionsType,paperPattern,colleges,difficultyLevel,prepareTime,whens,examId)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","field":field,"eligibility":eligibility,"subjects":subjects,"applicants":applicants,"qualified":qualified,"questionsType":questionsType,"paperPattern":paperPattern,"colleges":colleges,"difficultyLevel":difficultyLevel,"prepareTime":prepareTime,"whens":whens,"examId":examId}))
		return after_request(resp)	


@app.route('/education/get/exam/overview/',methods=['GET','POST'])
def APiGetExamoverView():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		examId=userinfo['examId']
		user_data = dbhelper.GetData().getexamOverview(examId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['field']=line[1]
				user_data_dict['eligibility']=line[2]
				user_data_dict['subjects']=line[3]
				user_data_dict['applicants']=line[4]
				user_data_dict['qualified']=line[5]
				user_data_dict['questionsType']=line[6]
				user_data_dict['paperPattern']=line[7]
				user_data_dict['colleges']=line[8]
				user_data_dict['difficultyLevel']=line[9]
				user_data_dict['prepareTime']=line[10]
				user_data_dict['whens']=line[11]
				user_data_dict['examId']=line[12]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "exam_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)	


@app.route('/education/get/course/subject/',methods=['GET','POST'])
def APiGetmastercourseSubh():
	if request.method=='POST':
		
		user_data = dbhelper.GetData().getcoursesubject()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['examId']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['description']=line[3]
				user_data_dict['subCategoryId']=line[4]
				user_data_dict['categoryId']=line[5]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				user_data_dict['chapter']=line[7]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/elearning/home/',methods=['GET','POST'])
def APiGetmastercourseSubhhome():
	if request.method=='POST':
		
		user_data = dbhelper.GetData().getcoursesubjecthome()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['headerOne']=line[1]
				user_data_dict['headerTwo']=line[2]
				user_data_dict['headerImage']=str(line[3])
				user_data_dict['headerThree']=line[4]
				user_data_dict['liveclassesHeader']=line[5]
				user_data_dict['liveclassesPara']=line[6]
				user_data_dict['liveclassesImage']=str(line[7])
				user_data_dict['videoclassesHeader']=line[8]
				user_data_dict['videoclassesPara']=line[9]
				user_data_dict['videoclassesImage']=str(line[10])
				user_data_dict['adaptivepracticeHeader']=line[11]
				user_data_dict['adaptivepracticePara']=line[12]
				user_data_dict['adaptivepracticeImage']=str(line[13])
				user_data_dict['crammingImage']=str(line[14])
				user_data_dict['crammingHeader']=line[15]
				user_data_dict['crammingPara']=line[16]
				user_data_dict['approach']=line[17]
				user_data_dict['believe']=line[18]
				user_data_dict['believePara']=line[19]
				user_data_dict['repeatHeader']=line[20]
				user_data_dict['repeatPara']=line[21]
				user_data_dict['comfort']=line[22]
				user_data_dict['comfortPara']=line[23]
				user_data_dict['lowerHeader']=line[24]
				user_data_dict['lowerPara']=line[25]
				user_data_dict['stories']=line[26]
				user_data_dict['storiesPara']=line[27]
				user_data_dict['uniqueHeader']=line[28]
				user_data_dict['uniquePara']=line[29]
				user_data_dict['approachImage']=str(line[30])
				user_data_dict['managementHeader']=line[31]
				user_data_dict['managementPara']=line[32]
				user_data_dict['tendingImage']=str(line[33])
				user_data_dict['trendingHeader']=line[34]
				user_data_dict['trendingPara']=line[35]
				user_data_dict['bookImage']=str(line[36])
				user_data_dict['bookHeader']=line[37]
				user_data_dict['bookPara']=line[38]
				user_data_dict['certifiedImage']=str(line[39])
				user_data_dict['certifiedHeader']=line[40]
				user_data_dict['certifiedPara']=line[41]
				user_data_dict['allImage']=str(line[42])
				user_data_dict['syllabusHeader']=line[43]
				user_data_dict['syllabusPara']=line[44]
				user_data_dict['flexibilityHeader']=line[45]
				user_data_dict['flexibilityPara']=line[46]
				user_data_dict['savemoneyHeader']=line[47]
				user_data_dict['savemoneyPara']=line[48]
				user_data_dict['savemoneyokHeader']=line[49]
				user_data_dict['savemoneyokPara']=line[50]
				user_data_dict['saveImage']=str(line[51])
				user_data_dict['footerImage']=str(line[52])

				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/update/elearning/home/',methods=['GET','POST'])
def APiUserupdatesubjectconhome():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		headerOne=userinfo['headerOne']
		headerTwo=userinfo['headerTwo']
		headerImage=userinfo['headerImage']
		headerThree=userinfo['headerThree']
		liveclassesHeader=userinfo['liveclassesHeader']
		liveclassesPara=userinfo['liveclassesPara']
		liveclassesImage=userinfo['liveclassesImage']
		videoclassesHeader=userinfo['videoclassesHeader']
		videoclassesPara=userinfo['videoclassesPara']
		videoclassesImage=userinfo['videoclassesImage']
		adaptivepracticeHeader=userinfo['adaptivepracticeHeader']
		adaptivepracticePara=userinfo['adaptivepracticePara']
		adaptivepracticeImage=userinfo['adaptivepracticeImage']
		crammingImage=userinfo['crammingImage']
		crammingHeader=userinfo['crammingHeader']
		crammingPara=userinfo['crammingPara']
		approach=userinfo['approach']
		believe=userinfo['believe']
		believePara=userinfo['believePara']
		repeatHeader=userinfo['repeatHeader']
		repeatPara=userinfo['repeatPara']
		comfort=userinfo['comfort']
		comfortPara=userinfo['comfortPara']
		lowerHeader=userinfo['lowerHeader']
		lowerPara=userinfo['lowerPara']
		stories=userinfo['stories']
		storiesPara=userinfo['storiesPara']
		uniqueHeader=userinfo['uniqueHeader']
		uniquePara=userinfo['uniquePara']
		approachImage=userinfo['approachImage']
		managementHeader=userinfo['managementHeader']
		managementPara=userinfo['managementPara']
		tendingImage=userinfo['tendingImage']
		trendingHeader=userinfo['trendingHeader']
		trendingPara=userinfo['trendingPara']
		bookImage=userinfo['bookImage']
		bookHeader=userinfo['bookHeader']
		bookPara=userinfo['bookPara']
		certifiedImage=userinfo['certifiedImage']
		certifiedHeader=userinfo['certifiedHeader']
		certifiedPara=userinfo['certifiedPara']
		allImage=userinfo['allImage']
		syllabusHeader=userinfo['syllabusHeader']
		syllabusPara=userinfo['syllabusPara']
		flexibilityHeader=userinfo['flexibilityHeader']
		flexibilityPara=userinfo['flexibilityPara']
		savemoneyHeader=userinfo['savemoneyHeader']
		savemoneyPara=userinfo['savemoneyPara']
		savemoneyokHeader=userinfo['savemoneyokHeader']
		savemoneyokPara=userinfo['savemoneyokPara']
		saveImage=userinfo['saveImage']
		footerImage=userinfo['footerImage']

		EditAssign = dbhelper.UpdateData().Updateuserdatasubjecthome(Id,headerOne,headerTwo,headerImage,headerThree,liveclassesHeader,liveclassesPara,liveclassesImage,videoclassesHeader,videoclassesPara,videoclassesImage,adaptivepracticeHeader,adaptivepracticePara,adaptivepracticeImage,crammingImage,crammingHeader,crammingPara,approach,believe,believePara,repeatHeader,repeatPara,comfort,comfortPara,lowerHeader,lowerPara,stories,storiesPara,uniqueHeader,uniquePara,approachImage,managementHeader,managementPara,tendingImage,trendingHeader,trendingPara,bookImage,bookHeader,bookPara,certifiedImage,certifiedHeader,certifiedPara,allImage,syllabusHeader,syllabusPara,flexibilityHeader,flexibilityPara,savemoneyHeader,savemoneyPara,savemoneyokHeader,savemoneyokPara,saveImage,footerImage)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)				

@app.route('/education/get/course/category/',methods=['GET','POST'])
def APiGetmastercourse():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subCategoryId= userinfo['subCategoryId']
		categoryId= userinfo['categoryId']
		
		user_data = dbhelper.GetData().getexamcoursecategory(subCategoryId,categoryId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['examId']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['description']=line[3]
				user_data_dict['subCategoryId']=line[4]
				user_data_dict['categoryId']=line[5]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				user_data_dict['chapter']=line[7]
				user_data_dict['overview']=line[9]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/course/category/new/',methods=['GET','POST'])
def APiGetmastercoursenew():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subCategoryId= userinfo['subCategoryId']
		categoryId= userinfo['categoryId']
		
		user_data = dbhelper.GetData().getexamcoursecategory(subCategoryId,categoryId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['examId']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['description']=line[3]
				user_data_dict['subCategoryId']=line[4]
				user_data_dict['categoryId']=line[5]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				user_data_dict['chapter']=line[7]
				user_data_dict['overview']=line[9]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/course/master/byid/',methods=['GET','POST'])
def APiGetmastercoursebyid():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		Id= userinfo['id']
		
		user_data = dbhelper.GetData().getexamcoursecategorybyid(Id)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['examId']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['description']=line[3]
				user_data_dict['subCategoryId']=line[4]
				user_data_dict['categoryId']=line[5]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				user_data_dict['chapter']=line[7]
				user_data_dict['overview']=line[9]

				categoryName = dbhelper.GetData().getexamcategorybyid(line[5])
				try:
					user_data_dict['categoryName']=categoryName[0][1]
				except:
					user_data_dict['categoryName']=''
				
				subcategoryName = dbhelper.GetData().getexamSubcategorybyid(line[4])
				try:
					user_data_dict['subcategoryName']=subcategoryName[0][1]
				except:
					user_data_dict['subcategoryName']=''
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/course/master/only/',methods=['GET','POST'])
def APiGetmastercoursebywithout():
	if request.method=='POST':
		
		user_data = dbhelper.GetData().getexamcoursecategorywithout()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['examId']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['description']=line[3]
				user_data_dict['subCategoryId']=line[4]
				user_data_dict['categoryId']=line[5]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				user_data_dict['chapter']=line[7]
				user_data_dict['overview']=line[9]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/course/master/overview/',methods=['GET','POST'])
def APiGetmastercoursebywioverview():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subjectId= userinfo['subjectId']
		
		user_data = dbhelper.GetData().getexamcoursecategorywithoutoverview(subjectId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['examId']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['description']=line[3]
				user_data_dict['subCategoryId']=line[4]
				user_data_dict['categoryId']=line[5]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				user_data_dict['chapter']=line[7]
				user_data_dict['overview']=line[9]
				categoryName = dbhelper.GetData().getexamcategorybyid(line[5])
				try:
					user_data_dict['categoryName']=categoryName[0][1]
				except:
					user_data_dict['categoryName']=''
				
				subcategoryName = dbhelper.GetData().getexamSubcategorybyid(line[4])
				try:
					user_data_dict['subcategoryName']=subcategoryName[0][1]
				except:
					user_data_dict['subcategoryName']=''

				checkStringLst= dbhelper.GetData().getexamcoursecategory(line[4],line[5])

				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['id']  = check[0]
					check_dict['examId']=check[1]
					check_dict['name']=check[2]
					check_dict['description']=check[3]
					check_dict['subCategoryId']=check[4]
					check_dict['categoryId']=check[5]
					check_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(check[6])
					check_dict['chapter']=check[7]
					check_dict['overview']=check[9]
					checkList.append(check_dict)

				user_data_dict['subjectList']=checkList

				chapterStringLst= dbhelper.GetData().getTopic(subjectId)



				chapterList=[]
				sr=0

				for checks in chapterStringLst:
					checks_dict={}
					sr=sr+1
					
					checks_dict['id']  = sr
					topicLst= dbhelper.GetData().getTopicList(checks[0])
					topic_data=[]
					sno=0
					for topic in topicLst:
						topic_dict={}
						sno= sno+1
						topic_dict['chapterName']=topic[0]
						topic_dict['sno']=sno
						topic_dict['topic']=topic[1]
						topic_dict['overview']=topic[2]
						topic_dict['chapterId']=topic[3]
						topic_data.append(topic_dict)


					checks_dict['subjectId']=checks[1]
					checks_dict['topicLst']=topic_data
					checks_dict['chapterName']=checks[2]
					checks_dict['overview']=checks[6]
					
					chapterList.append(checks_dict)

				user_data_dict['subjectList']=checkList
				user_data_dict['chapterList']=chapterList
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)						

@app.route('/education/get/course/categoryid/',methods=['GET','POST'])
def APiGetmastercourseid():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		categoryId= userinfo['categoryId']
		
		user_data = dbhelper.GetData().getexamcoursecategoryid(categoryId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['examId']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['description']=line[3]
				user_data_dict['subCategoryId']=line[4]
				user_data_dict['categoryId']=line[5]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				user_data_dict['chapter']=line[7]
				user_data_dict['overview']=line[9]

				categoryName = dbhelper.GetData().getexamcategorybyid(line[5])
				try:
					user_data_dict['categoryName']=categoryName[0][1]
				except:
					user_data_dict['categoryName']=''
				
				subcategoryName = dbhelper.GetData().getexamSubcategorybyid(line[4])
				try:
					user_data_dict['subcategoryName']=subcategoryName[0][1]
				except:
					user_data_dict['subcategoryName']=''
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/course/subcategoryid/',methods=['GET','POST'])
def APiGetmastercoursesubid():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subCategoryId= userinfo['subCategoryId']
		
		user_data = dbhelper.GetData().getexamcoursecategorysubid(subCategoryId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['examId']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['description']=line[3]
				user_data_dict['subCategoryId']=line[4]
				user_data_dict['categoryId']=line[5]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				user_data_dict['chapter']=line[7]
				user_data_dict['overview']=line[9]

				categoryName = dbhelper.GetData().getexamcategorybyid(line[5])
				try:
					user_data_dict['categoryName']=categoryName[0][1]
				except:
					user_data_dict['categoryName']=''
				
				subcategoryName = dbhelper.GetData().getexamSubcategorybyid(line[4])
				try:
					user_data_dict['subcategoryName']=subcategoryName[0][1]
				except:
					user_data_dict['subcategoryName']=''
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)				

@app.route('/education/update/course/category/',methods=['GET','POST'])
def APiUserupdatecourse():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		examId=userinfo['examId']
		name=userinfo['name']
		description=userinfo['description']
		subCategoryId=userinfo['subCategoryId']
		categoryId=userinfo['categoryId']
		overview=userinfo['overview'].replace("'","")

		
		EditAssign = dbhelper.UpdateData().Updateuserlastcourse(Id,examId,name,description,subCategoryId,categoryId,overview)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/delete/course/category/',methods=['GET','POST'])
def ApiAddmastercoursedel():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeleteDatamastercourse(Id)

		if update:
			db={'message':'course Added',"confirmation":1}
		else:
			db={'message': 'course not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)	

@app.route('/education/delete/course/chapter/list/',methods=['GET','POST'])
def ApicoursechapterList():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeletecourseChapterList(Id)

		if update:
			db={'message':'course Added',"confirmation":1}
		else:
			db={'message': 'course not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)					

@app.route('/education/add/subject/category/',methods=['GET','POST'])
def APiaddmastersubject():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		examId=userinfo['examId']
		name=userinfo['name']
		description=userinfo['description']
		sourceId=userinfo['sourceId']
		subCategoryId=userinfo['subCategoryId']
		categoryId=userinfo['categoryId']
		
		
		
		AddUser = dbhelper.AddData().addUsersubject(examId,name,description,sourceId,subCategoryId,categoryId)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","examId":examId,"name":name,"description":description,"sourceId":sourceId,"subCategoryId":"subCategoryId","categoryId":categoryId}))
		return after_request(resp)

@app.route('/education/add/subject/chapter/',methods=['GET','POST'])
def APiaddmastersubject2():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subjectId=userinfo['subjectId']
		categoryId=userinfo['categoryId']
		subCategoryId=userinfo['subcategoryId']
		chapter=userinfo['chapter']
		imageUrl= userinfo['imageUrl'].replace(" ","_")
		
		
		AddUser = dbhelper.AddData().addUsersubjectChapter(subjectId,subCategoryId,categoryId,chapter,imageUrl)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","subjectId":subjectId,"subCategoryId":subCategoryId,"categoryId":categoryId,"chapter":chapter}))
		return after_request(resp)

@app.route('/education/get/subject/category/',methods=['GET','POST'])
def APiGetmastersubject():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subCategoryId= userinfo['subCategoryId']
		categoryId= userinfo['categoryId']
		sourceId= userinfo['sourceId']
		user_data = dbhelper.GetData().getexamsubjectcategory(subCategoryId,categoryId,sourceId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['examId']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['description']=line[3]
				user_data_dict['sourceId']=line[4]
				user_data_dict['subCategoryId']=line[5]
				user_data_dict['categoryId']=line[6]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/update/subject/category/',methods=['GET','POST'])
def APiUserupdatesubject():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		examId=userinfo['examId']
		name=userinfo['name']
		description=userinfo['description']
		sourceId=userinfo['sourceId']
		subCategoryId=userinfo['subCategoryId']
		categoryId=userinfo['categoryId']

		
		EditAssign = dbhelper.UpdateData().Updateuserlastsubject(Id,examId,name,description,sourceId,subCategoryId,categoryId)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/delete/subject/category/',methods=['GET','POST'])
def ApiAddmastersubjectdel():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeleteDatamastersubject(Id)

		if update:
			db={'message':'subject Added',"confirmation":1}
		else:
			db={'message': 'subject not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)																

@app.route('/education/get/master/category/',methods=['GET','POST'])
def APiGetmaster():
	if request.method=='POST':
		# userinfo   = json.loads(request.data)
		user_data = dbhelper.GetData().getexamcategory()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['categoryId']  = line[0]
				user_data_dict['name']=line[1]
				user_data_dict['description']=line[2]
				user_data_dict['createdBy']=line[3]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/sub/category/simple/',methods=['GET','POST'])
def APiGetmastersimple():
	if request.method=='POST':
		user_data = dbhelper.GetData().getsubCategorysimple()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['subcategoryId']  = line[0]
				user_data_dict['name']=line[1]
				user_data_dict['description']=line[2]
				user_data_dict['createdBy']=line[3]
				user_data_dict['categoryId']=line[5]
				user_data_dict['logo']='https://storage.googleapis.com/courseimage/'+str(line[6])
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/education/get/sub/category/',methods=['GET','POST'])
def APiGetmastersub():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		categoryId= userinfo['categoryId']
		user_data = dbhelper.GetData().getexamsubcategory(categoryId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['subcategoryId']  = line[0]
				user_data_dict['name']=line[1]
				user_data_dict['description']=line[2]
				user_data_dict['createdBy']=line[3]
				user_data_dict['categoryId']=line[5]
				user_data_dict['logo']='https://storage.googleapis.com/courseimage/'+str(line[6])
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/board/name/',methods=['GET','POST'])
def APiGetboradname():
	if request.method=='POST':
		user_data = dbhelper.GetData().getexamboard()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['bardname']=line[1]
				user_data_dict['description']=line[2]
				user_data_dict['createdBy']=line[3]
				user_data_dict['categoryId']=line[5]
				user_data_dict['logo']=line[6]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)		


@app.route('/education/get/notification/',methods=['GET','POST'])
def APiGetNotifcation():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile= userinfo['mobile']
		user_data = dbhelper.GetData().getnotice(mobile)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['mobile']  = line[1]
				user_data_dict['message']=line[2]
				user_data_dict['title']=line[3]
				user_data_dict['date']=line[4]
				user_data_dict['time']=line[5]
			
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "notice_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/admin/notification/',methods=['GET','POST'])
def APiGeAdtNotifcation():
	if request.method=='POST':
		
		user_data = dbhelper.GetData().getAdminnotice()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['mobile']  = line[1]
				user_data_dict['message']=line[2]
				user_data_dict['title']=line[3]
				user_data_dict['date']=line[4]
				user_data_dict['time']=line[5]
			
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "notice_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/last/category/',methods=['GET','POST'])
def APiGetmasterlast():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subCategoryId= userinfo['subCategoryId']
		categoryId= userinfo['categoryId']
		user_data = dbhelper.GetData().getexamlastcategory(subCategoryId,categoryId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['name']=line[1]
				user_data_dict['description']=line[2]
				user_data_dict['createdBy']=line[3]
				user_data_dict['subCategoryId']=line[5]
				user_data_dict['categoryId']=line[6]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)	


@app.route('/education/get/subjet/chapter/list/',methods=['GET','POST'])
def APiGetsubjectChapterList():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subCategoryId= userinfo['subCategoryId']
		categoryId= userinfo['categoryId']
		subjectId= userinfo['subjectId']
		user_data = dbhelper.GetData().getsubjectChapterList(subCategoryId,categoryId,subjectId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['subjectId']=line[1]
				sub_data = dbhelper.GetData().getSubName(line[1])[0][0]
				user_data_dict['subjectName']=sub_data
				user_data_dict['chapter']=line[2]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[5])
				user_data_dict['overview']=line[6]
				
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)					



@app.route('/education/update/master/category/',methods=['GET','POST'])
def APiUserupdatemaster():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		name=userinfo['name']
		description=userinfo['description']
		createdBy=userinfo['createdBy']
		

		
		EditAssign = dbhelper.UpdateData().Updateusercategory(Id,name,description,createdBy)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/education/update/subject/chapter/',methods=['GET','POST'])
def APiUsersubjectChapter():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		Id=userinfo['id']
		chapter=userinfo['chapter']
		overview = userinfo['overview'].replace("'","")
		
		EditAssign = dbhelper.UpdateData().UpdatesubjectChapter(Id,overview,chapter)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/update/sub/category/',methods=['GET','POST'])
def APiUserupdatesub():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		name=userinfo['name']
		description=userinfo['description']
		createdBy=userinfo['createdBy']
		categoryId=userinfo['categoryId']
		

		
		EditAssign = dbhelper.UpdateData().Updateusersubcategory(Id,name,description,createdBy,categoryId)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/update/last/category/',methods=['GET','POST'])
def APiUserupdatelast():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		name=userinfo['name']
		description=userinfo['description']
		createdBy=userinfo['createdBy']
		subCategoryId=userinfo['subCategoryId']
		categoryId=userinfo['categoryId']

		
		EditAssign = dbhelper.UpdateData().Updateuserlastcategory(Id,name,description,createdBy,subCategoryId,categoryId)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)				

@app.route('/education/delete/master/category/',methods=['GET','POST'])
def ApiAddmastercat():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
		

	   
		update              =dbhelper.DeleteData().DeleteDatamaster(Id)
		user_data = dbhelper.GetData().getexamcategory()
		# user_data = dbhelper.GetData().getexamcategory()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['categoryId']  = line[0]
				user_data_dict['name']=line[1]
				user_data_dict['description']=line[2]
				user_data_dict['createdBy']=line[3]
				
				user_data_db.append(user_data_dict)

		if update:
			db={'message':'Token Added',"confirmation":1,"user_data":user_data_db}
		else:
			db={'message': 'Token not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

@app.route('/education/delete/sub/category/',methods=['GET','POST'])
def ApiAddmastersubcat():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeleteDatamastersub(Id)

		if update:
			db={'message':'Token Added',"confirmation":1}
		else:
			db={'message': 'Token not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

@app.route('/education/delete/last/category/',methods=['GET','POST'])
def ApiAddmasterlastcat():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeleteDatamasterlast(Id)

		if update:
			db={'message':'Token Added',"confirmation":1}
		else:
			db={'message': 'Token not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)				

# live classes

@app.route('/education/add/live/classes/',methods=['GET','POST'])
def APiadduseliveclasses():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		chapterId=userinfo['chapterId']
		subjectId=userinfo['subjectId']
		categoryId=userinfo['categoryId']
		subcategoryId=userinfo['subcategoryId']
		
		topic=userinfo['topic']
		videoUrl=userinfo['videoUrl']
		imageUrl=userinfo['imageUrl'].replace(" ","_")
		document=userinfo['document']
		com_status=userinfo['com_status']
		duration= userinfo['duration']
		
		
		AddUser = dbhelper.AddData().addUserliveclasses(chapterId,subjectId,categoryId,subcategoryId,topic,videoUrl,imageUrl,document,com_status,duration)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","imageUrl":imageUrl,"videoUrl":videoUrl}))
		return after_request(resp)

@app.route('/education/add/subject/concept/',methods=['GET','POST'])
def APiadduseliveclassessubject():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		chapterId=userinfo['chapterId']
		definition=userinfo['definition']
		imageUrl=userinfo['imageUrl'].replace(" ","_")
		categoryId=userinfo['categoryId']
		
		subcategoryId=userinfo['subcategoryId']
		subjectId=userinfo['subjectId']
		topic=userinfo['topic']
		
		AddUser = dbhelper.AddData().addUserliveclassessubject(chapterId,definition,imageUrl,categoryId,subcategoryId,subjectId,topic)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","imageUrl":imageUrl}))
		return after_request(resp)

# @app.route('/education/get/subject/concept2/',methods=['GET','POST'])
# def APiGetliveclassessubject():
# 	if request.method=='POST':
# 		# userinfo   = json.loads(request.data)
# 		user_data = dbhelper.GetData().getexamliveclassessubject()
# 		user_data_db=[]
# 		if(len(user_data))>0:
# 			for line in user_data:
# 				user_data_dict={}
# 				user_data_dict['id']  = line[0]
# 				user_data_dict['chapterId']=line[1]
# 				user_data_dict['definition']=line[2]
# 				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[3])
# 				user_data_dict['categoryId']=line[4]
# 				user_data_dict['subcategoryId']=line[5]
# 				user_data_dict['subjectId']=line[6]
# 				user_data_dict['topic']  = line[7]
# 				user_data_db.append(user_data_dict)
				
# 		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
# 		resp.headers['Content-type']='application/json'
# 		return after_request(resp)

@app.route('/education/add/chapter/story/',methods=['GET','POST'])
def APiadduseliveclassesstory():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		chapterId=userinfo['chapterId']
		definition=userinfo['definition']
		imageUrl=userinfo['imageUrl'].replace(" ","_")
		categoryId=userinfo['categoryId']
		
		subcategoryId=userinfo['subcategoryId']
		subjectId=userinfo['subjectId']
		topic=userinfo['topic']
		topicId=userinfo['topicId']
		overview=userinfo['overview']
		
		AddUser = dbhelper.AddData().addUserliveclassesstory(chapterId,definition,imageUrl,categoryId,subcategoryId,subjectId,topic,topicId,overview)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","imageUrl":imageUrl}))
		return after_request(resp)

@app.route('/education/get/chapter/story2/',methods=['GET','POST'])
def APiGetliveclassesstory():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		categoryId=userinfo['categoryId']
		subcategoryId=userinfo['subcategoryId']
		subjectId=userinfo['subjectId']
		# userinfo   = json.loa````````````````````````````````````````````````````````````````````````````````````ds(request.data)
		user_data = dbhelper.GetData().getexamliveclassesstory(categoryId,subcategoryId,subjectId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['chapterId']=line[1]
				user_data_dict['definition']=line[2]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[3])
				user_data_dict['createdAt']=str(line[4])
				user_data_dict['categoryId']=line[5]
				user_data_dict['subcategoryId']=line[6]
				user_data_dict['subjectId']=line[7]
				user_data_dict['topic']  = line[8]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/chapter/story/details/',methods=['GET','POST'])
def APiGetliveclassesstorydetails():
	if request.method=='POST':
		
		user_data = dbhelper.GetData().getstoryDetails()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['chapterId']=line[1]
				user_data_dict['definition']=line[2]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[3])
				user_data_dict['createdAt']=str(line[4])
				user_data_dict['categoryId']=line[5]
				categoryName = dbhelper.GetData().getexamcategorybyid(line[5])
				try:
					user_data_dict['categoryName']=categoryName[0][1]
				except:
					user_data_dict['categoryName']=''
				user_data_dict['subcategoryId']=line[6]
				subcategoryName = dbhelper.GetData().getexamSubcategorybyid(line[6])
				try:
					user_data_dict['subcategoryName']=subcategoryName[0][1]
				except:
					user_data_dict['subcategoryName']=''
				user_data_dict['subjectId']=line[7]
				user_data_dict['topic']  = line[8]
				user_data_dict['topicId']  = line[9]
				user_data_dict['overview']  = line[8]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/subject/concept2/',methods=['GET','POST'])
def APiGetliveclassessubjectcon():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		categoryId=userinfo['categoryId']
		subcategoryId=userinfo['subcategoryId']
		subjectId=userinfo['subjectId']
		# userinfo   = json.loa````````````````````````````````````````````````````````````````````````````````````ds(request.data)
		user_data = dbhelper.GetData().getexamliveclassessubject2(categoryId,subcategoryId,subjectId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['chapterId']=line[1]
				user_data_dict['definition']=line[2]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[3])
				user_data_dict['createdAt']=str(line[4])
				user_data_dict['categoryId']=line[5]

				user_data_dict['subcategoryId']=line[6]
				user_data_dict['subjectId']=line[7]
				user_data_dict['topic']  = line[8]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)		

@app.route('/education/get/subject/concept/details/',methods=['GET','POST'])
def APiGetConecptDetails():
	if request.method=='POST':
		
		user_data = dbhelper.GetData().getconceptDetails()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['chapterId']=line[1]
				user_data_dict['definition']=line[2]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[3])
				user_data_dict['createdAt']=str(line[4])
				user_data_dict['categoryId']=line[5]
				categoryName = dbhelper.GetData().getexamcategorybyid(line[5])
				try:
					user_data_dict['categoryName']=categoryName[0][1]
				except:
					user_data_dict['categoryName']=''
				user_data_dict['subcategoryId']=line[6]
				subcategoryName = dbhelper.GetData().getexamSubcategorybyid(line[6])
				try:
					user_data_dict['subcategoryName']=subcategoryName[0][1]
				except:
					user_data_dict['subcategoryName']=''
				user_data_dict['subjectId']=line[7]
				user_data_dict['topic']  = line[8]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)					

@app.route('/education/add/chapter/video/',methods=['GET','POST'])
def APiadduseliveclasses2():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		chapterId=userinfo['chapterId']
		topic=userinfo['topic']
		videoUrl=userinfo['videoUrl']
		duration=userinfo['duration']
		imageUrl=userinfo['imageUrl'].replace(" ","_")
		
		AddUser = dbhelper.AddData().addUserchapterVideo(chapterId,topic,videoUrl,duration,imageUrl)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","chapterId":chapterId,"topic":topic,"videoUrl":videoUrl,"duration":duration,"imageUrl":imageUrl}))
		return after_request(resp)

# @app.route('/education/get/chapter/video/',methods=['GET','POST'])
# def APiGetchaptervideo():
# 	if request.method=='POST':
# 		# userinfo   = json.loads(request.data)
# 		user_data = dbhelper.GetData().getexamchaptervideo()
# 		user_data_db=[]
# 		if(len(user_data))>0:
# 			for line in user_data:
# 				user_data_dict={}
# 				user_data_dict['id']  = line[0]
# 				user_data_dict['chapterId']=line[1]
# 				user_data_dict['topic']=line[2]
# 				user_data_dict['videoUrl']=line[3]
# 				user_data_dict['duration']=line[4]
# 				user_data_dict['imageUrl']=line[5]
# 				user_data_db.append(user_data_dict)
				
# 		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
# 		resp.headers['Content-type']='application/json'
# 		return after_request(resp)


@app.route('/education/update/chapter/video/',methods=['GET','POST'])
def APiUserchaptervideo():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		chapterId=userinfo['chapterId']
		topic=userinfo['topic']
		videoUrl=userinfo['videoUrl']
		duration=userinfo['duration']
		imageUrl=userinfo['imageUrl'].replace(" ","_")

		
		EditAssign = dbhelper.UpdateData().Updatechaptervideo(Id,chapterId,topic,videoUrl,duration,imageUrl)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/delete/chapter/video/',methods=['GET','POST'])
def ApiAddchaptervidieo():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeleteDatavideo(Id)

		if update:
			db={'message':'video Added',"confirmation":1}
		else:
			db={'message': 'video not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)				

@app.route('/education/get/live/classes/',methods=['GET','POST'])
def APiGetliveclasses():
	if request.method=='POST':
		# userinfo   = json.loads(request.data)
		user_data = dbhelper.GetData().getexamliveclasses()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['chapterId']=line[1]
				user_data_dict['topic']=line[2]
				user_data_dict['videoUrl']=str(line[3])+'?rel=0&amp;modestbranding=1&amp;showinfo=0'
				user_data_dict['duration']=line[4]
				user_data_dict['imageUrl']=line[5]
				user_data_dict['documentUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				user_data_dict['createdBy']  = line[7]
				user_data_dict['com_status']=line[8]
				user_data_dict['status']=line[14]
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/education/update/live/classes/',methods=['GET','POST'])
def APiUserupdate():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		topic=userinfo['topic']
		videoUrl=userinfo['videoUrl']
		duration=userinfo['duration']
		imageUrl=userinfo['imageUrl'].replace(" ","_")
		documentUrl=userinfo['documentUrl']
		createdBy=userinfo['createdBy']
		com_status=userinfo['com_status']

		
		EditAssign = dbhelper.UpdateData().Updateuserdata(Id,topic,videoUrl,duration,imageUrl,documentUrl,createdBy,com_status)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/update/subject/concept/',methods=['GET','POST'])
def APiUserupdatesubjectcon():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		definition=userinfo['definition']
		EditAssign = dbhelper.UpdateData().Updateuserdatasubject(Id,definition)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/update/chapter/story/',methods=['GET','POST'])
def APiUserupdatechapter():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		definition=userinfo['definition']
		EditAssign = dbhelper.UpdateData().Updateuserdatachapter(Id,definition)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)				

@app.route('/education/delete/live/classes/',methods=['GET','POST'])
def ApiAddmasterclasses():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeleteDatalive(Id)

		if update:
			db={'message':'Token Added',"confirmation":1}
		else:
			db={'message': 'Token not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

# EXAM New

@app.route('/education/add/exam/new/',methods=['GET','POST'])
def APiaddexamn():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		title=userinfo['title']
		description=userinfo['description']
		categoryId=userinfo['categoryId']
		createdBy=userinfo['createdBy']
		duration=userinfo['duration']
		
		
		AddUser = dbhelper.AddData().addUserexamnew(title,description,categoryId,createdBy,duration)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","title":title,"description":description,"categoryId":categoryId,"createdBy":createdBy}))
		return after_request(resp)

@app.route('/education/get/exam/new/',methods=['GET','POST'])
def APiGetmasterexam():
	if request.method=='POST':
		# userinfo   = json.loads(request.data)
		user_data = dbhelper.GetData().getexamnew()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['examId']  = line[0]
				user_data_dict['title']=line[1]
				user_data_dict['description']=line[2]
				user_data_dict['categoryId']=line[3]
				user_data_dict['createdBy']=line[4]
				user_data_dict['createdAt']=str(line[5])
				user_data_dict['duration']=line[6]
				user_data_dict['examStatus']=line[9]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)			


@app.route('/education/get/exam/teacher/',methods=['GET','POST'])
def APiGetmasterteacher():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		email = userinfo['email']
		user_data = dbhelper.GetData().getexamnewteacher(email)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['examId']  = line[0]
				user_data_dict['title']=line[1]
				user_data_dict['description']=line[2]
				user_data_dict['categoryId']=line[3]
				user_data_dict['createdBy']=line[4]
				user_data_dict['createdAt']=str(line[5])
				user_data_dict['duration']=line[6]
				user_data_dict['examStatus']=line[9]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)	


@app.route('/education/get/video/teacher/',methods=['GET','POST'])
def APiGetVideoteacher():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		email = userinfo['email']
		user_data = dbhelper.GetData().getvideoteacher(email)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['chapterId']  = line[1]
				user_data_dict['topic']=line[2]
				user_data_dict['videoUrl']=line[3]
				user_data_dict['duration']=line[4]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[5])
				user_data_dict['document']='https://storage.googleapis.com/courseimage/'+str(line[6])
				
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)	

@app.route('/education/get/subject/list2/',methods=['GET','POST'])
def APiGetSubject():
	if request.method=='POST':
		user_data = dbhelper.GetData().getsubject()
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['name']  = line[0]
				user_data_dict['id']=line[1]
				
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "subject_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)	



@app.route('/education/update/exam/new/',methods=['GET','POST'])
def APiUserupdateexamn():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		title=userinfo['title']
		description=userinfo['description']
		categoryId=userinfo['categoryId']
		createdBy=userinfo['createdBy']
		duration=userinfo['duration']
		

		
		EditAssign = dbhelper.UpdateData().Updateuserexam(Id,title,description,categoryId,createdBy,duration)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/delete/exam/new/',methods=['GET','POST'])
def ApiAddexamne():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeleteDataexam(Id)

		if update:
			db={'message':'exam deleted',"confirmation":1}
		else:
			db={'message': 'exam not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

#Question:

@app.route('/education/add/exam/question/',methods=['GET','POST'])
def APiaddexamquestion():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		questionType=userinfo['questionType']
		question=userinfo['question']
		optionA=userinfo['optionA']
		optionB=userinfo['optionB']
		optionC=userinfo['optionC']
		optionD=userinfo['optionD']
		correctAns=userinfo['correctAns']
		examId=userinfo['examId']
		
		
		AddUser = dbhelper.AddData().addUserexamquestion(questionType,question,optionA,optionB,optionC,optionD,correctAns,examId)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","questionType":questionType,"question":question,"optionA":optionA,"optionB":optionB,"optionC":optionC,"optionD":optionD,"correctAns":correctAns,"examId":examId}))
		return after_request(resp)

@app.route('/education/update/exam/question/',methods=['GET','POST'])
def APiUserupdatelogin2new():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		question=userinfo['question']
		optionA=userinfo['optionA']
		optionB=userinfo['optionB']
		optionC=userinfo['optionC']
		optionD=userinfo['optionD']
		correctAns=userinfo['correctAns']
		examId=userinfo['examId']
		description=userinfo['description']
		marks=userinfo['marks']
		negativeMarks=userinfo['negativeMarks']
		
		EditAssign = dbhelper.UpdateData().UpdateuserDatanew(Id,question,optionA,optionB,optionC,optionD,correctAns,examId,description,marks,negativeMarks)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/delete/exam/question/',methods=['GET','POST'])
def ApiAddmastercoursequestion():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeleteDataquestion(Id)

		if update:
			db={'message':'course Added',"confirmation":1}
		else:
			db={'message': 'course not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)				

@app.route('/education/add/teacher/video/',methods=['GET','POST'])
def APiaddTeacherVideo():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		chapterId=userinfo['chapterId']
		imageUrl=userinfo['imageUrl']
		videoUrl=userinfo['videoUrl']
		try:
			documentUrl=userinfo['documentUrl']
		except:
			documentUrl=''

		duration=userinfo['duration']
		createdBy=userinfo['createdBy']
		topic=userinfo['topic']
		
		
		AddUser = dbhelper.AddData().addTecaherVideo(chapterId,imageUrl,videoUrl,documentUrl,duration,createdBy,topic)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)

@app.route('/education/get/exam/question/',methods=['GET','POST'])
def APiGetmasterexamquestion():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		examId   = userinfo['examId']
		user_data = dbhelper.GetData().getexamnewquestion(examId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['questionId']  = line[0]
				user_data_dict['question']=line[1]
				user_data_dict['optionA']=line[2]
				user_data_dict['optionB']=line[3]
				user_data_dict['optionC']=line[4]
				user_data_dict['optionD']=line[5]
				user_data_dict['correctAns']=line[6]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[8])
				user_data_dict['description']=line[9]
				user_data_dict['examId']=line[10]
				user_data_dict['marks']=line[12]
				user_data_dict['negativeMarks']=line[13]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/education/get/test/rank/',methods=['GET','POST'])
def APiGetTestRank():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		examId   = userinfo['examId']
		mobile = userinfo['mobile']
		user_data = dbhelper.GetData().getTestRank(examId)
		sno = 0
		user_data_db=[]
		user_data_db2=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				sno=sno+1
				user_data_dict['id']  = sno
				user_data_dict['examId']=line[1]
				user_data_dict['totalQuestion']=line[2]
				user_data_dict['correctAns']=line[4]
				user_data_dict['wrongAns']=line[5]
				user_data_dict['attempted']=int(line[4])+int(line[5])
				user_data_dict['examTime']=line[6]
				user_data_dict['mobile']=line[9]
				getuserName = dbhelper.GetData().getregister(line[9])
				user_data_dict['name']= getuserName[0][2]
				user_data_dict['description']=line[9]
				getMarks = dbhelper.GetData().getMarks(line[1],line[9])
				user_data_dict['marks']=getMarks[0][0]
				user_data_dict['negativeMarks']=getMarks[0][1]
				user_data_dict['getMarks']=int(getMarks[0][0])-int(getMarks[0][1])
				gettotalMarks = dbhelper.GetData().getTotalExamMarks(line[1])
				user_data_dict['totalMarks']=int(gettotalMarks[0][0])
				

				# user_data_dict['examId']=line[10]
				if line[9]==mobile:
					user_data_dict2={}
					user_data_dict2['id']  = sno
					user_data_dict2['examId']=line[1]
					user_data_dict2['totalQuestion']=line[2]
					# user_data_dict2['attempted']=line[3]
					user_data_dict2['correctAns']=line[4]
					user_data_dict2['wrongAns']=line[5]
					user_data_dict2['attempted']=int(line[4])+int(line[5])
					user_data_dict2['examTime']=line[6]
					user_data_dict2['mobile']=line[9]
					getuserName = dbhelper.GetData().getregister(line[9])
					user_data_dict2['name']= getuserName[0][2]

					user_data_dict2['description']=line[9]
					getMarks = dbhelper.GetData().getMarks(line[1],line[9])
					user_data_dict2['marks']=getMarks[0][0]
					user_data_dict2['negativeMarks']=getMarks[0][1]
					user_data_dict2['getMarks']=int(getMarks[0][0])-int(getMarks[0][1])
					# user_data_dict2['totalMarks']=int(getMarks[0][0])-int(getMarks[0][1])
					gettotalMarks = dbhelper.GetData().getTotalExamMarks(line[1])
					user_data_dict2['totalMarks']=int(gettotalMarks[0][0])
					# user_data_dict2['examId']=line[10]
					user_data_db2.append(user_data_dict2)

				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "exam_data": user_data_db,"user_data_db2" :user_data_db2}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/exam/chapter/video/',methods=['GET','POST'])
def APiGetmasterexamquestionchapter():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		chapterId   = userinfo['chapterId']
		categoryId   = userinfo['categoryId']
		subCategoryId   = userinfo['subCategoryId']
		subjectId   = userinfo['subjectId']
		user_data = dbhelper.GetData().getexamnewquestionvideo(chapterId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['chapterId']=line[1]
				user_data_dict['topic']=line[2]
				user_data_dict['videoUrl']=line[3]
				user_data_dict['duration']=line[4]
				user_data_dict['imageUrl']=line[5]
				user_data_dict['documentUrl']=line[6]
				user_data_dict['createdBy']=line[7]
				user_data_dict['com_status']=line[8]
				user_data_dict['categoryId']=line[9]
				user_data_dict['subCategoryId']=line[10]
				user_data_dict['subjectId']=line[11]
				user_data_dict['likes']=line[12]
				user_data_dict['dislikes']=line[13]
				user_data_dict['status']=line[14]

				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)				



@app.route('/education/update/exam/question/',methods=['GET','POST'])
def APiUserupdateexamquestion():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['questionid']
		questionType=userinfo['questionType']
		question=userinfo['question']
		optionA=userinfo['optionA']
		optionB=userinfo['optionB']
		optionC=userinfo['optionC']
		optionD=userinfo['optionD']
		correctAns=userinfo['correctAns']
		examId=userinfo['examId']
		marks=userinfo['marks']
		negativeMarks=userinfo['negativeMarks']
		

		
		EditAssign = dbhelper.UpdateData().Updateuserexamquestion(Id,questionType,question,optionA,optionB,optionC,optionD,correctAns,examId,marks,negativeMarks)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/delete/exam/question/',methods=['GET','POST'])
def ApiAddexamquestiondel():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeleteDataexamquestion(Id)

		if update:
			db={'message':'Token Added',"confirmation":1}
		else:
			db={'message': 'Token not added', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

#examMaster:

@app.route('/education/add/exam/history/',methods=['GET','POST'])
def APiaddexamhistory():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		
		
		examId=userinfo['examId']
		totalQuestion=userinfo['totalQuestion']
		attempted=userinfo['attempted']
		correctAns=userinfo['correctAns']
		wrongAns=userinfo['wrongAns']
		examTime=userinfo['examTime']
		categoryId=userinfo['categoryId']
		
		
		AddUser = dbhelper.AddData().addUserexamque(examId,totalQuestion,attempted,correctAns,wrongAns,examTime,categoryId)
		db={'message':'User Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success","examId":examId,"totalQuestion":totalQuestion,"attempted":attempted,"correctAns":correctAns,"wrongAns":wrongAns,"examTime":examTime,"categoryId":categoryId}))
		return after_request(resp)

@app.route('/education/get/exam/history/',methods=['GET','POST'])
def APiGetmasterexamhistory():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile = userinfo['mobile']
		user_data = dbhelper.GetData().getexamnewexamhistory(mobile)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['examId']  = line[1]
				user_data_dict['totalQuestion']=line[2]
				user_data_dict['attempted']=line[3]
				user_data_dict['correctAns']=line[4]
				user_data_dict['wrongAns']=line[5]
				user_data_dict['examTime']=line[6]
				user_data_dict['categoryId']=line[7]
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "lecturer_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)		

@app.route('/education/add/question/summary/',methods=['GET','POST'])
def APiaddquesummary():
	if request.method=='POST':
		examInfo   = json.loads(request.data)
		dataLst          = examInfo['data']
		examId=examInfo['examId']
		totalQuestion=examInfo['totalQuestion']
		attempted=examInfo['attempted']
		correctAns=examInfo['correctAns']
		wrongAns=examInfo['wrongAns']
		examTime=examInfo['examTime']
		categoryId=examInfo['categoryId']
		mobile=examInfo['mobile']
		AddUser = dbhelper.AddData().addUserexamque(examId,totalQuestion,attempted,correctAns,wrongAns,examTime,categoryId,mobile)

		print dataLst
		for userinfo in dataLst:
		
			mobile=userinfo['mobile']
			examId=userinfo['examId']
			questionId=userinfo['questionId']
			user_data = dbhelper.GetData().getquestionMarks(questionId)
			mark=user_data[0][0]
			negativeMark=user_data[0][1]
			answers=userinfo['answer']
			correct=userinfo['correct']
			if isinstance(answers, int) == True:
				pass
			else:
				answer=userinfo['answer']
				if correct == answer:
					marks= mark
					negativeMarks=0

				else:
					negativeMarks = negativeMark
					marks = 0



			
			
			AddUser = dbhelper.AddData().addUsersummary(mobile,examId,questionId,answer,correct,marks,negativeMarks)
			db={'message':'Quiz Response Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)

# @app.route('/education/add/exam/summary/',methods=['GET','POST'])
# def APiaddexasummary():
# 	if request.method=='POST':
# 		userinfo   = json.loads(request.data)
		
		
# 		mobile=userinfo['mobile']
# 		examId=userinfo['examId']
# 		questionId=userinfo['questionId']
# 		answer=userinfo['answer']
# 		correct=userinfo['correct']
		
		
# 		AddUser = dbhelper.AddData().addUsersummary(mobile,examId,questionId,answer,correct)
# 		db={'message':'User Added',"confirmation":1}
		
# 		resp = Response(json.dumps({"response":"success","mobile":mobile,"examId":examId,"questionId":questionId,"answer":answer,"correct":correct}))
# 		return after_request(resp)		


@app.route('/education/update/exam/history/',methods=['GET','POST'])
def APiUserupdateexamhistory():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['id']
		examId=userinfo['examId']
		totalQuestion=userinfo['totalQuestion']
		attempted=userinfo['attempted']
		correctAns=userinfo['correctAns']
		wrongAns=userinfo['wrongAns']
		examTime=userinfo['examTime']
		categoryId=userinfo['categoryId']
		

		
		EditAssign = dbhelper.UpdateData().Updateuserexamhistory(Id,examId,totalQuestion,attempted,correctAns,wrongAns,examTime,categoryId)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/education/user/doubt/',methods=['GET','POST'])
def APiUserDoubt():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		mobile=userinfo['mobile']
		subjectId=userinfo['subjectId']
		subject=userinfo['subject']
		doubt=userinfo['doubt']
		imageUrl = userinfo['imageUrl'].replace(" ","_")
		lastId             =dbhelper.GetData().getdoubtLastID()[0][0]
		if lastId:
			newid=str(123+lastId)
		else:
			newid=str(123)
		cellPhone = mobile
		doubtId = 'CRN' + str(cellPhone[-4:]) + newid
		try:
			videoUrl= userinfo['videoUrl']
		except:
			videoUrl=''

		try:
			videoId = userinfo['videoId']
		except:
			videoId =''
		now= datetime.now()
		date= now.strftime('%d/%m/%Y')
		time= now.strftime("%I:%M %p" )
		
		AddUser = dbhelper.AddData().addUserdoubt(mobile,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,date,time)
		db={'message':'Doubt Added',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/education/user/chat/',methods=['GET','POST'])
def APiUserChat():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		mobile=userinfo['mobile']
		subjectId=userinfo['subjectId']
		subject=userinfo['subject']
		doubt=userinfo['doubt']
		imageUrl = userinfo['imageUrl'].replace(" ","_")
		doubtId = userinfo['doubtId']
		now= datetime.now()
		date= now.strftime('%d/%m/%Y')
		time= now.strftime("%I:%M %p" )
		try:
			videoUrl= userinfo['videoUrl']
		except:
			videoUrl=''

		try:
			videoId = userinfo['videoId']
		except:
			videoId =''
		
		AddUser = dbhelper.AddData().addUserChatdoubt(mobile,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,date,time)
		db={'message':'Doubt Added',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/get/doubt/answer/',methods=['GET','POST'])
def APiDoubtAnswer():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile= userinfo['mobile']
		topic_data = dbhelper.GetData().getTopicDoubt(mobile)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['mobile']=line[1]
				topic_data_dict['imageUrl']=line[2]
				topic_data_dict['subjectId']=line[3]
				topic_data_dict['doubt']=line[4]
				topic_data_dict['status']=line[5]
				topic_data_dict['subject']=line[6]
				topic_data_dict['createdAt']=str(line[9])
				topic_data_dict['doubtId']=line[10]
				topic_data_dict['date']=line[11]
				topic_data_dict['time']=line[12]
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "doubt_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/education/get/doubt/byid/',methods=['GET','POST'])
def APiDoubtById():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		doubtId= userinfo['doubtId']
		topic_data = dbhelper.GetData().getTopicDoubtId(doubtId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['mobile']=line[1]
				topic_data_dict['imageUrl']=line[2]
				topic_data_dict['subjectId']=line[3]
				topic_data_dict['doubt']=line[4]
				topic_data_dict['status']=line[5]
				topic_data_dict['subject']=line[6]
				topic_data_dict['createdAt']=str(line[9])
				topic_data_dict['doubtId']=line[10]
				topic_data_dict['date']=line[11]
				topic_data_dict['time']=line[12]
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "doubt_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/education/get/free/video/',methods=['GET','POST'])
def APiFreeVideo():
	if request.method=='POST':
		topic_data = dbhelper.GetData().GetFreeVideo()
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['chapterId'] = line[1]
				topic_data_dict['topic'] = line[2]
				topic_data_dict['videoUrl'] = str(line[3])+'?rel=0&amp;modestbranding=1&amp;showinfo=0'
				topic_data_dict['duration'] = line[4]
				topic_data_dict['imageUrl'] = line[5]
				topic_data_dict['docUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "topic_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/subject/topic/',methods=['GET','POST'])
def APiSubjectId():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subjectId= userinfo['subjectId']
		try:
			mobile= userinfo['mobile']
		except:
			mobile=''

		topic_data = dbhelper.GetData().getTopic(subjectId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['subjectId']=line[1]
				topic_data_dict['chapter']=line[2]
				checkStringLst= dbhelper.GetData().GetVideo(line[0])

				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['videoId'] = check[0]
					video_data = dbhelper.GetData().getchapterbook(mobile,line[0])
					try:
						videobook= video_data[0][0]
						check_dict['bookmarkStatus']=1
					except:
						check_dict['bookmarkStatus']=0
					check_dict['chapterId'] = check[1]
					check_dict['topic'] = check[2]
					check_dict['videoUrl'] = str(check[3])+'?autoplay=1;rel=0&amp;modestbranding=1&amp;showinfo=0'
					check_dict['duration'] = check[4]
					check_dict['imageUrl'] = check[5]
					check_dict['docUrl']='https://storage.googleapis.com/courseimage/'+str(check[6])
					checkList.append(check_dict)

				topic_data_dict['videoList']=checkList
				
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "topic_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/answer/report/',methods=['GET','POST'])
def APiAnswerReport():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile= userinfo['mobile']
		examId = userinfo['examId']
		topic_data = dbhelper.GetData().getExamsummary(mobile,examId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['mobile']=line[1]
				topic_data_dict['examId']=line[2]
				topic_data_dict['questionId']=line[3]
				topic_data_dict['answer']=line[4]
				topic_data_dict['correct']=line[5]
				checkStringLst= dbhelper.GetData().GetExamQue(line[3])
				topic_data_dict['question']=checkStringLst[0][1]
				topic_data_dict['optionA']=checkStringLst[0][2]
				topic_data_dict['optionB']=checkStringLst[0][3]
				topic_data_dict['optionC']=checkStringLst[0][4]
				topic_data_dict['optionD']=checkStringLst[0][5]
				topic_data_dict['correctAns']=checkStringLst[0][6]
				topic_data_dict['imageUrl']=checkStringLst[0][8]
				topic_data_dict['description']=checkStringLst[0][9]
				
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "exam_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/exam/details/',methods=['GET','POST'])
def APiExamDetails():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		examId= userinfo['examId']
		mobile= userinfo['mobile']
		topic_data = dbhelper.GetData().getTopic(subjectId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['subjectId']=line[1]
				topic_data_dict['chapter']=line[2]
				checkStringLst= dbhelper.GetData().GetVideo(line[0])

				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['videoId'] = check[1]
					check_dict['chapterId'] = check[1]
					check_dict['topic'] = check[2]
					check_dict['videoUrl'] = str(check[3])+'?rel=0&amp;modestbranding=1&amp;showinfo=0'
					check_dict['duration'] = check[4]
					check_dict['imageUrl'] = 'https://storage.googleapis.com/courseimage/'+str(check[5])
					checkList.append(check_dict)

				topic_data_dict['videoList']=checkList
				
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "topic_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/chapter/video/',methods=['GET','POST'])
def APiChaperVideo():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		chapterId= userinfo['chapterId']
		try:
			mobile= userinfo['mobile']
		except:
			mobile =''
		topic_data = dbhelper.GetData().getchapterVideo(chapterId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				video_data = dbhelper.GetData().getchapterbook(mobile,line[0])
				try:
					videobook= video_data[0][0]
					topic_data_dict['bookmarkStatus']=1
				except:
					topic_data_dict['bookmarkStatus']=0




				topic_data_dict['chapterId']=line[1]
				topic_data_dict['topic']=line[2]
				topic_data_dict['videoUrl']=str(line[3])+'?rel=0&amp;modestbranding=1&amp;showinfo=0'
				topic_data_dict['duration']=line[4]
				topic_data_dict['imageUrl']=line[5]
				topic_data_dict['docUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				topic_data_dict['com_status']=line[8]
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "video_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/chapter/story/',methods=['GET','POST'])
def APichapterstory():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subjectId= userinfo['subjectId']
		topic_data = dbhelper.GetData().getTopic(subjectId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['subjectId']=line[1]
				topic_data_dict['chapter']=line[2]
				checkStringLst= dbhelper.GetData().GetchapterStory(line[0])

				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['chapterId'] = check[1]
					check_dict['defenition'] = check[2]
					check_dict['topic'] = check[8]
					check_dict['topicId'] = check[9]
					check_dict['imageUrl'] = 'https://storage.googleapis.com/courseimage/'+str(check[3])
					checkList.append(check_dict)

				topic_data_dict['storyList']=checkList
				
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "topic_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/chapter/story/new/',methods=['GET','POST'])
def APichapterstorynew():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		chapterId= userinfo['chapterId']
		topicId = userinfo['topicId']
		topic_data = dbhelper.GetData().getchapternew(chapterId,topicId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				
				topic_dict={}
				topic_dict['chapterId'] = line[1]
				topic_dict['defenition'] = line[2]
				if line[3]=='':
					topic_dict['imageUrl']=''
				else:
					topic_dict['imageUrl'] = 'https://storage.googleapis.com/courseimage/'+str(line[3])
				
				topic_data_db.append(topic_dict)
				
		resp = Response(json.dumps({"success": True, "topic_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)		

@app.route('/education/get/subject/concept/new/',methods=['GET','POST'])
def APisubjectconceptnew():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		chapterId= userinfo['chapterId']
		topic_data = dbhelper.GetData().getTopicnew(chapterId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				
				topic_dict={}
				topic_dict['chapterId'] = line[1]
				topic_dict['defenition'] = line[2]
				topic_dict['imageUrl'] = 'https://storage.googleapis.com/courseimage/'+str(line[3])
				
				topic_data_db.append(topic_dict)
				
		resp = Response(json.dumps({"success": True, "topic_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)		

@app.route('/education/get/subject/concept/',methods=['GET','POST'])
def APisubjectconcept():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subjectId= userinfo['subjectId']
		topic_data = dbhelper.GetData().getTopic(subjectId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['subjectId']=line[1]
				topic_data_dict['chapter']=line[2]
				checkStringLst= dbhelper.GetData().Getsubjectconcept(line[0])

				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['conceptId'] = check[1]
					check_dict['chapterId'] = check[1]
					check_dict['definition'] = check[2]
					check_dict['imageUrl'] = 'https://storage.googleapis.com/courseimage/'+str(check[3])
					checkList.append(check_dict)

				topic_data_dict['conceptList']=checkList
				
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "topic_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/subject/chapter/summary/',methods=['GET','POST'])
def APisubjectsummary():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subjectId= userinfo['subjectId']
		topic_data = dbhelper.GetData().getTopic(subjectId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['subjectId']=line[1]
				topic_data_dict['chapter']=line[2]
				checkStringLst= dbhelper.GetData().Getsubjectconcept(line[0])

				checkList=[]
				for check in checkStringLst:
					check_dict={}
					check_dict['chapterId'] = check[1]
					check_dict['definition'] = check[2]
					check_dict['imageUrl'] = 'https://storage.googleapis.com/courseimage/'+str(check[3])
					checkList.append(check_dict)

				topic_data_dict['videoList']=checkList
				checkStringLst1= dbhelper.GetData().GetchapterStory(line[0])

				checkList1=[]
				for check in checkStringLst1:
					check_dict={}
					check_dict['chapterId'] = check[1]
					check_dict['defenition'] = check[2]
					check_dict['imageUrl'] = 'https://storage.googleapis.com/courseimage/'+str(check[3])
					checkList1.append(check_dict)

				topic_data_dict['storyList']=checkList1
				checkStringLst2= dbhelper.GetData().GetVideo(line[0])

				checkList2=[]
				for check in checkStringLst2:
					check_dict={}
					check_dict['chapterId'] = check[1]
					check_dict['topic'] = check[2]
					check_dict['videoUrl'] = str(check[3])+'?rel=0&amp;modestbranding=1&amp;showinfo=0'
					check_dict['duration'] = check[4]
					check_dict['imageUrl'] = 'https://storage.googleapis.com/courseimage/'+str(check[5])
					checkList2.append(check_dict)

				topic_data_dict['conceptList']=checkList2
				
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "topic_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)						


@app.route('/education/add/notes/',methods=['GET','POST'])
def APiUsernotes():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		url=userinfo['url']
		notes=userinfo['notes']
		username=userinfo['username']
		
		AddUser = dbhelper.AddData().addUsernotes(url,notes,username)
		db={'message':'Doubt Added',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/candidate/notice/', methods=['GET','POST'])
def fcmMNotice():

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
				mobile = gcmT[0]
				UpDateConfigure = dbhelper.AddData().AddMessage(mobile,message,titles,dateNow,time)
				# message_data={   "notification":{"action":"Notification","body":message,"title":titles,"imageUrl":"http://s33.postimg.org/slnc2rtwv/logo.png"},


				# "to" : gcmT[0]
				# }
				# form_data = json.dumps(message_data)


				# url='https://fcm.googleapis.com/fcm/send'
				# urlfetch.set_default_fetch_deadline(45)

				# resp = urlfetch.fetch(url=url,
				# 	method=urlfetch.POST,
				# 	payload=form_data,
				# 	headers={"Authorization":"key=AIzaSyCIXNIX9do1ajdKzNHt9TkhIXu7pG9Vb4k", "Content-Type":"application/json"}
				# 	)

			response = Response(json.dumps({"response":{"confirmation": 1}}))
			return after_request(response)

		else:
			response = Response(json.dumps({"response":{"confirmation": 0}}))
			return after_request(response)

@app.route('/education/candidate/notice/byclass/', methods=['GET','POST'])
def fcmMNoticeclass():

	if request.method    == 'POST':
		token_data        =json.loads(request.data)
		# deviceLst         =token_data['deviceLst']
		message           = token_data['message']
		titles           = token_data['titles']
		categoryId = token_data['categoryId']
		dateNow           = str(date.today())
		time              = (datetime.now() + timedelta(hours=05,minutes=30)).strftime("%H:%M")

		fcmTokenList         =dbhelper.GetData().getTokenbyclass(categoryId)
		if len(fcmTokenList)>0:
			for gcmT in fcmTokenList:
				mobile = gcmT[1]
				UpDateConfigure = dbhelper.AddData().AddMessage(mobile,message,titles,dateNow,time)
				# message_data={   "notification":{"action":"Notification","body":message,"title":titles,"imageUrl":"http://s33.postimg.org/slnc2rtwv/logo.png"},


				# "to" : gcmT[0]
				# }
				# form_data = json.dumps(message_data)


				# url='https://fcm.googleapis.com/fcm/send'
				# urlfetch.set_default_fetch_deadline(45)

				# resp = urlfetch.fetch(url=url,
				# 	method=urlfetch.POST,
				# 	payload=form_data,
				# 	headers={"Authorization":"key=AIzaSyCIXNIX9do1ajdKzNHt9TkhIXu7pG9Vb4k", "Content-Type":"application/json"}
				# 	)

			response = Response(json.dumps({"response":{"confirmation": 1}}))
			return after_request(response)

		else:
			response = Response(json.dumps({"response":{"confirmation": 0}}))
			return after_request(response)

@app.route('/education/candidate/notice/byboard/', methods=['GET','POST'])
def fcmMNoticeboard():

	if request.method    == 'POST':
		token_data        =json.loads(request.data)
		# deviceLst         =token_data['deviceLst']
		message           = token_data['message']
		titles           = token_data['titles']
		categoryId = token_data['categoryId']
		subcategoryId = token_data['subcategoryId']
		dateNow           = str(date.today())
		time              = (datetime.now() + timedelta(hours=05,minutes=30)).strftime("%H:%M")

		fcmTokenList         =dbhelper.GetData().getTokenbyclasboard(categoryId,subcategoryId)
		if len(fcmTokenList)>0:
			for gcmT in fcmTokenList:
				mobile = gcmT[0]
				UpDateConfigure = dbhelper.AddData().AddMessage(mobile,message,titles,dateNow,time)
				# message_data={   "notification":{"action":"Notification","body":message,"title":titles,"imageUrl":"http://s33.postimg.org/slnc2rtwv/logo.png"},


				# "to" : gcmT[0]
				# }
				# form_data = json.dumps(message_data)


				# url='https://fcm.googleapis.com/fcm/send'
				# urlfetch.set_default_fetch_deadline(45)

				# resp = urlfetch.fetch(url=url,
				# 	method=urlfetch.POST,
				# 	payload=form_data,
				# 	headers={"Authorization":"key=AIzaSyCIXNIX9do1ajdKzNHt9TkhIXu7pG9Vb4k", "Content-Type":"application/json"}
				# 	)

			response = Response(json.dumps({"response":{"confirmation": 1}}))
			return after_request(response)

		else:
			response = Response(json.dumps({"response":{"confirmation": 0}}))
			return after_request(response)


@app.route('/education/admin/reply/',methods=['GET','POST'])
def APiadminReply():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		mobile=userinfo['mobile']
		doubt=userinfo['doubt']
		status=1
		
		AddUser = dbhelper.AddData().addDoubtReply(mobile,doubt,status)
		db={'message':'Doubt Added',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/update/notes/',methods=['GET','POST'])
def APiupdateUsernotes():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		Id=userinfo['Id']
		url=userinfo['url']
		notes=userinfo['notes']
		username=userinfo['username']
		
		AddUser = dbhelper.UpdateData().Updatenotesdata(Id,url,notes,username)
		db={'message':'Notes Update',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/get/notes/',methods=['GET','POST'])
def APiDoubtnotes():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		username= userinfo['username']
		topic_data = dbhelper.GetData().getTopicnotes(username)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['url']=line[1]
				topic_data_dict['notes']=line[2]
				topic_data_dict['username']=line[3]
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "doubt_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/add/rating/',methods=['GET','POST'])
def APiUserrating():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		username=userinfo['username']
		url=userinfo['url']
		rating=userinfo['rating']
		
		AddUser = dbhelper.AddData().addUserrating(username,url,rating)
		db={'message':'Doubt Added',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/get/rating/',methods=['GET','POST'])
def APiDoubtrating():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		username= userinfo['username']
		topic_data = dbhelper.GetData().getTopicrating(username)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['username']=line[1]
				topic_data_dict['url']=line[2]
				topic_data_dict['rating']=line[3]
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "doubt_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/add/report/',methods=['GET','POST'])
def APiUserreport():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		url=userinfo['url']
		notes=userinfo['notes']
		username=userinfo['username']
		
		AddUser = dbhelper.AddData().addUserreport(url,notes,username)
		db={'message':'Doubt Added',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/get/report/',methods=['GET','POST'])
def APiDoubtreport():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		username= userinfo['username']
		topic_data = dbhelper.GetData().getTopicreport(username)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['url']=line[1]
				topic_data_dict['notes']=line[2]
				topic_data_dict['username']=line[3]
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "doubt_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)	


@app.route('/education/report/get/patient/diseasedetails/',methods=['GET','POST'])
def ApiAgewise():
	if request.method=='POST':
		patientInfo  = json.loads(request.data)
		patientId = patientInfo['patientId']
		doctorId = patientInfo['doctorId']

		app_data = dbhelper.GetData().getPatientdiseasedetails(patientId, doctorId)
		print app_data
		resp = Response(json.dumps({"success": True, "pateint_data": app_data }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)	


# Add Topic

@app.route('/education/add/chapter/topic/',methods=['GET','POST'])
def APiaddchapterTopic():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		print userinfo
		
		
		chapterId=userinfo['chapterId']
		subjectId=userinfo['subjectId']
		categoryId=userinfo['categoryId']
		subcategoryId=userinfo['subcategoryId']
		
		topic=userinfo['topic']
		overview=userinfo['overview'].encode("ascii", "ignore")
		chapterName=userinfo['chapterName']
		
		AddUser = dbhelper.AddData().addchapterTopic(chapterId,subjectId,categoryId,subcategoryId,topic,overview,chapterName)
		db={'message':'Topic Added Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)		


@app.route('/education/add/previous/paper/',methods=['GET','POST'])
def APiPreviousPaper():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subjectId=userinfo['subjectId']
		categoryId=userinfo['categoryId']
		subcategoryId=userinfo['subcategoryId']
		
		documentUrl=userinfo['documentUrl']
		
		
		AddUser = dbhelper.AddData().addUserprevious_Paper(subjectId,categoryId,subcategoryId,documentUrl)
		db={'message':'Topic Added Added',"confirmation":1}
		
		resp = Response(json.dumps({"response":"success"}))
		return after_request(resp)	


@app.route('/education/get/cahpter/topic/',methods=['GET','POST'])
def APiChapterTopic():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		chapterId= userinfo['chapterId']
		topic_data = dbhelper.GetData().getTopicChapter(chapterId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['categoryId']=line[1]
				topic_data_dict['subcategoryId']=line[2]
				topic_data_dict['subjectId']=line[3]
				topic_data_dict['chapterId']=line[4]
				topic_data_dict['chapterName']=line[5]
				topic_data_dict['topic']=line[6]
				topic_data_dict['overview']=line[7]
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "topic_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/education/get/cahpter/previous/paper/',methods=['GET','POST'])
def APiChapterPaper():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subjectId= userinfo['subjectId']
		topic_data = dbhelper.GetData().getTopicChapterPaper(subjectId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['categoryId']=line[2]
				topic_data_dict['subcategoryId']=line[3]
				topic_data_dict['subjectId']=line[1]
				topic_data_dict['documentUrl']=line[4]
				
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "paper_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/education/get/subject/chapter/details/',methods=['GET','POST'])
def APiChaptersubjectSummary():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		subjectId= userinfo['subjectId']
		categoryId = userinfo['categoryId']
		user_data = dbhelper.GetData().getexamcoursecategoryid(categoryId)
		user_data_db=[]
		if(len(user_data))>0:
			for line in user_data:
				user_data_dict={}
				user_data_dict['id']  = line[0]
				user_data_dict['examId']=line[1]
				user_data_dict['name']=line[2]
				user_data_dict['description']=line[3]
				user_data_dict['subCategoryId']=line[4]
				user_data_dict['categoryId']=line[5]
				user_data_dict['imageUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				user_data_dict['chapter']=line[7]
				user_data_dict['overview']=line[9]

				categoryName = dbhelper.GetData().getexamcategorybyid(line[5])
				try:
					user_data_dict['categoryName']=categoryName[0][1]
				except:
					user_data_dict['categoryName']=''
				
				subcategoryName = dbhelper.GetData().getexamSubcategorybyid(line[4])
				try:
					user_data_dict['subcategoryName']=subcategoryName[0][1]
				except:
					user_data_dict['subcategoryName']=''

				checkStringLst= dbhelper.GetData().getexamcoursecategorywithoutoverview(line[0])

				checkList=[]
				for check in checkStringLst:
					check_dict={}
					topic_dict={}
					check_dict['chapterId'] = check[0]
					topic_data = dbhelper.GetData().getTopicChapter(check[0])
					try:
						topic_dict['topic']= topic_data[0][5]
						topic_dict['overview']= topic_data[0][6]
					except:
						topic_dict['topic']= ''
						topic_dict['overview']= ''
					checkList.append(topic_dict)

					check_dict['chapter'] = check[2]
					check_dict['overview'] = check[5]
					checkList.append(check_dict)

				user_data_dict['chapter']=checkList
				
				
				user_data_db.append(user_data_dict)
				
		resp = Response(json.dumps({"success": True, "paper_data": user_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


# edit topic

@app.route('/education/edit/chapter/topic/',methods=['GET','POST'])
def APiEditCapterTopic():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		Id=userinfo['id']
		topic=userinfo['topic']
		overview=userinfo['overview'].replace("'","")
		
		
		EditAssign = dbhelper.UpdateData().UpdateTopic(Id,topic,overview)
		db={'message':'UserDataUpdate',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/education/delete/topic/',methods=['GET','POST'])
def ApiDeleteTopic():
	if request.method=='POST':
		query_data = json.loads(request.data)
		Id = query_data['id']
	   
		update              =dbhelper.DeleteData().DeleteTopic(Id)

		if update:
			db={'message':'Topic Deleted',"confirmation":1}
		else:
			db={'message': 'Topic not Deleted', "confirmation":0}

		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)


# get vido live



@app.route('/education/get/live/chat/',methods=['GET','POST'])
def APiChat():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		videoId=userinfo['videoId']
		topic_data = dbhelper.GetData().getLivechat(videoId)
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['videoId']=line[1]
				topic_data_dict['username']=line[2]
				topic_data_dict['mobile']=line[3]
				topic_data_dict['message']=line[4]
				topic_data_dict['status']=line[5]
				
				
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "topic_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/education/add/live/chat/',methods=['GET','POST'])
def APiAddChat():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		username=userinfo['username']
		message=userinfo['message']
		videoId=userinfo['videoId']
		mobile=userinfo['mobile']
		status= userinfo['status']
		
		
		AddUser = dbhelper.AddData().addUserchat(username,message,videoId,mobile,status)
		db={'message':'Doubt Added',"confirmation":1}
		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/education/get/live/class/',methods=['GET','POST'])
def APiFreeliveVideo():
	if request.method=='POST':
		topic_data = dbhelper.GetData().GetliveclassVideo()
		topic_data_db=[]
		if(len(topic_data))>0:
			for line in topic_data:
				topic_data_dict={}
				topic_data_dict['id']  = line[0]
				topic_data_dict['chapterId'] = line[1]
				topic_data_dict['topic'] = line[2]
				topic_data_dict['videoUrl'] = str(line[3])+'?rel=0&amp;modestbranding=1&amp;showinfo=0'
				topic_data_dict['duration'] = line[4]
				topic_data_dict['imageUrl'] = line[5]
				topic_data_dict['docUrl']='https://storage.googleapis.com/courseimage/'+str(line[6])
				topic_data_db.append(topic_data_dict)
				
		resp = Response(json.dumps({"success": True, "topic_data": topic_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)