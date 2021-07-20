import os

from google.appengine.api import memcache
from google.appengine.api import rdbms
from datetime import datetime
import time
import MySQLdb
from datetime import date, timedelta


_INSTANCE_NAME_GEN = 'smart-howl-286211:us-central1:eeachariya'
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'admin'



def connect_to_cloudsql(dbname):

	# When deployed to App Engine, the `SERVER_SOFTWARE` environment variable will be set to 'Google App Engine/version'.
	if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
		# Connect using the unix socket located at /cloudsql/cloudsql-connection-name.
		cloudsql_unix_socket = os.path.join('/cloudsql', _INSTANCE_NAME_GEN)

		db = MySQLdb.connect( unix_socket=cloudsql_unix_socket, user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db=dbname)

	# If the unix socket is unavailable, then try to connect using TCP. This will work if you're running a local MySQL server or using the Cloud SQL proxy, for example: cloud_sql_proxy -instances=your-connection-name=tcp:3306
	else:
		db = MySQLdb.connect(
			host='34.70.246.54',  user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, db=dbname)

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
	
	

	def addclasselearningstudent(self,mobile,name,email,invite_code,referalCode):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO student_register (mobile,name,email,inviteCode,referalCode) VALUES ('%s','%s','%s','%s','%s')"%(mobile,name,email,invite_code,referalCode)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	
	def addToken(self,mobile,fcmToken):
		try:
			dbname = 'elearning'
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

	def addUserregister(self,mobile,name,email,inviteCode,className,city,school,boardName,preparingForExam):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO student_register (mobile,name,email,inviteCode,className,city,school,boardName,preparingForExam) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(mobile,name,email,inviteCode,className,city,school,boardName,preparingForExam)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUsercontact(self,name,mobile,email,pinCode,feedback):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO contact_us (name,mobile,email,pinCode,feedback) VALUES ('%s','%s','%s','%s','%s')"%(name,mobile,email,pinCode,feedback)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserprevious_Paper(self,subjectId,categoryId,subcategoryId,documentUrl):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO previous_paper (subjectId,categoryId,subcategoryId,documentUrl) VALUES ('%s','%s','%s','%s')"%(subjectId,categoryId,subcategoryId,documentUrl)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUsertestseries(self,imageUrl,examName,noOfSeat,noOfQuestion,marks,subjectList):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO testSeries (imageUrl,examName,noOfSeat,noOfQuestion,marks,subjectList,status) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(imageUrl,examName,noOfSeat,noOfQuestion,marks,subjectList,1)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserliveclasses(self,chapterId,subjectId,categoryId,subcategoryId,topic,videoUrl,imageUrl,document,com_status,duration):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO chapterVideo (chapterId,subjectId,categoryId,subcategoryId,topic,videoUrl,imageUrl,documentUrl,com_status,duration) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(chapterId,subjectId,categoryId,subcategoryId,topic,videoUrl,imageUrl,document,com_status,duration)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserliveclassessubject(self,chapterId,definition,imageUrl,categoryId,subcategoryId,subjectId,topic):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO subjectConcept (chapterId,definition,imageUrl,categoryId,subcategoryId,subjectId,topic) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(chapterId,definition,imageUrl,categoryId,subcategoryId,subjectId,topic)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserliveclassesstory(self,chapterId,definition,imageUrl,categoryId,subcategoryId,subjectId,topic,topicId,overview):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO chapterStory (chapterId,definition,imageUrl,categoryId,subcategoryId,subjectId,topic,topicId,overview) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(chapterId,definition,imageUrl,categoryId,subcategoryId,subjectId,topic,topicId,overview)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)				

	def addUserchapterVideo(self,chapterId,topic,videoUrl,duration,imageUrl):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO chapterVideo (chapterId,topic,videoUrl,duration,imageUrl) VALUES ('%s','%s','%s','%s','%s')"%(chapterId,topic,videoUrl,duration,imageUrl)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)		

	def addUsercategory(self,name,description,createdBy):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO masterCategory (name,description,createdBy) VALUES ('%s','%s','%s')"%(name,description,createdBy)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUsersubcategory(self,name,description,createdBy,categoryId):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO subCategory (name,description,createdBy,categoryId) VALUES ('%s','%s','%s','%s')"%(name,description,createdBy,categoryId)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserlastcategory(self,name,description,createdBy,subCategoryId,categoryId,overview):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO category (name,description,createdBy,subCategoryId,categoryId,overview) VALUES ('%s','%s','%s','%s','%s','%s')"%(name,description,createdBy,subCategoryId,categoryId,overview)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUsercorsecategory(self,name,description,subCategoryId,categoryId,imageUrl,chapter,overview):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO courseMaster (name,description,subCategoryId,categoryId,imageUrl,chapter,overview) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(name,description,subCategoryId,categoryId,imageUrl,chapter,overview)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUsercorsecategoryexamdetails(self,field,eligibility,subjects,applicants,qualified,questionsType,paperPattern,colleges,difficultyLevel,prepareTime,whens,examId):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO examDetails (field,eligibility,subjects,applicants,qualified,questionsType,paperPattern,colleges,difficultyLevel,prepareTime,whens) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(field,eligibility,subjects,applicants,qualified,questionsType,paperPattern,colleges,difficultyLevel,prepareTime,whens,examId)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)		

	def addDoubtReply(self,mobile,status,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,replyBy):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO doubtchat (mobile,status,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,replyBy) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(mobile,status,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,replyBy)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def AddMessage(self,mobile,message,titles,dateNow,time):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO notification (mobile,message,titles,dateNow,time) VALUES ( '%s', '%s','%s', '%s','%s')"%(mobile,message,titles,dateNow,time)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserdoubt(self,mobile,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,date,time):
	# try:
		dbname = 'elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO doubt (mobile,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,date,time) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(mobile,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,date,time)
		print _sqlc_
		cursor.execute(_sqlc_)
		_sqlc = "INSERT INTO doubtchat (mobile,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,date,time) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(mobile,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,date,time)
		print _sqlc
		cursor.execute(_sqlc)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid 
	# except Exception,e:
	# 	print str(e)

	def addUserChatdoubt(self,mobile,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,date,time):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc = "INSERT INTO doubtchat (mobile,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,date,time) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(mobile,subjectId,subject,doubt,imageUrl,videoUrl,videoId,doubtId,date,time)
			print _sqlc
			cursor.execute(_sqlc)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserrating(self,username,url,rating):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO rating (username,url,rating) VALUES ('%s','%s','%s')"%(username,url,rating)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUsernotes(self,url,notes,username):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO notes (url,notes,username) VALUES ('%s','%s','%s')"%(url,notes,username)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserreport(self,url,notes,username):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO report (url,notes,username) VALUES ('%s','%s','%s')"%(url,notes,username)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)
	def addUserreportcomments(self,videoId,comments,likes,dislikes,name,commentDate):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO comment (videoId,comments,likes,dislikes,name,commentDate) VALUES ('%s','%s','%s','%s','%s','%s')"%(videoId,comments,likes,dislikes,name,commentDate)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUsereply(self,commentId,reply):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO reply (commentId,reply) VALUES ('%s','%s')"%(commentId,reply)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)										

	def addUsersubject(self,examId,name,description,sourceId,categoryId,subCategoryId):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO subjectMaster (examId,name,description,sourceId,categoryId,subCategoryId) VALUES ('%s','%s','%s','%s','%s','%s')"%(examId,name,description,sourceId,categoryId,subCategoryId)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)


	def addUsersubjectChapter(self,subjectId,subCategoryId,categoryId,chapter,imageUrl):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO topicMaster (subjectId,subCategoryId,categoryId,chapter,imageUrl) VALUES ('%s','%s','%s','%s','%s')"%(subjectId,subCategoryId,categoryId,chapter,imageUrl)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)								

	def addUserexamnew(self,title,description,categoryId,createdBy,duration):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO exam (title,description,categoryId,createdBy,duration) VALUES ('%s','%s','%s','%s','%s')"%(title,description,categoryId,createdBy,duration)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserexamquestion(self,questionType,question,optionA,optionB,optionC,optionD,correctAns,examId):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO questionList (questionType,question,optionA,optionB,optionC,optionD,correctAns,examId) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(questionType,question,optionA,optionB,optionC,optionD,correctAns,examId)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserexamque(self,examId,totalQuestion,attempted,correctAns,wrongAns,examTime,categoryId,mobile):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO examHistory (examId,totalQuestion,attempted,correctAns,wrongAns,examTime,categoryId,mobile) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(examId,totalQuestion,attempted,correctAns,wrongAns,examTime,categoryId,mobile)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addFeedback(self,username,url,feedback):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO feedback (username,url,feedback) VALUES ('%s','%s','%s')"%(username,url,feedback)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addTecaherVideo(self,chapterId,imageUrl,videoUrl,documentUrl,duration,createdBy,topic):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = 'INSERT INTO chapterVideo (chapterId,imageUrl,videoUrl,documentUrl,duration,createdBy,topic) VALUES ("%s","%s","%s","%s","%s","%s","%s")'%(chapterId,imageUrl,videoUrl,documentUrl,duration,createdBy,topic)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUsersummary(self,mobile,examId,questionId,answer,correct,marks,negativeMarks):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO examSummary (mobile,examId,questionId,answer,correct,marks,negativeMarks) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(mobile,examId,questionId,answer,correct,marks,negativeMarks)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)										

	def addUserquestionlist(self,question,optionA,optionB,optionC,optionD,correctAns,imageUrl,examId,description,marks,negativeMarks):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO questionList (question,optionA,optionB,optionC,optionD,correctAns,imageUrl,examId,description,marks,negativeMarks) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(question,optionA,optionB,optionC,optionD,correctAns,imageUrl,examId,description,marks,negativeMarks)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserquestionExcel(self,question,optionA,optionB,optionC,optionD,correctAns,description,createdBy,examId,marks,negativeMarks):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO questionList (question,optionA,optionB,optionC,optionD,correctAns,description,createdBy,examId,marks,negativeMarks) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(question,optionA,optionB,optionC,optionD,correctAns,description,createdBy,examId,marks,negativeMarks)
			print _sqlc_
			cursor.execute(_sqlc_)
			sqlcmd="UPDATE exam SET status=1 where id='%s'"%(examId)
			print sqlcmd
				
			cursor.execute(sqlcmd)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def AddComplain(self,mobile,category,subcategory,complain,name,complainId):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO candidate_complain (mobile,category,subcategory,complain,name,complainId) VALUES ('%s','%s','%s','%s','%s','%s')"%(mobile,category,subcategory,complain,name,complainId)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserquestionbookmark(self,question,optionA,optionB,optionC,optionD,correctAns,setNo,mobile):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO bookmarkQuestion (question,optionA,optionB,optionC,optionD,correctAns,setNo,mobile) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(question,optionA,optionB,optionC,optionD,correctAns,setNo,mobile)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserlivebookmark(self,bookmarkType,name,url,username,status,videoId):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO bookmarkLive(bookmarkType,name,url,username,status,videoId) VALUES ('%s','%s','%s','%s','%s','%s')"%(bookmarkType,name,url,username,status,videoId)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)		

	def addUsersubjectlist(self,className,boardName):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO subjectList (className,boardName) VALUES ('%s','%s')"%(className,boardName)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addteacherdetails(self,teacherName,schoolCode,subject,phone_no,email,password,status,image):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO teacher_details (teacherName,schoolCode,subject,phone_no,email,password,status,image) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(teacherName,schoolCode,subject,phone_no,email,password,status,image)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)		

	def addpricing(self,price,className,year,advancePlan,ultimatePlan,masterPlan):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO pricing (price,className,year,advancePlan,ultimatePlan,masterPlan) VALUES ('%s','%s','%s','%s','%s','%s')"%(price,className,year,advancePlan,ultimatePlan,masterPlan)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addchapterTopic(self,chapterId,subjectId,categoryId,subcategoryId,topic,overview,chapterName):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = 'INSERT INTO chapter_topic (chapterId,subjectId,categoryId,subcategoryId,topic,overview,chapterName) VALUES ("%s","%s","%s","%s","%s","%s","%s")'%(chapterId,subjectId,categoryId,subcategoryId,topic,overview,chapterName)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserchat(self,username,message,videoId,mobile,status):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = 'INSERT INTO liveChat (username,message,videoId,mobile,status) VALUES ("%s","%s","%s","%s","%s")'%(username,message,videoId,mobile,status)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def adduserlogin(self,mobile,name,email,inviteCode,className,city,school,boardName,preparingForExam):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO student_register (mobile,name,email,inviteCode,className,city,school,boardName,preparingForExam) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(mobile,name,email,inviteCode,className,city,school,boardName,preparingForExam)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)								

	def addrecommended(self,imageUrl,title,date,time,videoUrl,description,subjectName):
		try:
			dbname = 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO recommendedVideos (imageUrl,title,date,time,videoUrl,description,subjectName) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(imageUrl,title,date,time,videoUrl,description,subjectName)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)														

	

		#######################################################################################################
					   
class GetData():

	def getCandidateAuthStatus(self,mobile):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * from student_register where mobile='%s'" %str(mobile)
			
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

	def getcomplainList(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM subcatogroy where cateogryId='%s'"%(str(Id))
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

	def getexamOverview(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM examDetails where examId='%s'"%(str(Id))
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

	def getComplainID(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT max(id) FROM candidate_complain;"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTopicChapter(self,chapterId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM chapter_topic where chapterId='%s'"%(chapterId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTopicChapterPaper(self,subjectId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM previous_paper where subjectId='%s'"%(subjectId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getchapterVideo(self,chapterId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM chapterVideo where chapterId='%s'"%(chapterId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getLivechat(self,videoId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM liveChat where videoId='%s'"%(videoId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getchapterbook(self,mobile,videoId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM bookmarkLive where username='%s' and videoId='%s'"%(mobile,videoId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTestRank(self,examId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM examHistory where examId='%s' order by correctAns Desc"%(examId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTopicDoubt(self,mobile):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id,mobile,imageUrl,subjectId,doubt,status,subject,videoUrl,videoId,createdAt,doubtId,date,time FROM doubt where mobile='%s'"%(mobile)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	

	def getTopicDoubtId(self,doubtId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM doubtchat where doubtId='%s' order by id desc"%(doubtId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTopicnotes(self,username):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM notes where username='%s'"%(username)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTopicreport(self,username):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM report;"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTopicreportcomment(self,videoId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM comment where videoId='%s'"%(videoId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTopicreporturl(self,videoId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM chapterVideo where id='%s'"%(videoId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTopireply(self,commentId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM reply where commentId='%s'"%(commentId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getcountReply(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT count(id) FROM reply where id='%s'"%(Id)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)								

	def getTopicrating(self,username):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM rating;"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetExamQue(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM questionList where id-'%s'"%(Id)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getToken2(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT mobile from student_register"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 

	def getTokenbyclasboard(self,categoryId,subcategoryId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT mobile from student_register where categoryId='%s' and subcategoryId='%s'"%(categoryId,subcategoryId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 

	def getExamsummary(self,mobile,examId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM examSummary where examId='%s' and mobile='%s'"%(examId,mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)	


	def getTotalExamMarks(self,examId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT sum(marks) FROM questionList where examId='%s'"%(examId)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)							

	def getcomplain(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From complain"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getcomplainListData(self,mobile):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM candidate_complain where mobile='%s'"%(mobile)
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

	def getcomplainListAdmin(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM candidate_complain "
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
	

	def getuserstudent_registerStatus(self,mobile):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From student_register where mobile='%s'"%str(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 


	def getclassList(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From Select_class"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 
	

	
	def getcityList(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From your_city"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 




	def getschoolList(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From your_school"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 
			




	def getboardList(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From School_board"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 


	def getexamList(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From exam"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getuserexamstatus(self,mobile,examId):
		try:
			dbname= 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "select * from examHistory where mobile='%s' and examId='%s'" %(mobile,examId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			if len(dbDetails)>0:
				return 1
			else:
				return 0
		except Exception,e:
			print str(e)

	def getuserexamstatusnew(self):
		try:
			dbname= 'elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "select * from examHistory"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			if len(dbDetails)>0:
				return 1
			else:
				return 0
		except Exception,e:
			print str(e)		

	def getregister(self, mobile):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * from student_register where mobile =%s" %(mobile)
			
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexampreviousPaper(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From previousPaper"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexamtestseries(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From testSeries"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexamliveclasses(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From chapterVideo"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexamliveclassesstory(self,categoryId,subcategoryId,subjectId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From chapterStory where categoryId='%s' and subcategoryId='%s' and subjectId='%s'"%(categoryId,subcategoryId,subjectId)
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

	def getstoryDetails(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From chapterStory"
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

	def getexamliveclassessubject2(self,categoryId,subcategoryId,subjectId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From subjectConcept where categoryId='%s' and subcategoryId='%s' and subjectId='%s'"%(categoryId,subcategoryId,subjectId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)	

	def getconceptDetails(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From subjectConcept "
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)			

	def getexamchaptervideo(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From chapterVideo order by id desc limit 10"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		

	def getexamcategory(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From masterCategory"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getsubCategorysimple(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From subCategory"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		


	def getexamcategorybyid(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From masterCategory where id='%s'"%(Id)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexamSubcategorybyid(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From subCategory where id='%s'"%(Id)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexamcoursecategorybyid(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From courseMaster where id='%s'"%(Id)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexamcoursecategorywithoutoverview(self,subjectId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From courseMaster where id='%s'"%(subjectId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		

	def getexamcoursecategorywithout(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From courseMaster "
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)				

	def getnotice(self,mobile):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From notification where mobile='%s'"%(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getAdminnotice(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From notification"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexamsubcategory(self,categoryId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From subCategory where categoryId='%s'"%(categoryId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexamsubcategory2(self,categoryId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From subCategory "
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexamboard(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From subCategory"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		

	def getexamlastcategory(self,subCategoryId,categoryId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From category  where  subCategoryId='%s' and categoryId='%s'"%(subCategoryId,categoryId)
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

	def getsubjectChapterList(self,subCategoryId,categoryId,subjectId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From topicMaster  where  subCategoryId='%s' and categoryId='%s' and subjectId='%s'"%(subCategoryId,categoryId,subjectId)
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

	def getexamcoursecategory(self,subCategoryId,categoryId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From courseMaster where  subCategoryId='%s' and categoryId='%s'"%(subCategoryId,categoryId)
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

	def getexamcoursecategoryid(self,categoryId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From courseMaster where categoryId='%s'"%(categoryId)
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

	def getexamcoursecategorysubid(self,subCategoryId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From courseMaster where  subCategoryId='%s'"%(subCategoryId)
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

	def getPartnerLastID(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT max(id) FROM student_register;"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getdoubtLastID(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT max(id) FROM doubt;"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getcoursesubject(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From courseMaster "
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getcoursesubjecthome(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From elearningHome "
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		

	def PostTeacherLogin(self, email):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT id, password, teacherName, phone_no, email,status,subject,schoolCode FROM teacher_details where (email = '%s')"%(email)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 

	def getTopic(self,subjectId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From topicMaster where subjectId='%s'"%(subjectId)
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

	def getTopicList(self,chapterId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT chapterName,topic,overview,chapterId From chapter_topic where chapterId='%s'"%(chapterId)
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

	def getSubName(self,subjectId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT name From courseMaster where id='%s'"%(subjectId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getchapternew(self,chapterId,topicId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From chapterStory where chapterId='%s' and topicId='%s'"%(chapterId,str(topicId))
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

	def getTopicnew(self,chapterId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From subjectConcept where id='%s'"%(chapterId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		

	def GetVideo(self,chapterId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From chapterVideo where chapterId='%s'"%(chapterId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetFreeVideo(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From chapterVideo where com_status=1"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetliveclassVideo(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From chapterVideo where com_status=2"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getsubject(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT distinct(name),id From courseMaster"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getvideoteacher(self,email):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From chapterVideo where createdBy='%s'"%(email)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetchapterStory(self,chapterId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From chapterStory where chapterId='%s'"%(chapterId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		

	def Getsubjectconcept(self,chapterId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From subjectConcept where chapterId='%s'"%(chapterId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)				

	def getexamsubjectcategory(self,subCategoryId,categoryId,sourceId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From subjectMaster where subCategoryId like'%%%s%%' and categoryId like '%%%s%%' and sourceId like '%%%s%%'"%(subCategoryId,categoryId,sourceId)
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

	def getexamnew(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From exam"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexamnewteacher(self,email):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From exam where createdBy='%s'"%(email)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexamnewquestion(self,examId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM questionList where examId='%s'"%(examId)
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

	def getquestionMarks(self,questionId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT marks,negativeMarks FROM questionList where id='%s'"%(questionId)
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

	def getMarks(self,examId,mobile):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT sum(marks),sum(negativeMarks) FROM examSummary where mobile='%s' and examId='%s'"%(mobile,examId)
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

	def getexamnewquestionvideo(self,chapterId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM chapterVideo where chapterId='%s'"%(chapterId)
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

	def getexamnewexamhistory(self,mobile):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From examHistory where mobile='%s'"%(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)								

	def getquestionlist(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From questionList"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTokenbyclass(self,categoryId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From student_register where categoryId='%s'"%(categoryId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getlastmessage(self,mobile):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id,doubt From doubt where mobile='%s' order by id desc limit 1"%(mobile)
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

	def getstudentDoubt(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT distinct(doubt.mobile),name,email,doubt.createdAt FROM elearning.doubt left join student_register  on doubt.mobile = student_register.mobile where doubt.status=0"
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


	def getquestionExam(self,examId):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From questionList where examId='%s'"%(examId)
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



	def getSchoolCity(self,city):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From your_school where city='%s'"%(city)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getstudentprofile(self,mobile):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From profile where mobile='%s'"%(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		

	def getquestionbookmark(self,mobile):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From bookmarkQuestion where mobile='%s'"%(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getbookmarklive(self,username):
		
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd = "SELECT * From bookmarkLive where username='%s'"%(username)
		print sqlcmd
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails
		 # Exception,e:
		# print str(e)		

	def getsubjectlist(self,className,boardName):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From subjectList where className='%s' and boardName='%s'"%(className,boardName)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getteacherdetails(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From teacher_details "
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getteacherProfile(self,email):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From teacher_details where email='%s'"%(email)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		

	def getpricing(self,className,year):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From pricing where className='%s' and year='%s'"%(className,year)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getpricingnew(self,className):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From pricing where className='%s'"%(className)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getpricingsimple(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From pricing "
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)				

	def getsimplepricing(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From pricing "
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)	

	def getloginnew(self,mobile):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From student_register where mobile='%s'"%(mobile)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		

	def getloginnew2(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From student_register"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)							

	def getrecommended(self):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From chapterVideo"
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getloginDetails(self,username,password):
		
		dbname='elearning'
		
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd ="SELECT * FROM login_details where username='%s' and password='%s'"%(str(username),str(password))
		print sqlcmd
		
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails

	def getUserSummary(self):
		
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlcmd_ ='SELECT(select count(id)  FROM chapterVideo   )AS liveClasses, (select count(id) from exam ) As testSeries, (select count(id) from student_register)As student_register,(select count(id)  FROM courseMaster   )AS subjectList,(select count(id)  FROM teacher_details   )AS teacher_details,(select count(id)  FROM doubt   )AS doubt'
		print _sqlcmd_
		cursor.execute(_sqlcmd_)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails															


	


    

   


class UpdateData():
	
	##################################### END #################################################
	# def UpdateUserData(self,mobile,domicile_document,documentUrl,dob,gender,maritalStatus,category,disability,profile_image,khasi_read,khasi_write,khasi_speak,garo_read,garo_write,garo_speak,english_read,english_write,english_speak,hindi_read,hindi_write,hindi_speak,other_read,other_write,other_speak,higher_education,passing_year,training,employed,work_experience,employment_prefer,work_outside,expectedSalary,short_training,notice_period,address,houseNo,landmark,city,state,pincode,status,trainingType,specialization,trainingDate,trainingDuration,completionDate,willingState,willingCity,course,health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others,pQualification,pCourse,pPassingYear, image_url,student_register_code):
	# 	# try:
	# 	dbname='play_school'
	# 	conn = connect_to_cloudsql(dbname)
	# 	cursor = conn.cursor()
	# 	sqlcmd="UPDATE user_basic SET domicile_document='%s',documentUrl='%s',dob='%s',gender='%s',maritalStatus='%s',category='%s',disability='%s',profile_image='%s',khasi_read='%s',khasi_write='%s',khasi_speak='%s',garo_read='%s',garo_write='%s',garo_speak='%s',english_read='%s',english_write='%s',english_speak='%s',hindi_read='%s',hindi_write='%s',hindi_speak='%s',other_read='%s',other_write='%s',other_speak='%s',higher_education='%s',passing_year='%s',training='%s',employed='%s',work_experience='%s',employment_prefer='%s',work_outside='%s',expectedSalary='%s',short_training='%s',notice_period='%s',address='%s',houseNo='%s',landmark='%s',city='%s',state='%s',pincode='%s',status='%s',trainingType='%s',specialization='%s',trainingDate='%s',trainingDuration='%s',completionDate='%s',willingState='%s',willingCity='%s',course='%s',health='%s',hospitality='%s',tourism='%s',it='%s',retail='%s',manufacturing='%s',food='%s',construction='%s',education='%s',banking='%s',others='%s',pQualification='%s',pCourse='%s',pPassingYear='%s', image_url='%s', student_registerId='%s',formStatus=1 where mobile='%s'"%(domicile_document,documentUrl,dob,gender,maritalStatus,category,disability,profile_image,khasi_read,khasi_write,khasi_speak,garo_read,garo_write,garo_speak,english_read,english_write,english_speak,hindi_read,hindi_write,hindi_speak,other_read,other_write,other_speak,higher_education,passing_year,training,employed,work_experience,employment_prefer,work_outside,expectedSalary,short_training,notice_period,address,houseNo,landmark,city,state,pincode,status,trainingType,specialization,trainingDate,trainingDuration,completionDate,willingState,willingCity,course,health,hospitality,tourism,it,retail,manufacturing,food,construction,education,banking,others,pQualification,pCourse,pPassingYear,image_url,student_register_code, mobile)
		
	# 	cursor.execute(sqlcmd)
	# 	testid = cursor.lastrowid
	# 	conn.commit()
	# 	conn.close()
	# 	return testid
	# 	# except Exception,e:
	# 	#   print str(e)

	def Updateuserdata(self,Id,topic,videoUrl,duration,imageUrl,documentUrl,createdBy,com_status):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE chapterVideo SET topic='%s',	videoUrl='%s',	duration='%s',	imageUrl='%s',	documentUrl='%s',	createdBy='%s',	com_status='%s' where id='%s'"%(topic,videoUrl,duration,imageUrl,documentUrl,createdBy,com_status,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updateuserdatasubject(self,Id,definition):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE subjectConcept SET definition='%s' where id='%s'"%(definition,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updateuserdatasubjecthome(self,Id,headerOne,headerTwo,headerImage,headerThree,liveclassesHeader,liveclassesPara,liveclassesImage,videoclassesHeader,videoclassesPara,videoclassesImage,adaptivepracticeHeader,adaptivepracticePara,adaptivepracticeImage,crammingImage,crammingHeader,crammingPara,approach,believe,believePara,repeatHeader,repeatPara,comfort,comfortPara,lowerHeader,lowerPara,stories,storiesPara,uniqueHeader,uniquePara,approachImage,managementHeader,managementPara,tendingImage,trendingHeader,trendingPara,bookImage,bookHeader,bookPara,certifiedImage,certifiedHeader,certifiedPara,allImage,syllabusHeader,syllabusPara,flexibilityHeader,flexibilityPara,savemoneyHeader,savemoneyPara,savemoneyokHeader,savemoneyokPara,saveImage,footerImage):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE elearningHome SET headerOne='%s',headerTwo='%s',headerImage='%s',headerThree='%s',liveclassesHeader='%s',liveclassesPara='%s',liveclassesImage='%s',videoclassesHeader='%s',videoclassesPara='%s',videoclassesImage='%s',adaptivepracticeHeader='%s',adaptivepracticePara='%s',adaptivepracticeImage='%s',crammingImage='%s',crammingHeader='%s',crammingPara='%s',approach='%s',believe='%s',believePara='%s',repeatHeader='%s',repeatPara='%s',comfort='%s',comfortPara='%s',lowerHeader='%s',lowerPara='%s',stories='%s',storiesPara='%s',uniqueHeader='%s',uniquePara='%s',approachImage='%s',managementHeader='%s',managementPara='%s',tendingImage='%s',trendingHeader='%s',trendingPara='%s',bookImage='%s',bookHeader='%s',bookPara='%s',certifiedImage='%s',certifiedHeader='%s',certifiedPara='%s',allImage='%s',syllabusHeader='%s',syllabusPara='%s',flexibilityHeader='%s',flexibilityPara='%s',savemoneyHeader='%s',savemoneyPara='%s',savemoneyokHeader='%s',savemoneyokPara='%s',saveImage='%s',footerImage='%s' where id='%s'"%(headerOne,headerTwo,headerImage,headerThree,liveclassesHeader,liveclassesPara,liveclassesImage,videoclassesHeader,videoclassesPara,videoclassesImage,adaptivepracticeHeader,adaptivepracticePara,adaptivepracticeImage,crammingImage,crammingHeader,crammingPara,approach,believe,believePara,repeatHeader,repeatPara,comfort,comfortPara,lowerHeader,lowerPara,stories,storiesPara,uniqueHeader,uniquePara,approachImage,managementHeader,managementPara,tendingImage,trendingHeader,trendingPara,bookImage,bookHeader,bookPara,certifiedImage,certifiedHeader,certifiedPara,allImage,syllabusHeader,syllabusPara,flexibilityHeader,flexibilityPara,savemoneyHeader,savemoneyPara,savemoneyokHeader,savemoneyokPara,saveImage,footerImage,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid	

	def Updatelike(self,Id):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE chapterVideo SET likes=likes+1 where id='%s'"%(Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updatedislike(self,Id):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE chapterVideo SET dislikes=dislikes+1 where id='%s'"%(Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updatediscomments(self,Id):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE comment SET likes=likes+1 where id='%s'"%(Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid	

	def Updatedislcomments(self,Id):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE comment SET dislikes=dislikes+1 where id='%s'"%(Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updateuserdatachapter(self,Id,definition):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE chapterStory SET definition='%s' where id='%s'"%(definition,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid	

	def UpdateTopic(self,Id,topic,overview):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE chapter_topic SET topic='%s',overview='%s' where id='%s'"%(topic,overview,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid		

	def Updatechaptervideo(self,Id,chapterId,topic,videoUrl,duration,imageUrl):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE chapterVideo SET chapterId='%s',	topic='%s',	videoUrl='%s',	duration='%s',	imageUrl='%s' where id='%s'"%(chapterId,topic,videoUrl,duration,imageUrl,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid	

	def Updateusercategory(self,Id,name,description,createdBy):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE masterCategory SET name='%s',	description='%s',	createdBy='%s' where id='%s'"%(name,description,createdBy,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updateuserlogin(self,Id,mobile,name,email,inviteCode,imageName):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE student_register SET mobile='%s',name='%s',email='%s',inviteCode='%s',imageName='%s' where id='%s'"%(mobile,name,email,inviteCode,imageName,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid	

	def UpdateuserData2(self,mobile,className,boardName,preparingForExam,categoryId,subCategoryId):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE student_register SET className='%s',boardName='%s',preparingForExam='%s',status=1,categoryId='%s',subCategoryId='%s' where mobile='%s'"%(className,boardName,preparingForExam,categoryId,subCategoryId,mobile)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateuserDatauser(self,Id,mobile,name,email,className,boardName,preparingForExam,inviteCode):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE student_register SET mobile='%s',name='%s',email='%s',className='%s',boardName='%s',preparingForExam='%s',inviteCode='%s' where id='%s'"%(mobile,name,email,className,boardName,preparingForExam,inviteCode,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid	

	def UpdateuserDatanew(self,Id,question,optionA,optionB,optionC,optionD,correctAns,examId,description,marks,negativeMarks):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE questionList SET question='%s',optionA='%s',optionB='%s',optionC='%s',optionD='%s',correctAns='%s',examId='%s',description='%s',marks='%s',negativeMarks='%s' where id='%s'"%(question,optionA,optionB,optionC,optionD,correctAns,examId,description,marks,negativeMarks,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid	

	def Updateteacherdetails(self,Id,teacherName,schoolCode,subject,phone_no,email,password,image):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE teacher_details SET teacherName='%s',schoolCode='%s',subject='%s',phone_no='%s',email='%s',password='%s',image='%s' where id='%s'"%(teacherName,schoolCode,subject,phone_no,email,password,image,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid		

	def Updateusersubcategory(self,Id,name,description,createdBy,categoryId):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE subCategory SET name='%s',	description='%s',	createdBy='%s',categoryId='%s' where id='%s'"%(name,description,createdBy,categoryId,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updateuserlastcategory(self,Id,name,description,createdBy,subCategoryId,categoryId):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE category SET name='%s',	description='%s',	createdBy='%s',subCategoryId='%s',categoryId='%s' where id='%s'"%(name,description,createdBy,subCategoryId,categoryId,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updateuserlastcourse(self,Id,examId,name,description,subCategoryId,categoryId,overview):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE courseMaster SET examId='%s',name='%s',description='%s',subCategoryId='%s',categoryId='%s',overview='%s' where id='%s'"%(examId,name,description,subCategoryId,categoryId,overview,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updateuserlastsubject(self,Id,examId,name,description,sourceId,subCategoryId,categoryId):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE subjectMaster SET examId='%s',name='%s',description='%s',sourceId='%s',subCategoryId='%s',categoryId='%s' where id='%s'"%(examId,name,description,sourceId,subCategoryId,categoryId,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid						

	def Updateuserexam(self,Id,title,description,categoryId,createdBy,duration):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE exam SET title='%s',description='%s',categoryId='%s',createdBy='%s',duration='%s' where id='%s'"%(title,description,categoryId,createdBy,duration,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updateuserexamquestion(self,Id,questionType,question,optionA,optionB,optionC,optionD,correctAns,examId,marks,negativeMarks):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE questionList SET questionType='%s',question='%s',optionA='%s',optionB='%s',optionC='%s',optionD='%s',correctAns='%s',examId='%s',marks='%s',negativeMarks='%s' where id='%s'"%(questionType,question,optionA,optionB,optionC,optionD,correctAns,examId,marks,negativeMarks,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updateuserexamhistory(self,Id,examId,totalQuestion,attempted,correctAns,wrongAns,examTime,categoryId):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE examHistory SET examId='%s',totalQuestion='%s',attempted='%s',correctAns='%s',wrongAns='%s',examTime='%s',categoryId='%s' where id='%s'"%(examId,totalQuestion,attempted,correctAns,wrongAns,examTime,categoryId,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid								

	def Updateusertest(self,Id,imageUrl,examName,noOfSeat,noOfQuestion,marks,subjectList):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE testSeries SET imageUrl='%s',	examName='%s',	noOfSeat='%s',	noOfQuestion='%s',	marks='%s',status=1,	subjectList='%s' where id='%s'"%(imageUrl,examName,noOfSeat,noOfQuestion,marks,subjectList,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid	

	def Updatenotesdata(self,Id,url,notes,username):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE notes SET url='%s',	notes='%s' where id='%s'"%(url,notes,Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def UpdateReply(self,complainId,reply):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd="UPDATE candidate_complain SET reply='%s',status=1 where complainId='%s'"%(reply,complainId)
			cursor.execute(sqlcmd)
			testid = cursor.lastrowid
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
		  print str(e)	

	def UpdatesubjectChapter(self,Id,overview,chapter):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd="UPDATE topicMaster SET chapter='%s',overview='%s' where id='%s'"%(chapter,overview,Id)
			cursor.execute(sqlcmd)
			testid = cursor.lastrowid
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
		  print str(e)		

	def UpdateactiveClass(self,Id):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE chapterVideo SET status=1 where id='%s'"%(Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updateactivetest(self,Id):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE testSeries SET status=1 where id='%s'"%(Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid	

	def UpdatedeactiveClass(self,Id):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE chapterVideo SET status=0 where id='%s'"%(Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid

	def Updatedeactiveseries(self,Id):
		# try:
		dbname='elearning'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE testSeries SET status=0 where id='%s'"%(Id)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid				



	

	

class DeleteData():

	def deleteToken(self,mobile):
		try:
			dbname='elearning'
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

	def Deletesubjectconcept(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM subjectConcept WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def Deletechapterstory(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM chapterStory WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)				

	def DeleteRemovebook(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM bookmarkLive WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeletecourseChapterList(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM topicMaster WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)
		

	def DeleteRemoveteacher(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM teacher_details WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)		

	def DeleteDatavideo(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM chapterVideo WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)		

	def DeleteData2(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM liveClasses WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteTopic(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM chapter_topic WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteDatastudent(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM student_register WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)		

	def DeleteDatamaster(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM masterCategory WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteDatamastersub(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM subCategory WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteDatamasterlast(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM category WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteDatamastercourse(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM courseMaster WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteDataquestion(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM questionList WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)		

	def DeleteDatamastersubject(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM subjectMaster WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)								

	def DeleteDataexam(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM exam WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteDataexamquestion(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM question WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)				

	def DeleteDatalive(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM chapterVideo WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)				

	def Deletetest(self,Id):
		try:
			dbname='elearning'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM testSeries WHERE id="%s"'%(Id)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)				

	

	
