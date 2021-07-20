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
	
	

	def adduser(self,name,mobile,email,password):
		try:
			dbname = 'Exam'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd_="INSERT INTO login_details (name,mobile,email,password) VALUES ('%s','%s','%s','%s')"%(name,mobile,email,password)
			cursor.execute(sqlcmd_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addUserexamque(self,examId,totalQuestion,attempted,correctAns,wrongAns,examTime,categoryId,mobile):
		try:
			dbname = 'Exam'
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


	def addUsersummary(self,mobile,examId,questionId,answer,correct,marks,negativeMarks):
		try:
			dbname = 'Exam'
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

	

													

	

		#######################################################################################################
					   
class GetData():

	def checkUserstatus(self,email):
		try:
			dbname='Exam'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * from login_details where email='%s'" %(email)
			print sqlcmd
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

	def getloginnew(self,email):
		try:
			dbname='Exam'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * from login_details where email='%s'" %(email)
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

	def GetExamQue(self,Id):
		try:
			dbname='Exam'
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

	def getExamsummary(self,mobile,examId):
		try:
			dbname='Exam'
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

	
	def getquestionMarks(self,questionId):
		try:
			dbname='Exam'
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

	def getTestRank(self,examId):
		try:
			dbname='Exam'
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

	
	def getTotalExamMarks(self,examId):
		try:
			dbname='Exam'
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

	def getMarks(self,examId,mobile):
		try:
			dbname='Exam'
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

	def getregister(self, mobile):
		try:
			dbname='Exam'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * from login_details where mobile =%s" %(mobile)
			
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getexamData(self,):
		
		dbname='Exam'
		
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd ="SELECT * FROM Exam_data order by id desc"
		print sqlcmd
		
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails


	def getquestionExam(self,examId):
		try:
			dbname='Exam'
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



class UpdateData():
	
	##################################### END #################################################
	def UpdatePassword(self,username,password):
		# try:
		dbname='Act'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd="UPDATE login_details SET password='%s' where mobile='%s' or email='%s' or profileId='%s'"%(password,str(username),str(username),str(username))
		print sqlcmd
		
		cursor.execute(sqlcmd)
		testid = cursor.lastrowid
		conn.commit()
		conn.close()
		return testid
		# except Exception,e:
		#   print str(e)

	def UpdateadminPassword(self,username,password):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd="UPDATE admin_login SET password='%s' where email='%s'"%(password,str(username))
			cursor.execute(sqlcmd)
			testid = cursor.lastrowid
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
		  print str(e)

	def UpdateProfile(self,Id,name,image,password):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd="UPDATE login_details SET name='%s',image='%s',password='%s' where id='%s'"%(name,image,password,Id)
			cursor.execute(sqlcmd)
			testid = cursor.lastrowid
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
		  print str(e)

class DeleteData():

	def deleteVideo(self,username,videoId):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM video_like WHERE username="%s" and videoId="%s"'%(username,videoId)
			cursor.execute(sqlcmd)
			_sqlcmd_='DELETE FROM notification WHERE username="%s" and videoId="%s"'%(username,videoId)
			cursor.execute(_sqlcmd_)
			sqlcmd_="UPDATE video_list SET liked=liked-1 where id='%s'"%(videoId)
			cursor.execute(sqlcmd_)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def deletefollowup(self,profileId,followupId):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM follow WHERE profileId="%s" and followupId="%s"'%(profileId,followupId)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

														


	



	

	
