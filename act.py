# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import json, urllib2, logging
import cloudDbHandler as dbhelper
# import datetime
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
import actcloudDbHandler as dbhelper
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




@app.route('/act/get/admin/login/',methods=['GET','POST'])
def APigetlogin():
	if request.method=='POST':
		configure_data  = json.loads(request.data)
		email = configure_data['email']
		password  = configure_data['password']
		
		lesson_info_data = dbhelper.GetData().getloginDetails(email,password)
		lesson_info_data_db = []

		if(len(lesson_info_data))>0:
			for line in lesson_info_data:
				lesson_info_data_dict = {}
				lesson_info_data_dict['id']            =line[0]
				lesson_info_data_dict['email']      =line[1]
				lesson_info_data_dict['Password']      =line[2]
				lesson_info_data_dict['name']          =line[3]
				lesson_info_data_dict['status']     =line[4]
				lesson_info_data_dict['mobile']     =line[5]
				lesson_info_data_db.append(lesson_info_data_dict)
				
		
			resp = Response(json.dumps({"success": 1,  "login_data":lesson_info_data_db,"message":"Login Sucessfully"}))
		else:
			resp = Response(json.dumps({"success": 0 ,"message":"Wrong Credentials"}))

		resp.headers['Content-type']='application/json'
		return after_request(resp)
	

			
		resp.headers['Content-type']='application/json'
		return after_request(resp)



@app.route('/act/file/upload/',methods=['GET','POST'])
def apiSeminarUpload2():
	if request.method=='POST':
		print request.files
		file_object = request.files['file']
		
		BUCKET_NAME = 'mtrac-b56ab.appspot.com'
		storage = googleapiclient.discovery.build('storage', 'v1')
		
		print '**',file_object, type(file_object)
		GCS_UPLOAD_FOLDER = 'Act' 
		
		filename = file_object.filename.replace(" ","_")
		file_object.filename=file_object.filename.replace(" ","_")
		string_io_file = StringIO.StringIO(file_object.stream.read())

		fullName = GCS_UPLOAD_FOLDER + '/'+ filename
	
		print fullName
		body = {
			'name': fullName,
		}
		print body
		AddLike = dbhelper.AddData().addLogo(filename)

		
		

		req = storage.objects().insert(bucket=BUCKET_NAME, body=body, media_body=googleapiclient.http.MediaIoBaseUpload(string_io_file, 'image/jpeg'))
		response = req.execute()



		resp = Response(json.dumps({"success": True, "datasets": 'Yahoo',"message":"Logo has been Updated"}))
		return after_request(resp) 

@app.route('/act/audio/upload/',methods=['GET','POST'])
def apiAudioUpload():

	if request.method=='POST':
		print request.files,request
		file_object = request.files['file']
		
		BUCKET_NAME = 'mtrac-b56ab.appspot.com'
		storage = googleapiclient.discovery.build('storage', 'v1')
		
		print '**',file_object, type(file_object)
		GCS_UPLOAD_FOLDER = 'Act' 
		
		filename = file_object.filename.replace(" ","_")
		file_object.filename=file_object.filename.replace(" ","_")
		string_io_file = StringIO.StringIO(file_object.stream.read())

		fullName = GCS_UPLOAD_FOLDER + '/'+ filename
	
		print fullName
		body = {
			'name': fullName,
		}
		print body
	

		
		

		req = storage.objects().insert(bucket=BUCKET_NAME, body=body, media_body=googleapiclient.http.MediaIoBaseUpload(string_io_file, 'audio/mp3'))
		response = req.execute()



		resp = Response(json.dumps({"success": True, "datasets": 'Yahoo',"message":"Audio has been Updated"}))
		return after_request(resp) 

@app.route('/act/get/admin/details/',methods=['GET','POST'])
def APigetadmindetais():
	if request.method=='POST':
		configure_data  = json.loads(request.data)
		email = configure_data['email']
		
		lesson_info_data = dbhelper.GetData().getloginAdminDetails(email)
		lesson_info_data_db = []

		if(len(lesson_info_data))>0:
			for line in lesson_info_data:
				lesson_info_data_dict = {}
				lesson_info_data_dict['id']            =line[0]
				lesson_info_data_dict['email']      =line[1]
				lesson_info_data_dict['Password']      =line[2]
				lesson_info_data_dict['name']          =line[3]
				lesson_info_data_dict['adminType']     =line[4]
				lesson_info_data_db.append(lesson_info_data_dict)
				
		
			resp = Response(json.dumps({"success": 1,  "login_data":lesson_info_data_db,"message":"Login Sucessfully"}))
		else:
			resp = Response(json.dumps({"success": 0 ,"message":"Wrong Credentials"}))

		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/act/get/reported/video/',methods=['GET','POST'])
def APigetreportedvideo():
	if request.method=='POST':
		video_info_data = dbhelper.GetData().getReportedVideo()
		video_info_data_db = []

		if(len(video_info_data))>0:
			for line in video_info_data:
				video_info_data_dict = {}
				video_info_data_dict['id']            =line[0]
				video_info_data_dict['videoId']            =line[1]
				summary_info_data = dbhelper.GetData().getvideo(line[1])
				video_info_data_dict['videoUrl']      =summary_info_data[0][0]
				video_info_data_dict['reportedProfile']      =line[2]
				video_info_data_dict['profileId']      =line[3]
				video_info_data_dict['name']          =line[4]
				print line[5]
				if line[5]!='':
					print "hi"
					video_info_data_dict['image']     =line[5]
				else:
					video_info_data_dict['image']="https://youth-apicalls.appspot.com/media/user.png"
				video_info_data_dict['email']     =line[6]
				video_info_data_dict['mobile']     =line[7]
				if int(line[8])==1:
					video_info_data_dict['blockStatus']     ="Block"
				else:
					video_info_data_dict['blockStatus']     ="UnBlock"

				video_info_data_dict['blockDate']     =line[9]
				video_info_data_db.append(video_info_data_dict)
				
		
		resp = Response(json.dumps({"success": 1,  "video_data":video_info_data_db,"message":"Reported video Sucessfully"}))
		

		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/act/get/admin/summary/',methods=['GET','POST'])
def APigetadminsummary():
	if request.method=='POST':
		summary_info_data = dbhelper.GetData().getAdminSummary()
		summary_info_data_db = []

		if(len(summary_info_data))>0:
			for line in summary_info_data:
				summary_info_data_dict = {}
				summary_info_data_dict['video']            =line[0]
				summary_info_data_dict['user']      =line[1]
				summary_info_data_dict['subadmin']      =line[2]
				summary_info_data_dict['reportedvideo']      =line[3]
				summary_info_data_dict['audio']      =line[4]
				summary_info_data_db.append(summary_info_data_dict)
				
		
			resp = Response(json.dumps({"success": 1,  "summary_data":summary_info_data_db,"message":"Login Sucessfully"}))
		else:
			resp = Response(json.dumps({"success": 0 ,"message":"Wrong Credentials"}))

		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/act/get/child/admin/',methods=['GET','POST'])
def APigetchildadmin():
	if request.method=='POST':
		summary_info_data = dbhelper.GetData().getChildAdmin()
		summary_info_data_db = []

		if(len(summary_info_data))>0:
			for line in summary_info_data:
				summary_info_data_dict = {}
				summary_info_data_dict['id']            =line[0]
				summary_info_data_dict['email']      =line[1]
				summary_info_data_dict['password']      =line[2]
				summary_info_data_dict['name']      =line[3]
				summary_info_data_dict['status']      =line[4]
				summary_info_data_dict['mobile']      =line[5]
				summary_info_data_db.append(summary_info_data_dict)
				
		
			resp = Response(json.dumps({"success": 1,  "summary_data":summary_info_data_db,"message":"Child Admin Details"}))
		else:
			resp = Response(json.dumps({"success": 0 ,"message":"Child Admin"}))

		resp.headers['Content-type']='application/json'
		return after_request(resp)

# create subadmin
@app.route('/act/subadmin/',methods=['GET','POST'])
def subadmin():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile = userinfo['mobile']
		name = userinfo['name']
		email= userinfo['email']
		password= userinfo['password']
		status =0
		
		UserStatus  = dbhelper.GetData().checkSubadminstatus(email)
		
		if UserStatus==True:
			db={'message':'User Already Exist',"confirmation":0}
		else:
			
			AddSubadmin = dbhelper.AddData().addSubadmin(mobile,name,email,password,status)
			db={'message':'User added',"confirmation":1}
			
		resp = Response(json.dumps({"success": db}))
		return after_request(resp)
		

@app.route('/act/followup/',methods=['GET','POST'])
def followup():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		profileId = userinfo['profileId']
		followupId= userinfo['followupId']
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			UserStatus  = dbhelper.GetData().checkFollowstatus(profileId,followupId)
			print UserStatus	
			
			if UserStatus==True:
				update  =dbhelper.DeleteData().deletefollowup(profileId,followupId)
				try:
					follower =dbhelper.GetData().checkFollower(followupId)[0][0]
				except:
					follower = 0
				
				db={'message':'User Unfollow You',"confirmation":0,"followers":follower}
			else:
				
				AddSubadmin = dbhelper.AddData().addFollowup(profileId,followupId)
				try:
					follower =dbhelper.GetData().checkFollower(followupId)[0][0]
				except:
					follower = 0
				db={'message':'You have follow user',"confirmation":1,"followers":follower}
				
			resp = Response(json.dumps(db))
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps(db))
			return after_request(resp)
	

# signup
@app.route('/act/signup/',methods=['GET','POST'])
def singup():
	if request.method=='POST':
		userinfo   = json.loads(request.data)
		mobile = userinfo['mobile']
		userType = "public"
		print mobile
		name = userinfo['name'].replace(' ','-')
		email= userinfo['email']
		password= userinfo['password']
		isActor = userinfo['isActor']
		try:
			image = userinfo['image']
		except:
			image =''
		if email !='':
			UserStatus  = dbhelper.GetData().checkUserstatus2(email)

		else:
			UserStatus  = dbhelper.GetData().checkUserstatus(mobile)
		
		print UserStatus
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			if UserStatus==True:
				db={'message':'User Already Exist',"confirmation":0}
			else:
				lastId =dbhelper.GetData().getUserLastId()[0][0]
				if lastId:
					newid=str(123+lastId)
				else:
					newid=str(123)
			
				
				profileId = name +newid
				Adduser = dbhelper.AddData().adduser(mobile,name,email,password,profileId,isActor,image,userType)
				user = {"mobile":mobile, "name":name, "email":email,"profileId":profileId,"image":image}
				db={'message':'User added',"confirmation":1,"user":user}
				
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)


# login

@app.route('/act/login/',methods=['GET','POST'])
def ApiLogin():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		username = configure_data['username']
		password = configure_data['password']
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			user_status =dbhelper.GetData().checkUser(username)
			if user_status==True:
				login_info_data = dbhelper.GetData().Postlogin(username)
				login_info_data_db = []
				if(len(login_info_data))>0:
					for line in login_info_data:
						login_info_data_dict = {}
						login_info_data_dict['id'] =line[0]
						login_info_data_dict['email'] =line[1]
						login_info_data_dict['mobile']=line[2]
						login_info_data_dict['password']=line[3]
						login_info_data_dict['profileId']=line[4]
						login_info_data_dict['name']=line[5]
						login_info_data_dict['image']=line[6]
						login_info_data_dict['isActor']=line[7]
						login_info_data_dict['userType']=line[8]

						login_info_data_db.append(login_info_data_dict)
				if password=='':
					resp = Response(json.dumps({"success": 1,"message":"User Exist", "datasets":login_info_data_db}))
				else:

					if(password==login_info_data[0][3]):
						resp = Response(json.dumps({"success": 1,"message":"User Exist", "datasets":login_info_data_db}))
					else:
						resp = Response(json.dumps({"success": 0,"message":"Wrong Password",}))
			else:
				resp = Response(json.dumps({"success": 2,"message":"User Not Exist",}))
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)


# forget password

@app.route('/act/forget/password/',methods=['GET','POST'])
def ApiForgotPassword():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		username = configure_data['username']
		password = configure_data['password']
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			EditAssign = dbhelper.UpdateData().UpdatePassword(username,password)
			db={'message':'Password has been Updated',"confirmation":1}
		else:
			db={'message':'Unauthorized Access',"confirmation":0}

		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/act/admin/forget/password/',methods=['GET','POST'])
def ApiadminForgotPassword():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		username = configure_data['username']
		password = configure_data['password']
		
		EditAssign = dbhelper.UpdateData().UpdateadminPassword(username,password)
		db={'message':'Password has been Updated',"confirmation":1}
		

		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

# user auth
@app.route('/act/checkUser/',methods=['GET','POST'])
def ApicheckUser():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		username = configure_data['username']
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			user_status =dbhelper.GetData().checkUser(username)
			if user_status==True:
				
				resp = Response(json.dumps({"success": 1,"message":"User Exist",}))
			else:
				otp = random.randint(1000,9999)
				text =" Welcome+to+ elearning.+ Your +Login+ OTP + is + %s."%(str(otp))
				url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=INOBIN&mobile=%s&msg=%s'%(str(username),text)
				urlfetch.set_default_fetch_deadline(45)
				resp = urlfetch.fetch(url=url,
					method=urlfetch.GET,
					headers={'Content-Type': 'text/html'})

				# mailhandler.sendMail().sendDetails(username,text)
				resp = Response(json.dumps({"success": 2,"message":"User Not Exist","otp":otp}))
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)

# user exist
@app.route('/act/checkUser/exist/',methods=['GET','POST'])
def ApicheckUserexist():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		username = configure_data['username']
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			user_status =dbhelper.GetData().checkUser(username)
			if user_status==True:
				otp = random.randint(1000,9999)
				text =" Welcome+to+ elearning.+ Your +Login+ OTP + is + %s."%(str(otp))
				url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=INOBIN&mobile=%s&msg=%s'%(str(username),text)
				urlfetch.set_default_fetch_deadline(45)
				resp = urlfetch.fetch(url=url,
					method=urlfetch.GET,
					headers={'Content-Type': 'text/html'})
				
				resp = Response(json.dumps({"success": 1,"message":"User Exist","otp":otp}))
			else:
				
				resp = Response(json.dumps({"success": 2,"message":"User Not Exist"}))
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)

# video
@app.route('/act/video/',methods=['GET','POST'])
def ApiVideo():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		username = configure_data['username']
		videoType = configure_data['Type']
		print username,videoType
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			if videoType=='For you':
				video_status =dbhelper.GetData().video()
				video_status_db = []
				if(len(video_status))>0:
					for line in video_status:
						video_status_dict = {}
						video_status_dict['id'] =line[0]
						video_status_dict['profileId'] =line[1]
						video_status_dict['liked']=line[2]
						video_status_dict['comment']=line[3]
						video_status_dict['description']=line[4]
						video_status_dict['video']=line[5]
						video_status_dict['image']=line[7]
						video_status_dict['tags']=line[8]
						video_liked =dbhelper.GetData().videolikeed(username,line[0])
						video_status_dict['isLiked']=video_liked
						video_follow =dbhelper.GetData().checkFollowstatus(username,line[1])
						if video_follow	== True:
							video_status_dict['followstatus'] =1
						else:
							video_status_dict['followstatus'] =1

						

						video_status_db.append(video_status_dict)
			else:
				video_status =dbhelper.GetData().videofollows(username)
				video_status_db = []
				if(len(video_status))>0:
					for line in video_status:
						video_status_dict = {}
						video_status_dict['id'] =line[0]
						video_status_dict['profileId'] =line[1]
						video_status_dict['liked']=line[2]
						video_status_dict['comment']=line[3]
						video_status_dict['description']=line[4]
						video_status_dict['video']=line[5]
						video_status_dict['image']=line[7]
						video_status_dict['tags']=line[8]
						video_liked =dbhelper.GetData().videolikeed(username,line[0])
						video_status_dict['isLiked']=video_liked
						video_follow =dbhelper.GetData().checkFollowstatus(username,line[1])
						if video_follow	== True:
							video_status_dict['followstatus'] =1
						else:
							video_status_dict['followstatus'] =1

						

						video_status_db.append(video_status_dict)


			resp = Response(json.dumps({"success": 1,"message":"Video List", "video":video_status_db}))
			
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)


@app.route('/act/like/video/',methods=['GET','POST'])
def Apilikevideo():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		username = configure_data['username']
		videoId = configure_data['videoId']
		like = configure_data['like']
		message = str(username)+'has liked on your video'
		videoList =dbhelper.GetData().profileId(videoId)
		profileId = videoList[0][0]
		
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			if like==True:
				AddLike = dbhelper.AddData().addLike(username,videoId,message,profileId)
				videoList =dbhelper.GetData().profileId(videoId)
				profileId = videoList[0][0]
				liked = videoList[0][1]
				comment	 = videoList[0][2]
			else:
				update  =dbhelper.DeleteData().deleteVideo(username,videoId)
				videoList =dbhelper.GetData().profileId(videoId)
				profileId = videoList[0][0]
				liked = videoList[0][1]
				comment	 = videoList[0][2]
			db={'message':'like has been Updated',"confirmation":1,"TotalLiked":liked,"Totalcomment":comment}
		else:
			db={'message':'Unauthorized Access',"confirmation":0}

		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/act/comment/video/',methods=['GET','POST'])
def Apicommentvideo():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		username = configure_data['username']
		videoId = configure_data['videoId']
		videoUrl = configure_data['videoUrl']
		comment = configure_data['comment']
		profileId =dbhelper.GetData().profileId(videoId)[0][0]
		message = str(username)+'has commented on your video'
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			AddComment = dbhelper.AddData().addComment(username,videoId,videoUrl,comment,message,profileId)
			db={'message':'comment has been Updated',"confirmation":1}
		else:
			db={'message':'Unauthorized Access',"confirmation":0}

		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/act/reported/video/',methods=['GET','POST'])
def ApiReportedvideo():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		videoId = configure_data['videoId']
		profileId = configure_data['profileId']
		message = configure_data['message']
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			AddComment = dbhelper.AddData().addReportedVideo(videoId,profileId,message)
			db={'message':'Report on Video has been Submit',"confirmation":1}
		else:
			db={'message':'Unauthorized Access',"confirmation":0}

		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/act/add/video/',methods=['GET','POST'])
def Apiaddvideo():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		profileId = configure_data['profileId']
		description = configure_data['description']
		videoUrl = configure_data['videoUrl']
		image = configure_data['image']
		tags = configure_data['tags']

		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			AddComment = dbhelper.AddData().addVideo(profileId,description,videoUrl,image,tags)
			db={'message':'video has been Updated',"confirmation":1}
		else:
			db={'message':'Unauthorized Access',"confirmation":0}

		resp = Response(json.dumps({"response": db}))
		return after_request(resp)


@app.route('/act/get/like/',methods=['GET','POST'])
def ApigetLike():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		videoId = configure_data['videoId']
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			video_status =dbhelper.GetData().videolike(videoId)
			video_status_db = []
			if(len(video_status))>0:
				for line in video_status:
					video_status_dict = {}
					video_status_dict['id'] =line[0]
					video_status_dict['videoId'] =line[1]
					video_status_dict['videoUrl']=line[2]
					video_status_dict['username']=line[3]
					video_status_dict['createdAt']=str(line[4])
					
					

					video_status_db.append(video_status_dict)

			resp = Response(json.dumps({"success": 1,"message":"Video like List", "video":video_status_db}))
			
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)

@app.route('/act/get/audio/',methods=['GET','POST'])
def ApigetAudio():
	if request.method=='POST':
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			audio_status =dbhelper.GetData().GetAudio()
			audio_status_db = []
			if(len(audio_status))>0:
				for line in audio_status:
					audio_status_dict = {}
					audio_status_dict['id'] =line[0]
					audio_status_dict['audio'] ='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Act/'+str(line[1])
					audio_status_dict['name']=line[2]
					audio_status_dict['description']=line[3]
					audio_status_dict['createdAt']=str(line[4])
					audio_status_db.append(audio_status_dict)

			resp = Response(json.dumps({"success": 1,"message":"Aduio List", "audio":audio_status_db}))
			
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)

@app.route('/act/logo/',methods=['GET','POST'])
def ApigetLogo():
	if request.method=='POST':
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			logo_status =dbhelper.GetData().GetLogo()
			logo_status_db = []
			if(len(logo_status))>0:
				for line in logo_status:
					logo_status_dict = {}
					logo_status_dict['image'] ='https://storage.googleapis.com/mtrac-b56ab.appspot.com/Act/'+str(line[1])
					
					logo_status_db.append(logo_status_dict)

			resp = Response(json.dumps({"success": 1,"message":"Aduio List", "Logo":logo_status_db}))
			
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)



@app.route('/act/get/comment/',methods=['GET','POST'])
def ApigetComment():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		videoId = configure_data['videoId']
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			video_status =dbhelper.GetData().videoComment(videoId)
			video_status_db = []
			if(len(video_status))>0:
				for line in video_status:
					video_status_dict = {}
					video_status_dict['id'] =line[0]
					video_status_dict['username']=line[1]
					userprofile =dbhelper.GetData().userprofile(line[1])
					try:
						video_status_dict['image'] =userprofile[0][0]
					except:
						video_status_dict['image'] ='http://youth-apicalls.appspot.com/media/user.png'

					video_status_dict['videoId'] =line[2]
					video_status_dict['videoUrl']=line[3]
					video_status_dict['comment']=line[4]
					
					video_status_dict['createdAt']=str(line[5])
					
					

					video_status_db.append(video_status_dict)

			resp = Response(json.dumps({"success": 1,"message":"Video comment List", "comment":video_status_db}))
			
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)






@app.route('/act/upload/profile/',methods=['GET','POST'])
def ApiUploadProfile():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		Id = configure_data['id']
		image = configure_data['image']
		name = configure_data['name']
		password = configure_data['password']
		userType = configure_data['userType']
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			UpdateProfile = dbhelper.UpdateData().UpdateProfile(Id,name,image,password,userType)
			db={'message':'Profile has been Updated',"confirmation":1}
		else:
			db={'message':'Unauthorized Access',"confirmation":0}

		resp = Response(json.dumps({"response": db}))
		return after_request(resp)

@app.route('/act/deletesubadmin/',methods=['GET','POST','DELETE'])
def ApiDeleteDepartment():
	if request.method=='DELETE':
		print 'data', request.data
		did= request.args.get('did')
		deleteDepartment = dbhelper.DeleteData().deleteDepartment(did)
		if deleteDepartment:
			db={'message':'Subadmin Deleted'}
			success = 1
		else:
			db={'message': 'Subadmin could not be deleted'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

@app.route('/act/admin/block/',methods=['GET','POST'])
def Apiblock():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		profileId = configure_data['profileId']
		block = configure_data['block']
		if block=='7Days':
			tod = datetime.now()
			dateNow           = str(date.today())
			time              = (datetime.now() + timedelta(days=7))
			blockDate = time
			blockStatus=1
			print(blockDate)
		elif block=='14Days':
			dateNow           = str(date.today())
			time              = (datetime.now() + timedelta(days=14))
			blockDate = time
			blockStatus=1
			print(blockDate)
		elif block=='30Days':
			dateNow           = str(date.today())
			time              = (datetime.now() + timedelta(days=30))
			blockDate = time
			blockStatus=1
			print(blockDate)
		elif block=='unblock':
			blockDate = ''
			blockStatus=0
		else:
			blockDate=''
			blockStatus=0
		
		
		UpdateProfile = dbhelper.UpdateData().UpdateBlock(profileId,blockDate,blockStatus)
		if blockDate=='':
			db={'message':'',"confirmation":1}
		else:
			db={'message':'Profile has been Updated',"confirmation":1}
		

		resp = Response(json.dumps({"success": 1,"datasets": db}))
		return after_request(resp)

@app.route('/act/admin/audio/',methods=['GET','POST'])
def ApiAdminAudio():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		audio = configure_data['filname'].replace(" ","_")
		description = configure_data['description']
		name = configure_data['audioname']
		AddAudio = dbhelper.AddData().addAudio(audio,description,name)
		db={'message':'Audio has been Updated',"confirmation":1}
		

		resp = Response(json.dumps({"response": db}))
		return after_request(resp)
		
		

# notification

@app.route('/act/get/notification/',methods=['GET','POST'])
def ApigetNotification():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		profileId = configure_data['profileId']
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			video_status =dbhelper.GetData().getNotification(profileId)
			video_status_db = []
			if(len(video_status))>0:
				for line in video_status:
					video_status_dict = {}
					video_status_dict['id'] =line[0]
					video_status_dict['username'] =line[1]
					video_status_dict['videoId']=line[2]
					video_status_dict['notification']=line[3]
					
					video_status_db.append(video_status_dict)

			resp = Response(json.dumps({"success": 1,"message":"Notification List", "notification":video_status_db}))
			
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)


@app.route('/act/get/userlist/',methods=['GET','POST'])
def Apigetuserlist():
	if request.method=='POST':
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			user_status =dbhelper.GetData().getUserlist()
			user_status_db = []
			if(len(user_status))>0:
				for line in user_status:
					user_status_dict = {}
					user_status_dict['id'] =line[0]
					user_status_dict['email'] =line[1]
					user_status_dict['mobile']=line[2]
					user_status_dict['password']=line[3]
					user_status_dict['profileId']=line[4]
					user_status_dict['name']=line[5]
					user_status_dict['image']=line[6]
					user_status_dict['isActor']=line[7]
					
					user_status_db.append(user_status_dict)

			trending_list =dbhelper.GetData().getTrendingVideo()
			trending_list_db = []
			if(len(trending_list))>0:
				for line in trending_list:
					trending_list_dict = {}
					trending_list_dict['id'] =line[0]
					trending_list_dict['profileId'] =line[1]
					trending_list_dict['liked'] =line[2]
					trending_list_dict['comment'] =line[3]
					trending_list_dict['description'] =line[4]
					trending_list_dict['videoUrl'] =line[5]
					trending_list_dict['image'] =line[7]
					trending_list_dict['tag'] =line[8]
					
					trending_list_db.append(trending_list_dict)

			resp = Response(json.dumps({"success": 1,"message":"User List", "userList":user_status_db,"trending_list":trending_list_db}))
			
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)

@app.route('/act/get/taglist/',methods=['GET','POST'])
def Apigettaglist():
	if request.method=='POST':
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			trending_list =dbhelper.GetData().getTrendingVideo()
			trending_list_db = []
			if(len(trending_list))>0:
				for line in trending_list:
					trending_list_dict = {}
					trending_list_dict['tag'] =line[8]
					
					
					trending_list_db.append(trending_list_dict)

			resp = Response(json.dumps({"message":"Tag List","trending_list":trending_list_db}))
			
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)


@app.route('/act/user/video/',methods=['GET','POST'])
def ApiUserVideo():
	if request.method=='POST':
		configure_data = json.loads(request.data)
		profileId = configure_data['profileId']
		username = configure_data['username']
		headers = request.headers
		auth = headers.get("api-Key")
		if auth == 'NkHb13BxRBiZ0JSyxLbAU':
			video_status =dbhelper.GetData().uservideoList(username)
			video_status_db = []
			video_list_db =[]
			if(len(video_status))>0:
				for line in video_status:
					video_status_dict = {}
					video_status_dict['email'] =line[0]
					video_status_dict['mobile'] =line[1]
					video_status_dict['profileId'] =line[2]
					video_status_dict['name']=line[3]
					video_status_dict['image']=line[3]
					video_status_dict['isActor']=line[4]
					video_follower =dbhelper.GetData().checkFollower(username)
					video_status_dict['follower']=video_follower[0][0]
					video_follow =dbhelper.GetData().checkFollowstatus(profileId,username)
					print video_follow
					if video_follow	== True:
						video_status_dict['followstatus'] =1
						
					else:
						video_status_dict['followstatus'] =0
						
					video_status_db.append(video_status_dict)

			video_list =dbhelper.GetData().uservideoListData(username)
			if(len(video_list))>0:
				for line in video_list:
					video_list_dict = {}
					video_list_dict['id'] =line[0]
					video_list_dict['profileId'] =line[1]
					video_list_dict['liked']=line[2]
					video_list_dict['comment']=line[3]
					video_list_dict['description']=line[4]
					video_list_dict['video']=line[5]
					video_list_dict['image']=line[7]
					video_list_dict['tags']=line[8]
					video_liked =dbhelper.GetData().videolikeed(profileId,line[0])
					video_list_dict['isLiked']=video_liked
					video_follow =dbhelper.GetData().checkFollowstatus(profileId,username)
					if video_follow	== True:
						video_list_dict['followstatus'] =1
					else:
						video_list_dict['followstatus'] =0
					video_list_db.append(video_list_dict)

			resp = Response(json.dumps({"success": 1,"message":"User Video List", "user":video_status_dict,"video":video_list_db}))
			
			resp.headers['Content-type']='application/json'
			return after_request(resp)
		else:
			db={'message':'Unauthorized Access',"confirmation":0}
			resp = Response(json.dumps({"success": db}))
			return after_request(resp)

@app.route('/act/admin/user/',methods=['GET','POST'])
def ApiAdminUser():
	if request.method=='GET':
		profileId = request.args.get('profileId')
		video_status =dbhelper.GetData().uservideoList(profileId)
		video_status_db = []
		video_list_db =[]
		if(len(video_status))>0:
			for line in video_status:
				video_status_dict = {}
				video_status_dict['email'] =line[0]
				video_status_dict['mobile'] =line[1]
				video_status_dict['profileId'] =line[2]
				video_status_dict['name']=line[3]
				video_status_dict['image']=line[3]
				video_status_dict['isActor']=line[4]
				video_status_db.append(video_status_dict)	

		resp = Response(json.dumps({"success": 1,"message":"User  List", "user":video_status_dict}))
		
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/act/check/phone/', methods=['GET','POST'])
def ApiCheckPhone():
	if request.method=='POST':
		userInfo  = json.loads(request.data)
		phone = userInfo['phone']
		checkPhone = dbhelper.GetData().checkPhone(phone)
		print ('checkphone='+str(checkPhone))
		if (str(checkPhone)=='0'):
			db={'message':'Phone Invalid'}
			success = 0
		elif (str(checkPhone)=='1'):
			db={'message': 'Phone Valid'}
			success = 1
		else:
			db={'message':'Phone Invalid'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

@app.route('/act/otp-generator/',methods=['GET','POST'])
def ApiOtpGenerator():
	if request.method=='GET':
		otp = random.randint(0,9999)
		print otp

		resp = Response(json.dumps({"success": True, "security":otp }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/act/phone-verification/',methods=['GET','POST'])
def ApiPhoneVerification():
	if request.method=='POST':
		details=json.loads(request.data)
		print request.data
		#text=details['text']
		phone=details['phone']
		otp=details['otp']

		text =" Welcome+to+ elearning.+ Your +Login+ OTP is %s."%(str(otp))
		url ='https://sms.cell24x7.com:2029/mspProducerM/sendSMS?user=harshit&pwd=harshit&sender=INOBIN&mobile=%s&msg=%s'%(str(phone),text)
		print url
		urlfetch.set_default_fetch_deadline(45)
		resp = urlfetch.fetch(url=url,
			method=urlfetch.GET,
			headers={'Content-Type': 'text/html'})
		resp = Response(json.dumps({"success": True }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

		

@app.route('/act/check/email/', methods=['GET','POST'])
def ApiCheckEmail():
	if request.method=='POST':
		userInfo  = json.loads(request.data)
		email = userInfo['email']
		checkPhone = dbhelper.GetData().checkEmail(email)
		print ('checkphone='+str(checkPhone))
		if (str(checkPhone)=='0'):
			db={'message':'Email Invalid'}
			success = 0
		elif (str(checkPhone)=='1'):
			db={'message': 'Email Valid'}
			success = 1
		else:
			db={'message':'Email Invalid'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)
		


@app.route('/act/update/admin/password/',methods=['GET','POST'])
def APiAddUser():
	if request.method=='POST':
		userInfo  = json.loads(request.data)
		email   = userInfo['email']
		password  = userInfo['password']
		EditAssign = dbhelper.UpdateData().UpdateadminPassword(email,password)
		resp = Response(json.dumps({"success": 1,"message":"success"}))
		
		resp.headers['Content-type']='application/json'
		return after_request(resp)