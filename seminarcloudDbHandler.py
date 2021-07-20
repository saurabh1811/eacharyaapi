import os

from google.appengine.api import memcache
from google.appengine.api import rdbms
from datetime import datetime
import time
import MySQLdb
from datetime import date, timedelta


_INSTANCE_NAME_GEN = 'apidata-data:us-central1:apidata-us'
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'admin@123'



def connect_to_cloudsql(dbname):

	# When deployed to App Engine, the `SERVER_SOFTWARE` environment variable will be set to 'Google App Engine/version'.
	if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
		# Connect using the unix socket located at /cloudsql/cloudsql-connection-name.
		cloudsql_unix_socket = os.path.join('/cloudsql', _INSTANCE_NAME_GEN)

		db = MySQLdb.connect( unix_socket=cloudsql_unix_socket, user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db=dbname)

	# If the unix socket is unavailable, then try to connect using TCP. This will work if you're running a local MySQL server or using the Cloud SQL proxy, for example: cloud_sql_proxy -instances=your-connection-name=tcp:3306
	else:
		db = MySQLdb.connect(
			host='104.197.51.91',  user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db=dbname)

	return db


def connect_to_cloudsql_hindi(dbname):

	# When deployed to App Engine, the `SERVER_SOFTWARE` environment variable will be set to 'Google App Engine/version'.
	if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
		# Connect using the unix socket located at /cloudsql/cloudsql-connection-name.
		cloudsql_unix_socket = os.path.join('/cloudsql', _INSTANCE_NAME_GEN)

		db = MySQLdb.connect( unix_socket=cloudsql_unix_socket, user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db=dbname, charset='utf8', use_unicode=True)

	# If the unix socket is unavailable, then try to connect using TCP. This will work if you're running a local MySQL server or using the Cloud SQL proxy, for example: cloud_sql_proxy -instances=your-connection-name=tcp:3306
	else:
		db = MySQLdb.connect(
			host='104.197.51.91',  user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db=dbname, charset='utf8', use_unicode=True)

	return db



class AddData():
	
	


	

	def addUser(self,name,email,mobile,dob,designation1,designation2,designation3,designation4,designationYear1,designationYear2,designationYear3,designationYear4,qualification1,qualification2,qualification3,qualificationYear1,qualificationYear2,qualificationYear3,qualificationYear4,qualification4,affiliations1,affiliations2,affiliations3,affiliations4,gender,imageName,registrationNo):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO login (name,email,mobile,dob,designation1,designation2,designation3,designation4,designationYear1,designationYear2,designationYear3,designationYear4,qualification1,qualification2,qualification3,qualificationYear1,qualificationYear2,qualificationYear3,qualificationYear4,qualification4,affiliations1,affiliations2,affiliations3,affiliations4,gender,imageName,registrationNo) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(name,email,mobile,dob,designation1,designation2,designation3,designation4,designationYear1,designationYear2,designationYear3,designationYear4,qualification1,qualification2,qualification3,qualificationYear1,qualificationYear2,qualificationYear3,qualificationYear4,qualification4,affiliations1,affiliations2,affiliations3,affiliations4,gender,imageName,registrationNo)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addAgenda(self,sessionName,topic,tTime,time,speaker,chairperson,hall,seminarId,date,time2,time3,time4,userId,topicId):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO seminarSessional (sessionName,topic,tTime,time,speaker,chairPerson,hall,seminarId,date,time2,time3,time4,userId,topicId) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(sessionName,topic,tTime,time,speaker,chairperson,hall,seminarId,date,time2,time3,time4,userId,topicId)
			cursor.execute(_sqlc_)
			_sqlc = "INSERT INTO lecturer_information (seminarId,name,designation,userId) VALUES ('%s','%s','%s','%s')"%(seminarId,speaker,'speaker',userId)
			cursor.execute(_sqlc)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addAttendance(self,mobile,seminarId,name,dateNow,current_time):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO attendance (mobile,seminarId,name,date,time) VALUES ('%s','%s','%s','%s','%s')"%(mobile,seminarId,name,dateNow,current_time)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserlist(self,seminarName,seminarDate,location,seminarCode,mobile,image,email,endDate,userId):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO seminar_list (seminarName,seminarDate,location,seminarCode,mobile,image,email,endDate,userId) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(seminarName,seminarDate,location,seminarCode,mobile,image,email,endDate,userId)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserRating(self,mobile,rating,comment,seminarCode,topicId,overAllExperience,conferenceInterest,mostInterestedTopic,mostBoringTopic,mostInformativeTopic,sessionShouldShorter,whowasBestPresenter,likeToatrendAgain,wasAppUseful):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO rating (mobile,rating,comment,seminarId,topicId,overAllExperience,conferenceInterest,mostInterestedTopic,mostBoringTopic,mostInformativeTopic,sessionShouldShorter,whowasBestPresenter,likeToatrendAgain,wasAppUseful) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(mobile,rating,comment,seminarCode,topicId,overAllExperience,conferenceInterest,mostInterestedTopic,mostBoringTopic,mostInformativeTopic,sessionShouldShorter,whowasBestPresenter,likeToatrendAgain,wasAppUseful)
			cursor.execute(_sqlc_)

			_sqlc =_sqlc_ = "INSERT INTO point_calculation(mobile,seminarId, seminarFeedback) VALUES ('%s','%s',%s) on Duplicate Key update seminarFeedback= seminarFeedback + %s "%(mobile,seminarCode, 10, 10)
			
			print _sqlc
			cursor.execute(_sqlc)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserlistB(self,seminarId,mobile,questionId,answer):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO pooling_answer (seminarId,mobile,questionId,answer) VALUES ('%s','%s','%s','%s')"%(seminarId,mobile,questionId,answer)
			cursor.execute(_sqlc_)
			_sqlc="INSERT INTO points (seminarId,mobile,question,answer,pointType,points) VALUES ('%s','%s','%s','%s','%s','%s')"%(seminarId,mobile,questionId,answer,'Multiple',10)
			print _sqlc
			cursor.execute(_sqlc)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)		

	def addaskquestion(self,name,mobile,question,code,date,time,imageName):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO ask_question (name,mobile,question,code,date,time,imageName) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(name,mobile,question,code,date,time,imageName)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addSeminarAdvert(self,message,seminarId,seminarName,imageName):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO image_notice (message,seminarId,seminarName,imageName) VALUES ('%s','%s','%s','%s')"%(message,seminarId,seminarName,imageName)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addMessage(self,topic,message,seminarId):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO notice (topic,message,seminarId) VALUES ('%s','%s','%s')"%(topic,message,seminarId)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addToken(self,mobile,fcmToken):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO `token` (`mobile`,`fcmToken`) VALUES ( '%s', '%s') ON DUPLICATE KEY update fcmToken='%s'"%(mobile,fcmToken,fcmToken)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def addDocument(self,seminarId,documentType,image,name,description,userId):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO document (seminarId,documentType,image,name,description,userId) VALUES ('%s','%s','%s','%s','%s','%s')"%(seminarId,documentType,image,name,description,userId)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addDocumentImage(self,seminarId,image1,image2,image3,image4,image5,image6,image7):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO picture (seminarId,image1,image2,image3,image4,image5,image6,image7) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(seminarId,image1,image2,image3,image4,image5,image6,image7)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)			

	def addSeminarCode(self,mobile,seminarId,code,imageName):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO seminar_data (mobile,seminarId,code,imageName) VALUES ('%s','%s','%s','%s')"%(mobile,seminarId,code,imageName)
			cursor.execute(_sqlc_)
			# _sqlc = "INSERT INTO assign_survey (username,state,district,block,school,surveyId) VALUES ('%s','%s','%s','%s','%s','%s')"%(username,state,district,block,school,surveyId)
			# cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)	


	def addPayment(self,name,address,seminarCode,date,amount,status,mobile,seminarId):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO payment (name,address,seminarCode,date,amount,status,mobile,seminarId) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(name,address,seminarCode,date,amount,status,mobile,seminarId)
			cursor.execute(_sqlc_)
			_sqlc_ = "INSERT INTO seminar_data (mobile,seminarId,code) VALUES ('%s','%s','%s')"%(mobile,seminarId,seminarCode)
			cursor.execute(_sqlc_)
			# sqlcmd="UPDATE payment SET name='%s',address='%s',seminarCode='%s',date='%s',amount='%s',status='%s' where mobile='%s'"%(name,address,seminarCode,date,amount,status,mobile)
			# cursor.execute(sqlcmd)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addQuestion(self,seminarId,questionId,question,option1,option2,option3,option4,questionType,userId):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO pooling (seminarId,questionId,question,option1,option2,option3,option4,questionType,userId) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(seminarId,questionId,question,option1,option2,option3,option4,questionType,userId)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addQuizResp(self,mobile,seminarId,questionId,answer,correct):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO QuizResp (mobile,seminarId,questionId,answer,correct) VALUES ('%s','%s','%s','%s','%s')"%(mobile,seminarId,questionId,answer,correct)
			cursor.execute(_sqlc_)
			_sqlc_ = "INSERT INTO pooling_answer (seminarId,mobile,questionId,answer) VALUES ('%s','%s','%s','%s')"%(seminarId,mobile,questionId,answer)
			cursor.execute(_sqlc_)
			
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addPointQuizPoint(self,mobile,seminarId, correctA):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO point_calculation(mobile,seminarId, correctA) VALUES ('%s','%s',%s) on Duplicate Key update correctA= correctA + %s "%(mobile,seminarId, correctA, correctA)
			cursor.execute(_sqlc_)
			
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addSessionFeedPoint(self,mobile,seminarId, sessionFeedback):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO point_calculation(mobile,seminarId, sessionFeedback) VALUES ('%s','%s',%s) on Duplicate Key update sessionFeedback= sessionFeedback + %s "%(mobile,seminarId, sessionFeedback, sessionFeedback)
			cursor.execute(_sqlc_)
			
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)


	def addPointAcceptedoint(self,mobile,seminarId, acceptedQ):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO point_calculation(mobile,seminarId, acceptedQ) VALUES ('%s','%s',%s) on Duplicate Key update acceptedQ= acceptedQ + %s "%(mobile,seminarId, acceptedQ, acceptedQ)
			cursor.execute(_sqlc_)
			
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addRegistrationDocument(self,seminarId,image,userId):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO registrationForm(seminarId,imageName,userId) VALUES ('%s','%s','%s')"%(seminarId,image,userId)
			cursor.execute(_sqlc_)
			
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addPointLivePollPoint(self,mobile,seminarId, livePoll):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO point_calculation(mobile,seminarId, livePoll) VALUES ('%s','%s',%s) on Duplicate Key update livePoll= livePoll + %s "%(mobile,seminarId, livePoll, livePoll)
			cursor.execute(_sqlc_)
			
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addQuizPoint(self,mobile,seminarId,questionId,answer,correct):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO points (mobile,seminarId,question,answer,pointType,points) VALUES ('%s','%s','%s','%s','%s','%s')"%(mobile,seminarId,questionId,answer,'Quiz',10)
			cursor.execute(_sqlc_)
			
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addQuestion2(self,seminarId,questionId,question,option1,option2,option3,option4,questionType,correct,imageName,userId):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO pooling (seminarId,questionId,question,option1,option2,option3,option4,questionType,correctAnswer,imageName,userId) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(seminarId,questionId,question,option1,option2,option3,option4,questionType,correct,imageName,userId)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)


	def addComment(self,mobile,seminarId,topicId,rating,comment):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO seminar_comment (mobile,seminarId,topicId,rating,comment) VALUES ('%s','%s','%s','%s','%s')"%(mobile,seminarId,topicId,rating,comment)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addseminar_data(self,mobile,seminarId,code):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO seminar_data (mobile,seminarId,code) VALUES ('%s','%s','%s')"%(mobile,seminarId,code)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserhelp(self,mobile,email,seminarCode,userId):
		try:
			dbname = 'seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO help (mobile,email,seminarId,userId) VALUES ('%s','%s','%s','%s')"%(mobile,email,seminarCode,userId)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)		

	
	

		#######################################################################################################
					   
class GetData():

	def getTotalPoints(self,mobile, seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "select mobile, acceptedQ + correctA + livePoll + sessionFeedback + seminarFeedback as ss from point_calculation where mobile='%s' and seminarId='%s'" %(mobile, seminarId)
			
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getFeedbackagenda(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT mobile,seminar_comment.topicId,rating,sessionName,seminar_comment.comment FROM seminar.seminar_comment LEFT JOIN seminarSessional ON seminar_comment.topicId=seminarSessional.topicId where  seminar_comment.seminarId='%s'" %(seminarId)
			
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getQuestionInfo(self, Id):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "select * from ask_question where id=%s" %(Id)
			
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getfinalpayment(self, mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * from payment where mobile =%s" %(mobile)
			
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		

	def getUserStatus(self,mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "select * from login where mobile=%s" %(mobile)
			
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			print (len(dbDetails))
			if len(dbDetails)>0:
				return True
			else:
				return False 
		except Exception,e:
			print str(e)


	def getoverallfeedback(self,seminarId,mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "select * from rating where seminarId='%s' and mobile='%s'" %(seminarId,mobile)
			
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			print (len(dbDetails))
			if len(dbDetails)>0:
				return True
			else:
				return False 
		except Exception,e:
			print str(e)


	def getUserRegisterStatus(self,seminarId,mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "select * from seminar_data where seminarId='%s' and mobile='%s'" %(seminarId,mobile)
			
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			print (len(dbDetails))
			if len(dbDetails)>0:
				return True
			else:
				return False 
		except Exception,e:
			print str(e)



	def getsessionfeedback(self,seminarId,mobile,topicId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "select * from seminar_comment where seminarId='%s' and mobile='%s' and topicId='%s'" %(seminarId,mobile,topicId)
			
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			print (len(dbDetails))
			if len(dbDetails)>0:
				return True
			else:
				return False 
		except Exception,e:
			print str(e)
		

	def getSemainarverify(self,seminarId,code):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM seminar.seminar_list where id='%s' and seminarCode='%s'" %(seminarId,code)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			print (len(dbDetails))
			if len(dbDetails)>0:
				return True
			else:
				return False 
		except Exception,e:
			print str(e)


	def getDocsDocument(self,seminarId,documentType):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM seminar.document where seminarId='%s' and documentType='%s'" %(seminarId,documentType)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			print (len(dbDetails))
			if len(dbDetails)>0:
				return True
			else:
				return False 
		except Exception,e:
			print str(e)

	def getDocsImages(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM seminar.picture where seminarId='%s'" %(seminarId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			print (len(dbDetails))
			if len(dbDetails)>0:
				return True
			else:
				return False 
		except Exception,e:
			print str(e)

	def getPoolStatus(self,seminarId,pollId,mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM seminar.pooling_answer where  questionId='%s' and mobile='%s'" %(pollId,mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			print (len(dbDetails))
			if len(dbDetails)>0:
				return 1
			else:
				return 0 
		except Exception,e:
			print str(e)

	def getDatalist(self):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM seminar_list"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getAdminlist(self,userId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM seminar_list where userId='%s'"%(userId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getSeminarRegister(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM seminar_data where seminarId='%s'"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getpaymentbySeminar(self,mobile,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT name,mobile FROM payment where mobile='%s' and seminarId='%s'"%(mobile,seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getSeminarStatusData(self,mobile,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT status FROM payment where mobile='%s' and seminarId='%s'"%(mobile,seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetName(self,mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT name FROM login where mobile='%s'"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetSessionSeminar(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT location,seminarDate FROM seminar_list where id='%s'"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetAttendanceStatus(self,mobile,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM attendance where mobile='%s' and seminarId='%s'"%(mobile,seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetSessionListTotal(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM seminarSessional where seminarId='%s'"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	# def getRegistrationForm(self,seminarId):
	# 	try:
	# 		dbname='seminar'
	# 		conn = connect_to_cloudsql(dbname)
	# 		cursor = conn.cursor()
	# 		_sqlcmd_ ="SELECT * FROM registrationForm where seminarId='%s'"%(seminarId)
	# 		cursor.execute(_sqlcmd_)
	# 		dbDetails=[]
	# 		dbDetails = cursor.fetchall()
	# 		print dbDetails
	# 		conn.commit()
	# 		conn.close()
	# 		return dbDetails
	# 	except Exception,e:
	# 		print str(e)

	def getDocs(self):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM document"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getPollDate(self):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT id,activeAt FROM seminar.pooling where status=1;"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getranklist(self,mobile,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM user_rank where mobile='%s' and seminarId='%s'" %(mobile,seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getQuizAnswer(self,mobile,questionId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			print _sqlcmd_
			_sqlcmd_ ="SELECT answer,questionStatus FROM QuizResp where mobile='%s' and questionId='%s'" %(mobile,questionId)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getBrocher(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT image FROM document where seminarId='%s' and documentType='Brocher'" %(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getRegistrationForm(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT id,imageName FROM registrationForm where seminarId='%s' order by id desc limit 1" %(seminarId)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getRegistrationForm2(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM registrationForm where seminarId='%s' order by id desc limit 1" %(seminarId)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def APiGetPart(self,mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT count(distinct(seminarId)) FROM seminar.seminar_data where mobile='%s'" %(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def APiUserName(self,mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT name FROM seminar.login where mobile='%s'" %(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def APiGetPointRule(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM document where seminarId='%s' and documentType='UploadRules'" %(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getNotice(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM notice where  seminarId='%s' order by id desc" %(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)	


	def getseminarhelp(self,seminarCode):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM help where  seminarId='%s'" %(seminarCode)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getseminarCode(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT seminarCode FROM seminar_list where  id='%s'" %(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)	

	def getDatalistB(self):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM pooling_answer"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getQuestionType(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT questionId, questionType FROM pooling where seminarId='%s' and status=1"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getQusetionpool(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM pooling where seminarId='%s'"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getQuizQues(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM pooling where seminarId='%s' and questionType='QUIZ' and status=1"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getLastIDNew(self):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT max(id) FROM pooling;"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 

	def getSeminatRanking(self, seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT name, mobile, sum(points) as points FROM seminar.ask_question where code='%s' group by mobile order by points desc "%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getSeminatSum(self, seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT count(distinct(mobile)) FROM seminar.seminar_data where seminarId='%s'"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getUserDetails(self, mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM seminar.seminar_data where mobile='%s'"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getSeminatPart(self, seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT count(distinct(mobile)) FROM seminar.point_calculation where seminarId='%s'"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)



	def getSeminatCount(self,mobile, seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT mobile,count(question),sum(points) FROM seminar.ask_question where mobile='%s' and code='%s' group by mobile"%(mobile, seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def GetSessionList(self,seminarId, hall, date):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT sessionName,time,chairPerson FROM seminarSessional where seminarId='%s' and hall='%s' and date='%s'"%(seminarId,hall,date)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def SessionDetails(self,sessionName,hall,date):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM seminarSessional where sessionName='%s' and hall='%s' and date='%s'"%(sessionName,hall,date)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getPartnerLastID(self):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT max(id) FROM seminarSessional;"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getSelectedque(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT count(question) FROM seminar.ask_question where  code='%s'  and status=1"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)



	def getSeminarName(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT seminarName FROM seminar.seminar_list where id='%s'"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getAgendaImage(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM seminar.agenda where seminarId='%s' group by seminarId"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getRating(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM seminar.rating where seminarId='%s'"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getLecturer(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM lecturer_information where seminarId='%s'"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getAgenda(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM seminarSessional where seminarId='%s'"%(seminarId)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getSeminaruser(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT distinct(seminar_data.mobile),login.name,login.imageName,login.email FROM seminar.seminar_data LEFT JOIN login ON seminar_data.mobile=login.mobile where seminarId='%s'"%(seminarId)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)




	def getSponser(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM document where seminarId='%s' and documentType='SponserList'"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getSminarCode(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT seminarCode FROM seminar_list where id='%s'"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getSeminarTopic(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM seminarSessional where seminarId='%s'"%(seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)	

	def getUserName(self,mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT name FROM login where mobile='%s'"%(mobile)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getasklist(self,code):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM  ask_question where code='%s'" %(code)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTotalPoint(self,mobile,code):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT sum(points) FROM  point_calculation where mobile='%s' AND seminarId='%s'" %(mobile,code)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getPointlist(self,code):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM  point_calculation where seminarId='%s'" %(code)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getuserdeatisl(self,mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM  login where mobile='%s'" %(mobile)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getuserdea(self):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM  login "
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getasklistAll(self,code):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM  ask_question where code='%s' and status=1" %(code)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getpool(self,seminarId,questionId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM  pooling where seminarId='%s' and questionId='%s'" %(seminarId,questionId)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getQuestionLivePool(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT questionId,option1,option2,option3,option4,question FROM seminar.pooling where seminarId='%s' and status=1 and questionType='MULTIPLE'" %(seminarId)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getQuestionPool(self,questionId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT questionId,option1,option2,option3,option4,question FROM seminar.pooling where questionId='%s'" %(questionId)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getQueLivePool(self,seminarId,pollId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT questionId,option1,option2,option3,option4,question FROM seminar.pooling where seminarId='%s' and questionId='%s'" %(seminarId,pollId)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getQuestionLivePool2(self,questionId,option1,option2,option3,option4):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT(SELECT count(*) From pooling_answer where questionId='%s' and answer like '%%%s%%')AS opt1,(SELECT count(*) From pooling_answer where questionId='%s' and answer like '%%%s%%')AS opt2,(SELECT count(*) From pooling_answer where questionId='%s' and answer like '%%%s%%')AS opt3,(SELECT count(*) From pooling_answer where questionId='%s' and answer like '%%%s%%')AS opt4" %(questionId,option1,questionId,option2,questionId,option3,questionId,option4)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getSminarUserData(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT(SELECT count(distinct(mobile)) FROM seminar.seminar_data where seminarId='%s')AS Total,(SELECT count(distinct(mobile)) FROM seminar.attendance where seminarId='%s')AS Present" %(seminarId,seminarId)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTotalPointDivide(self,mobile,code):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT(SELECT sum(points) From point_calculation where mobile='%s' and pointType ='ActiveQuestion' and seminarId='%s')AS opt1,(SELECT sum(points) From point_calculation where mobile='%s' and pointType ='Multiple' and seminarId='%s')AS opt2,(SELECT sum(points) From point_calculation where mobile='%s' and pointType ='Quiz' and seminarId='%s')AS opt3,(SELECT sum(points) From point_calculation where mobile='%s' and pointType ='FEEDBACK' and seminarId='%s')AS opt4" %(mobile,code,mobile,code,mobile,code)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getCountVote(self,seminarId,questionId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT count(id) FROM  pooling where seminarId='%s' and questionId='%s'" %(seminarId,questionId)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getQuestionPoll(self):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT * FROM  pooling"
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)			

	def getLastId(self):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT max(id) FROM seminar_list"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		

	
	

	def getUserLoginStatusNew(self,mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM login where mobile='%s'"%(mobile)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)	


	def getToken(self,seminarId):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			
			sqlcmd = "SELECT * FROM seminar.token where mobile  in (select distinct(mobile) from seminar_data where seminarId='%s')"%(seminarId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)													 


	

	
			 
			  
		

	

	
	

class UpdateData():
	
	##################################### END #################################################
	def UpdateUserData(self,mobile,domicile_document,documentUrl,dob,gender,maritalStatus,category,disability,profile_image,khasi_read,khasi_write,khasi_speak,garo_read,garo_write,garo_speak,english_read,english_write,english_speak,hindi_read,hindi_write,hindi_speak,other_read,other_write,other_speak,higher_education,passing_year,training,employed,work_experience,employment_prefer,work_outside,expectedSalary,short_training,notice_period,address,houseNo,landmark,city,state,pincode,status,trainingType,specialization,trainingDate,trainingDuration,completionDate,willingState,willingCity,course,health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others,pQualification,pCourse,pPassingYear, image_url,registration_code):
		# try:
		dbname='play_school'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE user_basic SET domicile_document='%s',documentUrl='%s',dob='%s',gender='%s',maritalStatus='%s',category='%s',disability='%s',profile_image='%s',khasi_read='%s',khasi_write='%s',khasi_speak='%s',garo_read='%s',garo_write='%s',garo_speak='%s',english_read='%s',english_write='%s',english_speak='%s',hindi_read='%s',hindi_write='%s',hindi_speak='%s',other_read='%s',other_write='%s',other_speak='%s',higher_education='%s',passing_year='%s',training='%s',employed='%s',work_experience='%s',employment_prefer='%s',work_outside='%s',expectedSalary='%s',short_training='%s',notice_period='%s',address='%s',houseNo='%s',landmark='%s',city='%s',state='%s',pincode='%s',status='%s',trainingType='%s',specialization='%s',trainingDate='%s',trainingDuration='%s',completionDate='%s',willingState='%s',willingCity='%s',course='%s',health='%s',hospitality='%s',tourism='%s',it='%s',retail='%s',manufacturing='%s',food='%s',construction='%s',education='%s',banking='%s',others='%s',pQualification='%s',pCourse='%s',pPassingYear='%s', image_url='%s', registrationId='%s',formStatus=1 where mobile='%s'"%(domicile_document,documentUrl,dob,gender,maritalStatus,category,disability,profile_image,khasi_read,khasi_write,khasi_speak,garo_read,garo_write,garo_speak,english_read,english_write,english_speak,hindi_read,hindi_write,hindi_speak,other_read,other_write,other_speak,higher_education,passing_year,training,employed,work_experience,employment_prefer,work_outside,expectedSalary,short_training,notice_period,address,houseNo,landmark,city,state,pincode,status,trainingType,specialization,trainingDate,trainingDuration,completionDate,willingState,willingCity,course,health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others,pQualification,pCourse,pPassingYear,image_url,registration_code, mobile)
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	def Updateuserdata(self,mobile,	designation1,	designation2,	designation3,	designation4,	qualification1,	qualification2,	qualification3,	qualification4,	qualificationYear1,	qualificationYear2,	qualificationYear3,	qualificationYear4,	affiliations1,	affiliations2,	affiliations3,	affiliations4,	designationYear1,	designationYear2,	designationYear3,	designationYear4):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE login SET designation1='%s',	designation2='%s',	designation3='%s',	designation4='%s',	qualification1='%s',	qualification2='%s',	qualification3='%s',	qualification4='%s',	qualificationYear1='%s',	qualificationYear2='%s',	qualificationYear3='%s',	qualificationYear4='%s',	affiliations1='%s',	affiliations2='%s',	affiliations3='%s',	affiliations4='%s',	designationYear1='%s',	designationYear2='%s',	designationYear3='%s',	designationYear4='%s' where mobile='%s'"%(designation1,	designation2,	designation3,	designation4,	qualification1,	qualification2,	qualification3,	qualification4,	qualificationYear1,	qualificationYear2,	qualificationYear3,	qualificationYear4,	affiliations1,	affiliations2,	affiliations3,	affiliations4,	designationYear1,	designationYear2,	designationYear3,	designationYear4, mobile)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updatepayment(self,name,address,seminarCode,date,amount,status,mobile):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE payment SET name='%s',address='%s',seminarCode='%s',date='%s',amount='%s',status='%s' where mobile='%s'"%(name,address,seminarCode,date,amount,status,mobile)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid				

	def updateInPoll(self,Id):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE pooling SET status=0 where id='%s'"%(Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	def updateInACPoll(self,Id):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE pooling SET status=0 where id='%s'"%(Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	def updateLockPoll(self,Id):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE pooling SET seminar_status=1 where id='%s'"%(Id)
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	def updateunLockPoll(self,Id):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE pooling SET seminar_status=0 where id='%s'"%(Id)
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	def updateActQue(self,Id):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE ask_question SET status=1,points=10 where id='%s'"%(Id)
		cursor.execute(sqlcmd)
		print sqlcmd
		
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	def updateDeQue(self,Id):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE ask_question SET status=0 where id='%s'"%(Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	def updateDocs(self,seminarId,documentType,image,name,description,userId):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE document SET image='%s',name='%s',description='%s',userId='%s' where seminarId='%s' and documentType='%s'"%(image,name,description,userId,seminarId,documentType)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	def updateDocsImages(self,seminarId,image1,image2,image3,image4,image5,image6,image7):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE picture SET image1='%s',image2='%s',image3='%s',image4='%s',image5='%s',image6='%s',image7='%s' where seminarId='%s'"%(image1,image2,image3,image4,image5,image6,image7,seminarId)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	def updatePoll(self,Id,now):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE pooling SET status=1,activeAt='%s' where id='%s'"%(now,Id)
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	def updatePoll2(self,Id,now):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE pooling SET status=0,activeAt='%s' where id='%s'"%(now,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	def updateProfileImage(self,mobile,imageName):
		# try:
		dbname='seminar'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE login SET imageName='%s' where mobile='%s'"%(imageName,mobile)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	
	
	

	

class DeleteData():

	def deleteToken(self,mobile):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM token WHERE mobile="%s"'%(mobile)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def deleteSession(self,Id):
		try:
			dbname='seminar'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM seminarSessional WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	
