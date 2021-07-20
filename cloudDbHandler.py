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
	
	

	

	
	
	def addloginDetails(self,username,name,password,email,phone_no):
		try:
			dbname = 'ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()

			_sqlc_ = "INSERT INTO login_details (username,name,password,email,phone_no,adminTpe,status) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(username,name,password,email,phone_no,0,0)

			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
		  print str(e)

	def addUser(self,username,email,phone_no,state,district,block,school):
		try:
			dbname = 'ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO login_details (username,email,phone_no,adminType,status,state,district,block,school) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(username,email,phone_no,0,0,state,district,block,school)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addsurvey(self,description,survey):
		try:
			dbname = 'ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO survey_list (description,survey) VALUES ('%s','%s')"%(description,survey)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)		   
	def addclasssurvey(self,username,registeredStudent,presentStudent,absentStudent,appointedTeacher,presentTeacher,absentTeacher,studentStatus,punctualityStudent,teacherStatus,punctualityTeacher,classActivity,conversation,relationship,studyMaterial,studentExibition,groupWork,Questions,studentSkills,lastActivity,Assignment,assignmentMarks,lunchStatus,lunchInspection,Cleanliness,drinkingWater,toiletStatus,ptmMeeting,ptmPresence,dateTime):
		try:
			dbname = 'ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()

			_sqlc_ = "INSERT INTO Survey (username,registeredStudent,presentStudent,absentStudent,appointedTeacher,presentTeacher,absentTeacher,studentStatus,punctualityStudent,teacherStatus,punctualityTeacher,classActivity,conversation,relationship,studyMaterial,studentExibition,groupWork,Questions,studentSkills,lastActivity,Assignment,assignmentMarks,lunchStatus,lunchInspection,Cleanliness,drinkingWater,toiletStatus,ptmMeeting,ptmPresence) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(username,registeredStudent,presentStudent,absentStudent,appointedTeacher,presentTeacher,absentTeacher,studentStatus,punctualityStudent,teacherStatus,punctualityTeacher,classActivity,conversation,relationship,studyMaterial,studentExibition,groupWork,Questions,studentSkills,lastActivity,Assignment,assignmentMarks,lunchStatus,lunchInspection,Cleanliness,drinkingWater,toiletStatus,ptmMeeting,ptmPresence)
			cursor.execute(_sqlc_)
			sqlcmd="UPDATE login_details SET surveyStatus=1 ,dateTime='%s' where phone_no='%s'"%(str(dateTime),str(username))
			print sqlcmd
			cursor.execute(sqlcmd)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
		  print str(e)

	def addschooldetails(self,username,schoolName,schoolCode):
		try:
			dbname = 'ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()

			_sqlc_ = "INSERT INTO schoolDetails (username,schoolName,schoolCode) VALUES ('%s','%s','%s')"%(username,schoolName,schoolCode)

			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
		  print str(e)

	def addQuestion(self,question,option1,option2,option3,option4):
		try:
			dbname = 'ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO question (question,option1,option2,option3,option4) VALUES ('%s','%s','%s','%s','%s')"%(question,option1,option2,option3,option4)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
		  print str(e)
				
		





	

	

	############################################################ 
	
	

	

	
	#######################################################################################################
					   
class GetData():


	
	def getloginDetails(self,username,password):
		
		dbname='ssca'
		
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

	def getUserSurveyStatus(self,username,district,block,school):
		
		dbname='ssca'
		
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd ="SELECT status FROM login_details where phone_no='%s' and district='%s' and block='%s' and school='%s'"%(str(username),str(district),str(block),str(school))
		print sqlcmd
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails

	def getQuestionStatus(self,):
		
		dbname='ssca'
		
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd ="SELECT(SELECT count(id) FROM question where status=1) As question"
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails

	def getSurveyStatus(self,mobile):
		
		dbname='ssca'
		
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd ="SELECT * FROM login_details where phone_no='%s'"%(mobile)
		print sqlcmd
		
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails

	def getuserList(self,):
		
		dbname='ssca'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd ="SELECT * FROM login_details ORDER BY id DESC"
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails

	def getUserStatus(self,mobile):
		
		dbname='ssca'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd ="SELECT status,surveyStatus FROM login_details where phone_no='%s'"%(mobile)
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails

	def getUserSummary(self):
		
		dbname='ssca'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlcmd_ ='SELECT(select count(id)  FROM login_details  where status=0  )AS Inactive, (select count(id) from login_details where status=1) As Active'
		print _sqlcmd_
		cursor.execute(_sqlcmd_)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails

	def getclasssurvey(self,username):
		
		dbname='ssca'
		
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd ="SELECT * FROM Survey where username='%s'"%(str(username))
		print sqlcmd
		
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails

	def getLatestVersion(self):
		try:
			dbname='ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="select id,appName,version,versionCode,updateOn from appVersion WHERE  id  IN( select max(id) FROM appVersion)"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 

	def getStateList(self):
		try:
			dbname='ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="select * from state_data order by stateName"
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getDistrictList(self,stateCode):
		try:
			dbname='ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="select disticName,distcode from organisation where stateId='%s'"%(stateCode)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 

	def getSchoolList(self,block):
		try:
			dbname='ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="select organizationName from organisation where blockName='%s'"%(block)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 

	def getBlockList(self,districtcode):
		try:
			dbname='ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="select blockName from organisation where distcode='%s'"%(districtcode)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 

	def getUsersurvey(self,mobile):
		try:
			dbname='ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="select * FROM Survey where username='%s'"%(mobile)
			cursor.execute(_sqlcmd_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e) 

	def getAdminsurvey(self):
		
		dbname='ssca'
		
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd ="SELECT * FROM Survey"
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails

	def getschooldetails(self,username):
		
		dbname='ssca'
		
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd ="SELECT * FROM schoolDetails where username='%s'"%(str(username))
		print sqlcmd
		
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails   

	def getUserLoginStatus(self,mobile):
		try:
			dbname='ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * From login_details where phone_no='%s'"%str(mobile)
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

	

	


	def updateUserStatus(self,Id):
		try:
			dbname='ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd="UPDATE login_details SET status=1 where id=%s "%(Id)
			print sqlcmd
			cursor.execute(sqlcmd)
			testid = cursor.lastrowid
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
		  print str(e)

	def updateDeUserStatus(self,Id):
		try:
			dbname='ssca'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd="UPDATE login_details SET status=0 where id=%s "%(Id)
			print sqlcmd
			cursor.execute(sqlcmd)
			testid = cursor.lastrowid
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
		  print str(e)

	

	

