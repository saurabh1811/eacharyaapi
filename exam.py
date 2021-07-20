# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import json, urllib2, logging
import datetime
import json
import StringIO

import mailhandler
import random
from math import radians, cos, sin, asin, sqrt
import math
import ast
from time import gmtime, strftime
from sets import  Set
import unicodedata
import urllib
import urllib2
from datetime import date, timedelta
import examcloudDbHandler as dbhelper
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



	

# signup
@app.route('/exam/signup/',methods=['GET','POST'])
def singup():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile = userinfo['mobile']
		name = userinfo['name']
		email= userinfo['email']
		password= userinfo['password']
		
		UserStatus  = dbhelper.GetData().checkUserstatus(email)

		if UserStatus==True:
			db={'message':'User Already Exist',"confirmation":0}
		else:
			Adduser = dbhelper.AddData().adduser(name,mobile,email,password)
			db={'message':'User added',"confirmation":1}
			
		resp = Response(json.dumps({"success": db}))
		return after_request(resp)

@app.route('/exam/get/exam/',methods=['GET','POST'])
def APigetExam():
	if request.method=='POST':
		exam_data = dbhelper.GetData().getexamData()
		exam_data_db = []

		if(len(exam_data))>0:
			for line in exam_data:
				exam_data_dict = {}
				exam_data_dict['id']            =line[0]
				exam_data_dict['examName']      =line[1]
				exam_data_dict['overview']      =line[2]
								
				exam_data_db.append(exam_data_dict)
		
			resp = Response(json.dumps({"success": 1,  "examData":exam_data_db}))
		else:
			resp = Response(json.dumps({"success": 0}))
			
		resp.headers['Content-type']='application/json'
		return after_request(resp)
		

@app.route('/exam/check/candidate/auth/', methods=['GET','POST'])
def AddCheckStatus():
	if request.method       == 'POST':
		user_data   =json.loads(request.data)
		email  = user_data['email']
		password = user_data['password']	
		UserStatus  = dbhelper.GetData().checkUserstatus(email)
		if UserStatus== True:
			user_data = dbhelper.GetData().getloginnew(email)
			name=user_data[0][1]
			mobile=user_data[0][2]
			email=user_data[0][3]
			password=user_data[0][4]
			if password==user_data[0][4]:
				db={'message':'User Already Exist',"confirmation":1,"name":name,"mobile":mobile,"email":email}
			else:
				db={'message':'Wrong Password',"confirmation":2}

		else:
			db={'message':'User Not Exist', "confirmation":0}


		resp = Response(json.dumps({ "response": db}))
		return after_request(resp)

@app.route('/exam/get/question/exam/',methods=['GET','POST'])
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

@app.route('/exam/add/question/summary/',methods=['GET','POST'])
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
			print user_data
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

@app.route('/exam/get/test/rank/',methods=['GET','POST'])
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

@app.route('/exam/get/answer/report/',methods=['GET','POST'])
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

