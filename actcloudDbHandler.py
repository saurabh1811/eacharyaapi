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
	
	

	def addLike(self,username,videoId,message,profileId):
		try:
			dbname = 'Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO video_like (username,videoId) VALUES ('%s','%s')"%(username,videoId)
			cursor.execute(_sqlc_)
			sqlcmd_="INSERT INTO notification (username,videoId,notification,profileId) VALUES ('%s','%s','%s','%s')"%(username,videoId,message,profileId)
			cursor.execute(sqlcmd_)
			sqlcmd="UPDATE video_list SET liked=liked+1 where id='%s'"%(videoId)
			print sqlcmd
			cursor.execute(sqlcmd)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def adduser(self,mobile,name,email,password,profileId,isActor,image,userType):
		try:
			dbname = 'Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO login_details (mobile,name,email,password,profileId,isActor,image,userType) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(mobile,name,email,password,profileId,isActor,image,userType)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addComment(self,username,videoId,videoUrl,comment,message,profileId):
		try:
			dbname = 'Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO comment (username,videoId,videoUrl,comment) VALUES ('%s','%s','%s','%s')"%(username,videoId,videoUrl,comment)
			cursor.execute(_sqlc_)
			_sqlc = "INSERT INTO notification (username,videoId,notification,profileId) VALUES ('%s','%s','%s','%s')"%(username,videoId,message,profileId)
			cursor.execute(_sqlc)
			sqlcmd="UPDATE video_list SET comment=comment+1 where id='%s'"%(videoId)
			cursor.execute(sqlcmd)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addVideo(self,profileId,description,videoUrl,image,tags):
		try:
			dbname = 'Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO video_list (profileId,description,videoUrl,image,tags) VALUES ('%s','%s','%s','%s','%s')"%(profileId,description,videoUrl,image,tags)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addFollowup(self,profileId,followupId):
		try:
			dbname = 'Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO follow (profileId,followupId) VALUES ('%s','%s')"%(profileId,followupId)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addLogo(self,filename):
		try:
			dbname = 'Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO logo (images) VALUES ('%s')"%(filename)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	
	def addSubadmin(self,mobile,name,email,password,status):
		try:
			dbname = 'Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO admin_login (mobile,name,email,password,status) VALUES ('%s','%s','%s','%s','%s')"%(mobile,name,email,password,status)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addReportedVideo(self,videoId,profileId,message):
		try:
			dbname = 'Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO reported_video (videoId,reportedProfile,message) VALUES ('%s','%s','%s')"%(videoId,profileId,message)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addAudio(self,audio,description,name):
	# try:
		dbname = 'Act'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		_sqlc_ = "INSERT INTO audioFile (audio,description,name) VALUES ('%s','%s','%s')"%(audio,description,name)
		cursor.execute(_sqlc_)
		conn.commit()
		testid = cursor.lastrowid
		conn.close()
		return testid 
	# except Exception,e:
	# 	print str(e)

													

	

		#######################################################################################################
					   
class GetData():

	def getloginDetails(self,email,password):
		
		dbname='Act'
		
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()
		sqlcmd ="SELECT * FROM admin_login where email='%s' and password='%s'"%(str(email),str(password))
		print sqlcmd
		
		cursor.execute(sqlcmd)
		dbDetails=[]
		for row in cursor.fetchall():
			dbDetails.append(row)
		conn.commit()
		conn.close()
		return dbDetails

	def checkUser(self,username):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * from login_details where mobile='%s' or email='%s' or profileId='%s'" %(str(username),str(username),str(username))
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


	def checkPhone(self, phone):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="select COUNT(id) from admin_login WHERE (mobile='%s')"%(phone)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			count = (cursor.fetchone())[0]
			print count
			print 'count='
			if (count==None):
				result=0
			elif (count==0):
				result=1
			else:
				result=2
			print result
			print 'result='
			conn.commit()
			conn.close()
			return result
		except Exception,e:
			print str(e)

	def checkEmail(self, email):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="select COUNT(id) from admin_login WHERE (email='%s')"%(email)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			count = (cursor.fetchone())[0]
			print count
			print 'count='
			if (count==None):
				result=0
			elif (count==0):
				result=1
			else:
				result=2
			print result
			print 'result='
			conn.commit()
			conn.close()
			return result
		except Exception,e:
			print str(e)

	def videolikeed(self,username,videoId):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * from video_like where username='%s' and videoId='%s'" %(username,videoId)
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

	def checkUserstatus(self,mobile):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * from login_details where mobile='%s'" %(str(mobile))
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

	def checkUserstatus2(self,email):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * from login_details where email='%s'" %(str(email))
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

	def checkSubadminstatus(self,email):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * from admin_login where email='%s'" %(str(email))
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

	def checkFollowstatus(self,profileId,followupId):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * from follow where profileId='%s' and followupId='%s'" %(profileId,followupId	)
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

	def getUserLastId(self):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT max(id) FROM login_details;"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def checkFollower(self,username):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT count(id) FROM follow where followupId='%s'"%(username)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def uservideoList(self,profileId):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT email,mobile,profileId,name,image,isActor FROM Act.login_details where profileId='%s'"%(profileId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getReportedVideo(self):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT reported_video.id,videoId,reportedProfile,profileId,name,image,email,mobile,blockStatus,blockDate FROM Act.reported_video left join login_details  on reportedProfile = profileId order by reported_video.id desc"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def profileId(self,videoId):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT profileId,liked,comment FROM video_list where id='%s'"%(videoId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getChildAdmin(self):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM admin_login where status=0"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getvideo(self,videoId):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT videoUrl FROM video_list where id='%s'"%(videoId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def uservideoListData(self,profileId):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM video_list where profileId='%s'"%(profileId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def Postlogin(self,username):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM login_details where mobile='%s' or email='%s' or profileId='%s'"%(str(username),str(username),str(username))
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def userprofile(self,username):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT image FROM login_details where mobile='%s' or email='%s' or profileId='%s'"%(str(username),str(username),str(username))
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def videolike(self,videoId):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM video_like where videoId='%s' order by id desc"%(videoId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getAdminSummary(self):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT(select count(id)  FROM video_list)AS video, (select count(id) from login_details) As user,(select count(id)  FROM admin_login   where  status=1)AS SubAdmin,(select count(id)  FROM reported_video)AS reportedVideo,(select count(id)  FROM audioFile)AS audio"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getUserlist(self):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM login_details  order by id desc"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getTrendingVideo(self):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM video_list  order by id desc"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetAudio(self):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM audioFile  order by id desc"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetLogo(self):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM logo  ORDER BY id DESC LIMIT 1"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getNotification(self,profileId):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM notification where profileId='%s' order by id desc"%(profileId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def videoComment(self,videoId):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM comment where videoId='%s' order by id desc"%(videoId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def video(self):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM video_list order by id desc"
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def videofollows(self,profileId):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM Act.video_list  WHERE  profileId  IN( select followupId FROM follow where profileId='%s')"%(profileId)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)


	def getloginAdminDetails(self,email):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT * FROM admin_login where email='%s'"%(email)
			cursor.execute(sqlcmd)
			dbDetails=[]
			dbDetails = cursor.fetchall()
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

	def UpdateProfile(self,Id,name,image,password,userType):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd="UPDATE login_details SET name='%s',image='%s',password='%s',userType='%s' where id='%s'"%(name,image,password,userType,Id)
			cursor.execute(sqlcmd)
			testid = cursor.lastrowid
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
		  print str(e)

	def UpdateBlock(self,profileId,blockDate,blockStatus):
		try:
			dbname='Act'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd="UPDATE login_details SET blockDate='%s',blockStatus='%s'where profileId='%s'"%(blockDate,blockStatus,profileId)
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
			print sqlcmd_
			cursor.execute(sqlcmd_)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def deleteDepartment(self, did):
	# try:
		dbname='Act'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()

		#Delete Employees
		sqlcmd='DELETE FROM admin_login WHERE  id="%s"'%(did)
		cursor.execute(sqlcmd)
		count = cursor.rowcount
		conn.commit()
		conn.close()
		return count
	# except Exception,e:
	# 	return 0
	# 	print str(e)

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

														


	



	

	
