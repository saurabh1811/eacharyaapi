# -*- coding: utf-8 -*-
from flask import Flask, request, Response
import json, urllib2, logging
import payrollcloudDbHandler as dbhelper
import datetime as datetime
import json
import StringIO

import mailhandler
import random
from math import radians, cos, sin, asin, sqrt
import math
import ast
from time import gmtime, strftime
# import cloudDbHandler as dbhelper
from sets import  Set
import unicodedata
import re
import urllib as urllib
import urllib2 as urllib2


# from datetime import datetime


import googleapiclient.discovery
import googleapiclient.http
from google.appengine.api import urlfetch
from datetime import timedelta, date, datetime
from time import gmtime, strftime,time,localtime
# from dateutil.parser import parse







app = Flask(__name__)

############################   Normal Function To calculate the Details   ###################################################

API_KEY = ['BiZ0JSyxLbAUNkHb13BxR','yFGsqfLeGu7Hx1XU63ZTh']



def daterange(date1, date2):
	for n in range(int ((date2 - date1).days)+1):
		yield date1 + timedelta(n)

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

# def changeDateFormat(words):
# 	dt = parse(words)
# 	date_w = dt.strftime('%d/%m/%Y')
# 	return date_w


# signup
@app.route('/payroll/add/payroll-v2/user/',methods=['GET','POST'])
def APiAddUser():
	if request.method=='POST':
		userInfo  = json.loads(request.data)
		name = userInfo['name']
		username = userInfo['username']    
		phone = userInfo['phone']
		email   = userInfo['email']
		password  = userInfo['password']
		signupdate = userInfo['signupdate']
		trialperiod = userInfo['trialperiod']
		newid = dbhelper.AddData().addUser(name, username, phone, email, password, signupdate, trialperiod)
		AddUser = dbhelper.GetData().returnSignupCookies(username)
		print AddUser
		AddUser_db = []
		if (len(AddUser))>=0:
			for line in AddUser:
				AddUser_dict = {}
				AddUser_dict['USER_ID'] 								=line[0]
				AddUser_dict['USER_NAME'] 								=line[1]
				AddUser_dict['USER_EMAIL'] 								=line[2]
				AddUser_dict['USER_PHONE'] 								=line[3]
				AddUser_dict['USER_ROLE'] 								=line[4]
				AddUser_dict['USER_MAX_COMPANIES']						=line[5]
				AddUser_dict['USER_CREATED_COMPANIES']					=line[6]
				AddUser_dict['USER_SIGNUP_DATE']						=line[7]
				AddUser_dict['USER_TRIAL_PERIOD']						=line[8]
				
				
								
				AddUser_db.append(AddUser_dict)
				
		if (len(AddUser_db))>0:
				resp = Response(json.dumps({"success": 1,"message":"success","datasets":AddUser_db}))
		else:
			resp = Response(json.dumps({"success": 0,"message":"Cookies Could not be retrieved"}))	
		
		
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#unique username
@app.route('/payroll/check/username/', methods=['GET','POST'])
def ApiCheckUsername():
	if request.method=='POST':
		userInfo  = json.loads(request.data)
		username = userInfo['username']
		checkUsername = dbhelper.GetData().checkUsername(username)
		print ('chkusrname='+str(checkUsername))
		if (str(checkUsername)=='0'):
			db={'message':'Username Invalid'}
			success = 0
		elif (str(checkUsername)=='1'):
			db={'message': 'Username Valid'}
			success = 1
		else:
			db={'message':'Username Invalid'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#unique phone
@app.route('/payroll/check/phone/', methods=['GET','POST'])
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

# Login
@app.route('/payroll/login/payroll-v2',methods=['GET','POST'])
def ApiUserLogin():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		email= configure_data['email']
		password= configure_data['password']
		login_info_data = dbhelper.GetData().LoginData(email)
		login_info_data_db = []

		if (len(login_info_data))>=0:
			for line in login_info_data:
				login_info_data_dict = {}
				login_info_data_dict['USER_ID'] 						=line[0]
				login_info_data_dict['USER_NAME'] 						=line[1]
				login_info_data_dict['USER_EMAIL'] 						=line[2]
				login_info_data_dict['USER_PASSWORD'] 					=line[3]
				login_info_data_dict['USER_ROLE'] 						=line[4]
				login_info_data_dict['USER_PHONE']						=line[5]
				login_info_data_dict['USER_MAX_COMPANIES']				=line[6]
				login_info_data_dict['USER_CREATED_COMPANIES']			=line[7]
				
				
								
				login_info_data_db.append(login_info_data_dict)
				
		if (len(login_info_data_db))>0:

			if(password==login_info_data[0][3]):
				resp = Response(json.dumps({"success": 1,"message":"success","datasets":login_info_data_db}))
			else:
				resp = Response(json.dumps({"success": 2,"message":"wrong credentials"}))
		else:
			resp = Response(json.dumps({"success": 0,"message":"No Data found"}))	
		
		
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################

#Company_setup
@app.route('/payroll/add/payroll-v2/company/',methods=['GET','POST'])
def ApiAddCompany():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		name = configure_data['oname']
		country = configure_data['country']
		industry = configure_data['industry']
		state = configure_data['state']
		city = configure_data['city']
		pin = configure_data['pin']
		address1 = configure_data['address1']
		address2 = configure_data['address2']
		address = address1 + " " + address2
		filing_address = address + ", " + city + ", " + state + ", " + pin + ", " + country
		userid = configure_data['userid']
		addCompany = dbhelper.AddData().addCompany(name,country,industry,address,city,state,pin,filing_address,userid)
		if addCompany:
			db={'message':'company added'}
			success = 1
		else:
			db={'message': 'company already exists or company could not be added'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#GET COMPANIES AND DETAILS
@app.route('/payroll/get/payroll-v2/user-companies/',methods=['GET','POST'])
def ApiGetUserCompanies():
	if request.method =='GET':
		print request
		uid=request.args.get('userid')
		print uid
		companies_data = dbhelper.GetData().GetUserCompanies(uid)
		print companies_data
		companies_data_db=[]
		if(len(companies_data))>0:
			for line in companies_data:
				companies_data_dict={}
				companies_data_dict['cid']							=line[0]
				companies_data_dict['cname']						=line[1]
				companies_data_dict['PRIMARY_ADDRESS']				=line[2]
				companies_data_dict['COMPANY_CITY']					=line[3]
				companies_data_dict['COMPANY_STATE']				=line[4]
				companies_data_dict['COMPANY_COUNTRY']				=line[5]
				companies_data_dict['COMPANY_PIN']					=line[6]
				companies_data_dict['industry']						=line[7]
				print line[8]
				if (int(line[8])==1):
					companies_data_dict['status']					='Active'
				else:
					companies_data_dict['status']					='Inactive'					

				companies_data_db.append(companies_data_dict)

		resp = Response(json.dumps({"success": True, "posts":companies_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#GET company to edit
@app.route('/payroll/get/payroll-v2/edit-companies/',methods=['GET','POST'])
def ApiGetCompany():
	if request.method =='GET':
		print request
		uid=request.args.get('userid')
		print uid
		cid=request.args.get('cid')
		print cid
		companies_data = dbhelper.GetData().GetCompany(uid,cid)
		print companies_data
		companies_data_db=[]
		if(len(companies_data))>0:
			for line in companies_data:
				companies_data_dict={}
				companies_data_dict['cid']							=line[0]
				companies_data_dict['cname']						=line[1]
				companies_data_dict['PRIMARY_ADDRESS']				=line[2]
				companies_data_dict['COMPANY_CITY']					=line[3]
				companies_data_dict['COMPANY_STATE']				=line[4]
				companies_data_dict['COMPANY_COUNTRY']				=line[5]
				companies_data_dict['COMPANY_PIN']					=line[6]
				companies_data_dict['industry']						=line[7]
				print line[8]
				if (line[8]=='1'):
					companies_data_dict['status']					='Active'
				else:
					companies_data_dict['status']					='Inactive'					

				companies_data_db.append(companies_data_dict)

		resp = Response(json.dumps({"success": True, "posts":companies_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#UPDATE COMPANY
@app.route('/payroll/update/payroll-v2/edit-companies/',methods=['GET','POST'])
def ApiUpdateCompany():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		name = configure_data['oname']
		country = configure_data['country']
		industry = configure_data['industry']
		state = configure_data['state']
		city = configure_data['city']
		pin = configure_data['pin']
		address1 = configure_data['address1']
		address2 = configure_data['address2']
		address = address1 + address2
		filing_address = address + ", " + city + ", " + state + ", " + str(pin) + ", " + country
		userid = configure_data['userid']
		cid= configure_data['cid']
		UpdateCompany = dbhelper.UpdateData().updateCompany( cid, name, country, industry, address, city, state, pin, filing_address, userid)
		if UpdateCompany:
			db={'message':'company updated'}
			success = 1
		else:
			db={'message':'company updated'}
			success = 1
			

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Get Active Company
@app.route('/payroll/get/payroll-v2/active_company/',methods=['GET','POST'])
def ApiActiveCompany():
	if request.method=='GET':
		print request
		userid=request.args.get('userid')
		print userid
		activeCompany = dbhelper.GetData().GetActiveCompany(userid)
		print activeCompany
		activeCompany_db=[]
		if activeCompany:
			for line in activeCompany:
				activeCompany_dict={}
				activeCompany_dict['COMPANY_ID']= 		line[0]
				activeCompany_dict['COMPANY_NAME']= 	line[1]


				activeCompany_db.append(activeCompany_dict)

			db={'ACTIVE_COMPANY_ID':activeCompany_db}
			success = 1
		else:
			db={'ACTIVE_COMPANY_ID': 'could not get any active company'}
			success = 0
			
		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Change Active Company
@app.route('/payroll/change/payroll-v2/active_company/',methods=['GET','POST'])
def ApiChangeActiveCompany():
	if request.method=='GET':
		print request
		userid=request.args.get('userid')
		print userid
		cmpid=request.args.get('cid')
		print cmpid
		activeCompany = dbhelper.UpdateData().ChangeActiveCompany(userid,cmpid)
		print activeCompany
		activeCompany_db=[]
		if activeCompany:
			for line in activeCompany:
				activeCompany_dict={}
				activeCompany_dict['COMPANY_ID']= 		line[0]
				activeCompany_dict['COMPANY_NAME']= 	line[1]


				activeCompany_db.append(activeCompany_dict)

			db={'ACTIVE_COMPANY_ID':activeCompany_db}
			success = 1
		else:
			db={'ACTIVE_COMPANY_ID': 'could not get any active company'}
			success = 0
		
		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#delete company
@app.route('/payroll/delete/payroll-v2/company/',methods=['GET','POST','DELETE'])
def ApiDeleteCompany():
	if request.method=='DELETE':
		print request.data
		cid= request.args.get('cid')
		DeleteCompany = dbhelper.DeleteData().DeleteCompany(cid)
		if DeleteCompany:
			db={'message':'Company Deleted'}
			success = 1
		else:
			db={'message': 'Company could not be deleted'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db, "Company ID": cid}))
		return after_request(resp)

###################################################################################################

# Add New Salary Component Earning
@app.route('/payroll/add/payroll-v2/salary-component-earning/',methods=['GET','POST'])
def ApiAddSalaryComponentEarning():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		component_name= configure_data['component_name']
		component_type=configure_data['component_type']
		component_payslip_name=configure_data['component_payslip_name']
		component_pay_type=configure_data['component_pay_type']
		component_calculation_type=0
		component_calculation_amt=0
		if( int(configure_data['calculation_type'])%10==1):
			component_calculation_type=0
		elif(int(configure_data['calculation_type'])%10==2):
			component_calculation_type=2
		
		if(component_calculation_type==0):
			component_calculation_amt= configure_data['amount']
		elif(component_calculation_type==2):
			component_calculation_amt= configure_data['percent']
		
		active_state=0
		if(configure_data['checked']=='true'):
			active_state=1
		elif(configure_data['checked']=='false'):
			active_state=0

		cmpid = request.args.get('cid')
		
		addComponent = dbhelper.AddData().addSalaryComponentEarning(component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, active_state, cmpid)
		if addComponent:
			db={'message':'component added'}
			success = 1
		else:
			db={'message': 'component not added'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

# Get Salary Components Earning
@app.route('/payroll/get/payroll-v2/salary-components-earning/',methods=['GET','POST'])
def ApiGetSalaryComponentsEarning():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		component_data = dbhelper.GetData().GetSalaryComponentsEarning(cmpid)
		print component_data
		component_data_db=[]
		if(len(component_data))>0:
			for line in component_data:
				test_data_dict={}
				test_data_dict['component_id']						=line[0]
				test_data_dict['component_name']					=line[1]
				test_data_dict['component_type']					=line[2]
				test_data_dict['component_payslip_name']			=line[3]
				test_data_dict['component_pay_type']				=line[4]
				
				if(line[5]==0):
					test_data_dict['component_calculation_type']='Flat Amount'
				elif(line[5]==1):
					test_data_dict['component_calculation_type']='Percentage of CTC'
				else:
					test_data_dict['component_calculation_type']='Percentage of Basic'

				test_data_dict['component_calculation_amt']			=line[6]
				
				if(line[7]==1):
					test_data_dict['status']='Active'
				else:
					test_data_dict['status']='Inactive'
									

				component_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "posts":component_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Change component active status earning
@app.route('/payroll/change/payroll-v2/active_component_earning/',methods=['GET','POST'])
def ApiChangeActiveComponentEarning():
	if request.method=='GET':
		print request
		cid=request.args.get('cid')
		compid=request.args.get('compid')
		print cid, compid
		activeComponentChange = dbhelper.UpdateData().ChangeActiveComponentEarning(compid,cid)
		print activeComponentChange
		activeComponent_db=[]
		if (activeComponentChange==1):
			success= 1
			db={'Activity': 'Toggled'}
		else:
			db={'Activity': 'could not change'}
			success = 0
		
		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Delete earning component
@app.route('/payroll/delete/payroll-v2/salary_component_earning/',methods=['GET','POST','DELETE'])
def ApiDeleteComponentEarning():
	if request.method=='DELETE':
		print 'data', request.data
		cid= request.args.get('cid')
		compid = request.args.get('compid')
		DeleteComponentEarning = dbhelper.DeleteData().DeleteComponentEarning(cid,compid)
		if DeleteComponentEarning:
			db={'message':'Component Deleted'}
			success = 1
		else:
			db={'message': 'Component could not be deleted'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

##################################################################################################

# Add New Salary Component Deduction
@app.route('/payroll/add/payroll-v2/salary-component-deduction/',methods=['GET','POST'])
def ApiAddSalaryComponentDeduction():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		name= configure_data['name']
		amt_type=configure_data['type']
		amt=configure_data['amount']
		if(configure_data['checked']=='true'):
			active_state=1
		else:
			active_state=0

		preorposttax= configure_data['preorposttax']
		cmpid = request.args.get('cmpid')
		addComponent = dbhelper.AddData().addSalaryComponentDeduction(name, amt_type, amt, active_state, preorposttax, cmpid)
		if addComponent:
			db={'message':'component added'}
			success = 1
		else:
			db={'message': 'component not added'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

# Get Salary Components Deduction PreTax
@app.route('/payroll/get/payroll-v2/salary-components-deduction-pretax/',methods=['GET','POST'])
def ApiGetSalaryComponentDeductionPreTax():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		component_data = dbhelper.GetData().GetSalaryComponentsDeductionPreTax(cmpid)
		print component_data
		component_data_db=[]
		if(len(component_data))>0:
			for line in component_data:
				test_data_dict={}
				test_data_dict['name']					=line[0]
				test_data_dict['type']					=line[1]
				test_data_dict['amount']				=line[2]
				if(line[3]==1):
					test_data_dict['status']='Active'
				else:
					test_data_dict['status']='Inactive'					

				component_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "deducts1":component_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

# Get Salary Components Deduction PostTax
@app.route('/payroll/get/payroll-v2/salary-components-deduction-posttax/',methods=['GET','POST'])
def ApiGetSalaryComponentDeductionPostTax():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		component_data = dbhelper.GetData().GetSalaryComponentsDeductionPostTax(cmpid)
		print component_data
		component_data_db=[]
		if(len(component_data))>0:
			for line in component_data:
				test_data_dict={}
				test_data_dict['name']					=line[0]
				test_data_dict['type']					=line[1]
				test_data_dict['amount']				=line[2]
				if(line[3]==1):
					test_data_dict['status']='Active'
				else:
					test_data_dict['status']='Inactive'					

				component_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "deducts2":component_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

##################################################################################################

# Get Salary Components Reimbursement
@app.route('/payroll/get/payroll-v2/salary-components-reimbursement/',methods=['GET','POST'])
def ApiGetSalaryComponentReimbursement():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		component_data = dbhelper.GetData().GetSalaryComponentsReimbursement(cmpid)
		print component_data
		component_data_db=[]
		if(len(component_data))>0:
			for line in component_data:
				test_data_dict={}
				test_data_dict['id']					=line[0]
				test_data_dict['name']					=line[1]
				test_data_dict['type']					=line[2]
				test_data_dict['amount']				=line[3]
				if(line[4]==1):
					test_data_dict['status']='Active'
				else:
					test_data_dict['status']='Inactive'					

				component_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "reimburse":component_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

# Get Salary Components Reimbursement to edit
@app.route('/payroll/edit/payroll-v2/salary-components-reimbursement/',methods=['GET','POST'])
def ApiGetSalaryComponentReimbursementEdit():
	if request.method =='GET':
		cmpid = request.args.get('cid')
		compid = request.args.get('compid')

		component_data = dbhelper.GetData().GetSalaryComponentsReimbursementEdit(cmpid, compid)
		print component_data
		component_data_db=[]
		if(len(component_data))>0:
			for line in component_data:
				test_data_dict={}
				test_data_dict['id']					=line[0]
				test_data_dict['name']					=line[1]
				test_data_dict['type']					=line[2]
				test_data_dict['amount']				=line[3]
				if(line[4]==1):
					test_data_dict['status']='Active'
				else:
					test_data_dict['status']='Inactive'					

				component_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "reimburse":component_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#change salary components reimbursement status
@app.route('/payroll/change/payroll-v2/active_component_reimbursement/',methods=['GET','POST'])
def ApiChangeActiveComponentReimbursement():
	if request.method=='GET':
		print request
		cid=request.args.get('cid')
		compid=request.args.get('compid')
		print cid, compid
		activeComponentChange = dbhelper.UpdateData().ChangeActiveComponentReimbursement(compid,cid)
		print activeComponentChange
		if (activeComponentChange==1):
			success= 1
			db={'Activity': 'Toggled'}
		else:
			db={'Activity': 'could not change'}
			success = 0
		
		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Update Reimbursement Components
@app.route('/payroll/update/payroll-v2/salary-components-reimbursement/',methods=['GET','POST'])
def ApiUpdateComponentReimbursement():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		component_name = configure_data['name']
		component_type = configure_data['type']
		amount = configure_data['amount']
		active_state=0
		if(configure_data['checked']=='true'):
			active_state=1
		elif(configure_data['checked']=='false'):
			active_state=0
		cid = request.args.get('cid')
		compid= request.args.get('compid')
		UpdateComponentReimbursement = dbhelper.UpdateData().UpdateComponentReimbursement( component_name, component_type, amount, active_state, cid, compid)
		if UpdateComponentReimbursement:
			db={'message':'company updated'}
			success = 1
		else:
			db={'message': 'company could not be updated'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

##################################################################################################

#Add Branch
@app.route('/payroll/add/payroll-v2/branch/',methods=['GET','POST'])
def ApiAddBranch():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		name = configure_data['name']
		state = configure_data['state']
		city = configure_data['city']
		pin = configure_data['pin']
		address1 = configure_data['address1']
		address2 = configure_data['address2']
		address = address1 + " " + address2
		country = configure_data['country']
		cmpid = request.args.get('cmpid')
		addBranch = dbhelper.AddData().addBranch( name, address, city, state, country, pin, cmpid)
		print addBranch
		if addBranch:
			db={'message':'branch added'}
			success = 1
		else:
			db={'message': 'branch not added'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Update Branch
@app.route('/payroll/update/payroll-v2/branch/',methods=['GET','POST'])
def ApiUpdateBranch():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		name = configure_data['name']
		state = configure_data['state']
		city = configure_data['city']
		pin = configure_data['pin']
		address1 = configure_data['address1']
		address2 = configure_data['address2']
		address = address1 + " " + address2
		country = configure_data['country']
		cmpid = request.args.get('cmpid')
		bid = request.args.get('bid')
		addBranch = dbhelper.UpdateData().updateBranch( name, address, city, state, country, pin, cmpid, bid)
		print addBranch
		if addBranch:
			db={'message':'branch updated'}
			success = 1
		else:
			db={'message': 'branch not updated'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Get Branch
@app.route('/payroll/get/payroll-v2/branch-details/',methods=['GET','POST'])
def ApiGetBranchDetails():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		branch_data = dbhelper.GetData().GetBranchDetails(cmpid)
		print branch_data
		branch_data_db=[]
		if(len(branch_data))>0:
			for line in branch_data:
				branch_data_dict={}
				branch_data_dict['BRANCH_ID']					=line[0]
				branch_data_dict['BRANCH_NAME']					=line[1]
				branch_data_dict['BRANCH_ADDRESS']				=line[2]
				branch_data_dict['BRANCH_CITY']					=line[3]
				branch_data_dict['BRANCH_STATE']				=line[4]
				branch_data_dict['BRANCH_COUNTRY']				=line[5]
				branch_data_dict['BRANCH_PIN']					=line[6]
									

				branch_data_db.append(branch_data_dict)

		resp = Response(json.dumps({"success": True, "posts":branch_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get Branch to Edit
@app.route('/payroll/get/payroll-v2/edit-branch/',methods=['GET','POST'])
def ApiGetBranchEdit():
	if request.method =='GET':
		cmpid = request.args.get('cid')
		bid = request.args.get('bid')
		branch_data = dbhelper.GetData().GetBranchEdit(bid, cmpid)
		print branch_data
		branch_data_db=[]
		if(len(branch_data))>0:
			for line in branch_data:
				branch_data_dict={}
				branch_data_dict['BRANCH_ID']					=line[0]
				branch_data_dict['BRANCH_NAME']					=line[1]
				branch_data_dict['BRANCH_ADDRESS']				=line[2]
				branch_data_dict['BRANCH_CITY']					=line[3]
				branch_data_dict['BRANCH_STATE']				=line[4]
				branch_data_dict['BRANCH_COUNTRY']				=line[5]
				branch_data_dict['BRANCH_PIN']					=line[6]
									

				branch_data_db.append(branch_data_dict)

		resp = Response(json.dumps({"success": True, "posts":branch_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#delete branch
@app.route('/payroll/delete/payroll-v2/branch/',methods=['GET','POST','DELETE'])
def ApiDeleteBranch():
	if request.method=='DELETE':
		print 'data', request.data
		bid= request.args.get('bid')
		deleteBranch = dbhelper.DeleteData().deleteBranch(bid)
		if deleteBranch:
			db={'message':'Branch Deleted'}
			success = 1
		else:
			db={'message': 'Branch could not be deleted'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Get branch for drop down
@app.route('/payroll/get/payroll-v2/branch-drop-down/',methods=['GET','POST'])
def ApiGetBranchDropDown():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		branch_data = dbhelper.GetData().GetBranchDropDown(cmpid)
		print branch_data
		branch_data_db=[]
		if(len(branch_data))>0:
			for line in branch_data:
				branch_data_dict={}
				branch_data_dict['label']					=line[0]
				branch_data_dict['value']					=line[1]
									

				branch_data_db.append(branch_data_dict)

		resp = Response(json.dumps({"success": True, "posts":branch_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################

#Add Department
@app.route('/payroll/add/payroll-v2/department/',methods=['GET','POST'])
def ApiAddDepartment():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		name = configure_data['name']
		cmpid = configure_data['cmpid']
		userid = configure_data['userid']
		creation = configure_data['creation']
		addDepartment = dbhelper.AddData().addDepartment( name, cmpid, userid, creation)
		print addDepartment
		if addDepartment:
			db={'message':'Department added'}
			success = 1
		else:
			db={'message': 'Department not added'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#GET DEPARTMENTS
@app.route('/payroll/get/payroll-v2/department-list/',methods=['GET','POST'])
def ApiGetDepartmentList():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		department_data = dbhelper.GetData().GetDepartmentList(cmpid)
		print department_data
		department_data_db=[]
		if(len(department_data))>0:
			for line in department_data:
				department_data_dict={}
				department_data_dict['DEPARTMENT_ID']					=line[0]
				department_data_dict['DEPARTMENT_NAME']					=line[1]
				department_data_dict['DEPARTMENT_CREATED_ON']			=line[2]
				userid													=line[3]
				username = dbhelper.GetData().GetUser(userid)
				department_data_dict['DEPARTMENT_CREATED_BY']			=username
									
				department_data_db.append(department_data_dict)

		resp = Response(json.dumps({"success": True, "posts":department_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


@app.route('/payroll/contact/request/',methods=['GET','POST'])
def BirthdayWish():
	if request.method=='POST':
		birthday_wish=json.loads(request.data)
		print request.data
		contact_number =birthday_wish['contact_number']
		from_name  =birthday_wish['from_name']
		to_name  =birthday_wish['to_name']
		company_name=birthday_wish['company_name']
		location=birthday_wish['location']
		email=birthday_wish['email']
		website=birthday_wish['website']
		product=birthday_wish['product']
		message_html=birthday_wish['message_html']
		reply_to=birthday_wish['reply_to']
		to_id="info@tracelay.net"

		mailhandler.sendMail().sendLeadsDetails(to_id, contact_number,from_name,to_name,company_name,location,email,website,product,message_html,reply_to)
		

		resp = Response(json.dumps({"response": "Success"}))
		return after_request(resp)



@app.route('/payroll/contact/subscribe/',methods=['GET','POST'])
def subscribe():
	if request.method=='POST':
		subscribe=json.loads(request.data)
		email =subscribe['email']
		text="Thanks for Subscribing Tracelay"
		

		mailhandler.sendMail().sendSubscription(email, text)
		

		resp = Response(json.dumps({"response": "Success"}))
		return after_request(resp)
#Get Department to Edit
@app.route('/payroll/get/payroll-v2/edit-department/',methods=['GET','POST'])
def ApiGetDepartmentEdit():
	if request.method =='GET':
		cmpid = request.args.get('cid')
		did = request.args.get('did')
		department_data = dbhelper.GetData().GetDepartmentEdit(did, cmpid)
		print department_data
		department_data_db=[]
		if(len(department_data))>0:
			for line in department_data:
				department_data_dict={}
				department_data_dict['DEPARTMENT_ID']					=line[0]
				department_data_dict['DEPARTMENT_NAME']					=line[1]
									

				department_data_db.append(department_data_dict)

		resp = Response(json.dumps({"success": True, "posts":department_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Update Department
@app.route('/payroll/update/payroll-v2/department/',methods=['GET','POST'])
def ApiUpdateDepartment():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		name = configure_data['name']
		cmpid = request.args.get('cmpid')
		did = configure_data['did']
		addDepartment = dbhelper.UpdateData().updateDepartment( name, cmpid, did)
		print addDepartment
		if addDepartment:
			db={'message':'branch updated'}
			success = 1
		else:
			db={'message': 'branch not updated'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#delete department
@app.route('/payroll/delete/payroll-v2/department/',methods=['GET','POST','DELETE'])
def ApiDeleteDepartment():
	if request.method=='DELETE':
		print 'data', request.data
		did= request.args.get('did')
		deleteDepartment = dbhelper.DeleteData().deleteDepartment(did)
		if deleteDepartment:
			db={'message':'Dept Deleted'}
			success = 1
		else:
			db={'message': 'Dept could not be deleted'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#get dept for drop down
@app.route('/payroll/get/payroll-v2/department-drop-down/',methods=['GET','POST'])
def ApiGetDepartmentDropDown():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		department_data = dbhelper.GetData().GetDepartmentDropDownList(cmpid)
		print department_data
		department_data_db=[]
		if(len(department_data))>0:
			for line in department_data:
				department_data_dict={}
				department_data_dict['label']					=line[0]
				department_data_dict['value']					= int(line[1])
									
				department_data_db.append(department_data_dict)

		resp = Response(json.dumps({"success": True, "posts":department_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################

#Add Designation
@app.route('/payroll/add/payroll-v2/designation/',methods=['GET','POST'])
def ApiAddDesignation():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		name = configure_data['name']
		cmpid = configure_data['cmpid']
		userid = configure_data['userid']
		creation = configure_data['creation']
		addDesignation = dbhelper.AddData().addDesignation( name, cmpid, userid, creation)
		print addDesignation
		if addDesignation:
			db={'message':'Designation added'}
			success = 1
		else:
			db={'message':'Designation not added'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#GET Designation
@app.route('/payroll/get/payroll-v2/designation-list/',methods=['GET','POST'])
def ApiGetDesignationList():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		designation_data = dbhelper.GetData().GetDesignationList(cmpid)
		print designation_data
		designation_data_db=[]
		if(len(designation_data))>0:
			for line in designation_data:
				designation_data_dict={}
				designation_data_dict['DESIGNATION_ID']					=line[0]
				designation_data_dict['DESIGNATION_NAME']				=line[1]
				designation_data_dict['DESIGNATION_CREATED_ON']			=line[2]
				userid													=line[3]
				username = dbhelper.GetData().GetUser(userid)
				designation_data_dict['DESIGNATION_CREATED_BY']			=username					
				designation_data_db.append(designation_data_dict)

		resp = Response(json.dumps({"success": True, "posts":designation_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get Designation to Edit
@app.route('/payroll/get/payroll-v2/edit-designation/',methods=['GET','POST'])
def ApiGetDesignationEdit():
	if request.method =='GET':
		cmpid = request.args.get('cid')
		did = request.args.get('did')
		designation_data = dbhelper.GetData().GetDesignationEdit(did, cmpid)
		print designation_data
		designation_data_db=[]
		if(len(designation_data))>0:
			for line in designation_data:
				designation_data_dict={}
				designation_data_dict['DESIGNATION_ID']					=line[0]
				designation_data_dict['DESIGNATION_NAME']				=line[1]
									

				designation_data_db.append(designation_data_dict)

		resp = Response(json.dumps({"success": True, "posts":designation_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Update Designation
@app.route('/payroll/update/payroll-v2/designation/',methods=['GET','POST'])
def ApiUpdateDesignation():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		name = configure_data['name']
		cmpid = configure_data['cmpid']
		did = configure_data['did']
		addDesignation = dbhelper.UpdateData().updateDesignation( name, cmpid, did)
		print addDesignation
		if addDesignation:
			db={'message': 'branch not updated'}
			success = 0
			
		else:
			db={'message':'branch updated'}
			success = 1

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#delete designation
@app.route('/payroll/delete/payroll-v2/designation/',methods=['GET','POST','DELETE'])
def ApiDeleteDesignation():
	if request.method=='DELETE':
		print 'data', request.data
		did= request.args.get('did')
		deleteDesignation = dbhelper.DeleteData().deleteDesignation(did)
		if deleteDesignation:
			db={'message':'Designation Deleted'}
			success = 1
		else:
			db={'message': 'Designation could not be deleted'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Get Designation Drop Down
@app.route('/payroll/get/payroll-v2/designation-drop-down/',methods=['GET','POST'])
def ApiGetDesignationDropDown():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		designation_data = dbhelper.GetData().GetDesignationDropDown(cmpid)
		print designation_data
		designation_data_db=[]
		if(len(designation_data))>0:
			for line in designation_data:
				designation_data_dict={}
				designation_data_dict['label']					=line[0]
				designation_data_dict['value']					=line[1]
								
				designation_data_db.append(designation_data_dict)

		resp = Response(json.dumps({"success": True, "posts":designation_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################

#FOR SALARY TEMPLATE
# Get Salary Components Active Reimbursement
@app.route('/payroll/get/payroll-v2/salary-components-reimbursement-active/',methods=['GET','POST'])
def ApiGetActiveSalaryComponentReimbursement():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		component_data = dbhelper.GetData().GetActiveSalaryComponentsReimbursement(cmpid)
		print component_data
		component_data_db=[]
		if(len(component_data))>0:
			for line in component_data:
				test_data_dict={}
				test_data_dict['id']					=line[0]
				test_data_dict['name']					=line[1]
				test_data_dict['type']					=line[2]
				test_data_dict['amount']				=line[3]
				if(line[4]==1):
					test_data_dict['status']='Active'
				else:
					test_data_dict['status']='Inactive'					
				test_data_dict['button']='<Button onClick={this.getRowId} type="dashed" shape="circle" icon="close">Close</Button>'

				component_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "reimburse":component_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

# Get Salary Components Active Earning
@app.route('/payroll/get/payroll-v2/salary-components-earning-active/',methods=['GET','POST'])
def ApiActiveGetSalaryComponentsEarning():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		component_data = dbhelper.GetData().GetActiveSalaryComponentsEarning(cmpid)
		print component_data
		component_data_db=[]
		if(len(component_data))>0:
			for line in component_data:
				test_data_dict={}
				test_data_dict['component_id']						=line[0]
				test_data_dict['component_name']					=line[1]
				test_data_dict['component_type']					=line[2]
				test_data_dict['component_payslip_name']			=line[3]
				test_data_dict['component_pay_type']				=line[4]
				
				if(line[5]==0):
					test_data_dict['component_calculation_type']='Flat Amount'
				elif(line[5]==1):
					test_data_dict['component_calculation_type']='Percentage of CTC'
				else:
					test_data_dict['component_calculation_type']='Percentage of Basic'

				test_data_dict['component_calculation_amt']			=line[6]
				
				if(line[7]==1):
					test_data_dict['status']='Active'
				else:
					test_data_dict['status']='Inactive'
				test_data_dict['button']='<Button onClick={this.getRowId} type="dashed" shape="circle" icon="close">Close</Button>'			

				component_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "posts":component_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Send Salary Components Earning selected in template
@app.route('/payroll/get/payroll-v2/salary-components-earning-template/',methods=['GET','POST'])
def ApiTemplateActiveGetSalaryComponentsEarning():
	if request.method =='POST':
		configure_data = json.loads(request.data)
		cmpid = configure_data['cmpid']
		componentstring = configure_data['active_earning_components']
		components=[]
		components.append(componentstring.split(','))
		print len(components[0])
		component_data_db=[]
		for i in range(0,len(components[0])):
			id= (components[0])[i]
			print id
			component_data = dbhelper.GetData().GetTemplateActiveSalaryComponentsEarning(id, cmpid)
			for line in component_data:
				test_data_dict={}
				test_data_dict['component_id']						=line[0]
				test_data_dict['component_name']					=line[1]
				test_data_dict['component_type']					=line[2]
				test_data_dict['component_payslip_name']			=line[3]
				test_data_dict['component_pay_type']				=line[4]
				
				if(line[5]==0):
					test_data_dict['component_calculation_type']='Flat Amount'
				elif(line[5]==1):
					test_data_dict['component_calculation_type']='Percentage of CTC'
				else:
					test_data_dict['component_calculation_type']='Percentage of Basic'

				test_data_dict['component_calculation_amt']			=line[6]
				
				if(line[7]==1):
					test_data_dict['status']='Active'
				else:
					test_data_dict['status']='Inactive'

				component_data_db.append(test_data_dict)
				


		resp = Response(json.dumps({"success": True, "posts":component_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


#Send Salary Components Reimbursements selected in template
@app.route('/payroll/get/payroll-v2/salary-components-reimbursement-template/',methods=['GET','POST'])
def ApiTemplateActiveGetSalaryComponentsReimbursement():
	if request.method =='POST':
		configure_data = json.loads(request.data)
		cmpid = configure_data['cmpid']
		componentstring = configure_data['active_reimbursement_components']
		components=[]
		components.append(componentstring.split(','))
		print len(components[0])
		component_data_db=[]
		for i in range(0,len(components[0])):
			id= (components[0])[i]
			print id
			component_data = dbhelper.GetData().GetTemplateActiveSalaryComponentsReimbursement(id, cmpid)
			for line in component_data:
				test_data_dict={}
				test_data_dict={}
				test_data_dict['id']					=line[0]
				test_data_dict['name']					=line[1]
				test_data_dict['type']					=line[2]
				test_data_dict['amount']				=line[3]
				if(line[4]==1):
					test_data_dict['status']='Active'
				else:
					test_data_dict['status']='Inactive'					

				component_data_db.append(test_data_dict)
				


		resp = Response(json.dumps({"success": True, "reimburses":component_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Template Calculator
#Calculate and send back amounts
@app.route('/payroll/get/payroll-v2/template-calculations/',methods=['GET','POST'])
def ApiTemplateCalculations():
	if request.method =='POST':
		configure_data = json.loads(request.data)
		earnings = configure_data['posts']
		print earnings
		reimburses = configure_data['reimburses']
		ctc = configure_data['ctc']
		earning_amount_all=[]
		earning_amount_monthly_all=[]
		reimburse_amount_all=[]
		reimburse_amount_monthly_all=[]
		total_monthly=0
		total_annually=0
		fixed_allowance_monthly=0
		fixed_allowance_annually=0
		basic=0
		for i in range(0,len(earnings)):
			calculation_type= earnings[i]['component_calculation_type']
			if (calculation_type=='Percentage of CTC'):
				earning_amount =float((int(earnings[i]['component_calculation_amt']) * int(ctc))/100) 
				earning_amount_monthly= earning_amount/12
				earning_amount_all.append(earning_amount)
				earning_amount_monthly_all.append(earning_amount_monthly)
			elif(calculation_type=='Percentage of Basic'):
				for j in range(0,len(earnings)):
					if(earnings[j]['component_name']=='Basic'):
						basic = float((int(earnings[i]['component_calculation_amt']) * int(ctc))/100) 
				earning_amount= float((int(earnings[i]['component_calculation_amt']) * int(basic))/100)
				earning_amount_monthly= earning_amount/12
				earning_amount_all.append(earning_amount)
				earning_amount_monthly_all.append(earning_amount_monthly)
			elif(calculation_type=='Flat Amount'):
				earning_amount = int(earnings[i]['component_calculation_amt'])
				earning_amount_monthly = earning_amount/12
				earning_amount_all.append(earning_amount)
				earning_amount_monthly_all.append(earning_amount_monthly)
		
		for i in range(0,len(reimburses)):
			amount = int(reimburses[i]['amount'])
			amount_monthly = amount/12
			reimburse_amount_all.append(amount)
			reimburse_amount_monthly_all.append(amount_monthly)

		for i in range(0, len(earning_amount_monthly_all)):
			total_monthly += earning_amount_monthly_all[i]

		for i in range(0, len(reimburse_amount_monthly_all)):
			total_monthly += reimburse_amount_monthly_all[i]

		for i in range(0, len(earning_amount_all)):
			total_annually += earning_amount_all[i]

		for i in range(0, len(reimburse_amount_all)):
			total_annually += reimburse_amount_all[i]
   		
		
		payable_annually = int(ctc)


		if(int(ctc)<=250000):
			rate = 0
			income_tax_annually = payable_annually * rate
			income_tax_monthly = income_tax_annually/12
		elif((int(ctc)>250000) and (int(ctc)<=500000)):
			rate = 0.05
			print rate
			income_tax_annually = payable_annually * rate
			income_tax_monthly = income_tax_annually/12
		elif((int(ctc)>500000) and (int(ctc)<=1000000)):
			rate = 0.2
			income_tax_annually = payable_annually * rate
			income_tax_monthly = income_tax_annually/12
		else:
			rate = 0.3
			income_tax_annually = payable_annually * rate
			income_tax_monthly = income_tax_annually/12

		print income_tax_annually
		print income_tax_monthly

   		fixed_allowance_monthly = int(ctc)/12 - total_monthly - income_tax_monthly
   		fixed_allowance_annually = int(ctc) - total_annually - income_tax_annually
   		total_monthly = int(ctc)/12 - income_tax_monthly
   		total_annually = int(ctc) - income_tax_annually


   

	
	resp = Response(json.dumps({"earnings_monthly": earning_amount_monthly_all, "earnings_annually": earning_amount_all, "reimburse_monthly": reimburse_amount_monthly_all, "reimburse_annually": reimburse_amount_all, "total_monthly": total_monthly, "total_annually": total_annually, "fixed_allowance_monthly": fixed_allowance_monthly, "fixed_allowance_annually": fixed_allowance_annually, "income_tax_monthly": income_tax_monthly, "income_tax_annually": income_tax_annually}))
	resp.headers['Content-type']='application/json'
	return after_request(resp)

#Template Calculator 2
#Calculate and send back amounts
@app.route('/payroll/get/payroll-v2/template-calculations-2/',methods=['GET','POST'])
def ApiTemplateCalculationsTwo():
	if request.method =='POST':
		configure_data = json.loads(request.data)

		cmpid = configure_data['cmpid']
		earning_components = (configure_data['active_earning_components']).strip().split(',')
		reimbursement_components = (configure_data['active_reimbursement_components']).strip().split(',')
		ctc = configure_data['ctc']
		
		#Get Earning Details
		earnings=[]
		for i in range(0, len(earning_components)):
			earning = (dbhelper.GetData().GetTemplateActiveSalaryComponentsEarning(earning_components[i], cmpid))
			for line in earning:
				test_data_dict={}
				test_data_dict['component_id']						=line[0]
				test_data_dict['component_name']					=line[1]
				test_data_dict['component_type']					=line[2]
				test_data_dict['component_payslip_name']			=line[3]
				test_data_dict['component_pay_type']				=line[4]
				
				if(line[5]==0):
					test_data_dict['component_calculation_type']='Flat Amount'
				elif(line[5]==1):
					test_data_dict['component_calculation_type']='Percentage of CTC'
				else:
					test_data_dict['component_calculation_type']='Percentage of Basic'

				test_data_dict['component_calculation_amt']			=line[6]
				
				if(line[7]==1):
					test_data_dict['status']='Active'
				else:
					test_data_dict['status']='Inactive'

				earnings.append(test_data_dict)
		
		#Get Reimbursement Details
		reimbursements=[]
		for i in range(0,len(reimbursement_components)):
			reimbursement = dbhelper.GetData().GetTemplateActiveSalaryComponentsReimbursement(reimbursement_components[i], cmpid)
			for line in reimbursement:
				test_data_dict={}
				test_data_dict['id']					=line[0]
				test_data_dict['name']					=line[1]
				test_data_dict['type']					=line[2]
				test_data_dict['amount']				=line[3]
				if(line[4]==1):
					test_data_dict['status']='Active'
				else:
					test_data_dict['status']='Inactive'					

				reimbursements.append(test_data_dict)


		earning_amount_all=[]
		earning_amount_monthly_all=[]
		reimburse_amount_all=[]
		reimburse_amount_monthly_all=[]
		total_monthly=0
		total_annually=0
		fixed_allowance_monthly=0
		fixed_allowance_annually=0
		basic=0
		
		#Calculate Earning amounts
		for i in range(0,len(earnings)):
		 	calculation_type= earnings[i]['component_calculation_type']
		 	if (calculation_type=='Percentage of CTC'):
		 		earning_amount =float((int(earnings[i]['component_calculation_amt']) * int(ctc))/100) 
		 		earning_amount_monthly= earning_amount/12
		 		earning_amount_all.append(earning_amount)
		 		earning_amount_monthly_all.append(earning_amount_monthly)
		 	elif(calculation_type=='Percentage of Basic'):
		 		for j in range(0,len(earnings)):
		 			if(earnings[j]['component_name']=='Basic'):
		 				basic = float((int(earnings[i]['component_calculation_amt']) * int(ctc))/100) 
		 		earning_amount= float((int(earnings[i]['component_calculation_amt']) * int(basic))/100)
		 		earning_amount_monthly= earning_amount/12
		 		earning_amount_all.append(earning_amount)
		 		earning_amount_monthly_all.append(earning_amount_monthly)
		 	elif(calculation_type=='Flat Amount'):
		 		earning_amount = int(earnings[i]['component_calculation_amt'])
		 		earning_amount_monthly = earning_amount/12
		 		earning_amount_all.append(earning_amount)
		 		earning_amount_monthly_all.append(earning_amount_monthly)
		
		#Calculate Reimbursement amounts
		for i in range(0,len(reimbursements)):
			amount = int(reimbursements[i]['amount'])
		 	amount_monthly = amount/12
		 	reimburse_amount_all.append(amount)
		 	reimburse_amount_monthly_all.append(amount_monthly)

		#Generate Summary
		for i in range(0, len(earning_amount_monthly_all)):
		 	total_monthly += earning_amount_monthly_all[i]

		for i in range(0, len(reimburse_amount_monthly_all)):
		 	total_monthly += reimburse_amount_monthly_all[i]

		for i in range(0, len(earning_amount_all)):
		 	total_annually += earning_amount_all[i]

		for i in range(0, len(reimburse_amount_all)):
			total_annually += reimburse_amount_all[i]

		payable_annually = int(ctc)


		if(int(ctc)<=250000):
			rate = 0
			income_tax_annually = payable_annually * rate
			income_tax_monthly = income_tax_annually/12
		elif((int(ctc)>250000) and (int(ctc)<=500000)):
			rate = 0.05
			print rate
			income_tax_annually = payable_annually * rate
			income_tax_monthly = income_tax_annually/12
		elif((int(ctc)>500000) and (int(ctc)<=1000000)):
			rate = 0.2
			income_tax_annually = payable_annually * rate
			income_tax_monthly = income_tax_annually/12
		else:
			rate = 0.3
			income_tax_annually = payable_annually * rate
			income_tax_monthly = income_tax_annually/12

		print income_tax_annually
		print income_tax_monthly

   		fixed_allowance_monthly = int(ctc)/12 - total_monthly - income_tax_monthly
   		fixed_allowance_annually = int(ctc) - total_annually - income_tax_annually
   		total_monthly = int(ctc)/12 - income_tax_monthly
   		total_annually = int(ctc) - income_tax_annually
   

	resp = Response(json.dumps({"template_fixed_monthly": fixed_allowance_monthly, "template_fixed_annually": fixed_allowance_annually, "template_total_monthly": total_monthly, "template_total_annually": total_annually, "template_earning_monthly": earning_amount_monthly_all, "template_earning_annually": earning_amount_all, "template_reimbursement_monthly": reimburse_amount_monthly_all, "template_reimbursement_annually": reimburse_amount_all, "template_income_tax_monthly": income_tax_monthly, "template_income_tax_annually": income_tax_annually}))
	resp.headers['Content-type']='application/json'
	return after_request(resp)

#Save Template
@app.route('/payroll/add/payroll-v2/payment-template/',methods=['GET','POST'])
def ApiAddPaymentTemplate():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		test=[]
		
		template_name = configure_data['temp_name']
		template_description = configure_data['temp_desc']
		template_ctc = configure_data['ctc']
		
		template_earning_components = configure_data['active_earning_components']
		template_earning_monthly = ''
		test= configure_data['earning_monthly']
		print "test="
		print test
		for i in range(0, len(test)):
			template_earning_monthly= template_earning_monthly+ str(test[i])+', '
			print template_earning_monthly

		template_earning_annually = ''
		test = configure_data['earning_annually']
		for i in range(0, len(test)):
			template_earning_annually= template_earning_annually + str(test[i]) +', '
			print template_earning_annually
		
		#template_deduction_components = configure_data['active_deduction_components']
		#template_deduction_monthly = configure_data['deduction_monthly']
		#template_deduction_annually = configure_data['deduction_annually']
		
		template_reimbursement_components = configure_data['active_reimbursement_components']
		template_reimbursement_monthly = ''
		test= configure_data['reimburse_monthly']
		for i in range(0, len(test)):
			template_reimbursement_monthly= template_reimbursement_monthly+ str(test[i])+ ', '
   
		template_reimbursement_annually = ''
		test= configure_data['reimburse_annually']
		for i in range(0, len(test)):
			template_reimbursement_annually= template_reimbursement_annually+ str(test[i]) + ', '

		template_fixed_monthly = configure_data['fixed_allowance_monthly']
		template_fixed_annually = configure_data['fixed_allowance_annually']

		template_total_annually = configure_data['total_annually']
		template_total_monthly = configure_data['total_monthly']

		cmpid = configure_data['cmpid']

		print cmpid


		addPaymentTemplate = dbhelper.AddData().addPaymentTemplate( template_name, template_description, template_ctc, template_earning_components, template_earning_monthly, template_earning_annually, template_reimbursement_components, template_reimbursement_monthly, template_reimbursement_annually, template_fixed_monthly, template_fixed_annually,template_total_monthly, template_total_annually, cmpid )
		print addPaymentTemplate
		if addPaymentTemplate:
			db={'message':'Template added'}
			success = 1
		else:
			db={'message':'Template not added'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Get Payment Template List
@app.route('/payroll/get/payroll-v2/payment-templates/',methods=['GET','POST'])
def ApiGetPaymentTemplates():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		component_data = dbhelper.GetData().GetPaymentTemplates(cmpid)
		print component_data
		component_data_db=[]
		if(len(component_data))>0:
			for line in component_data:
				test_data_dict={}
				test_data_dict['temp_id']					=line[0]
				test_data_dict['temp_name']					=line[1]
				test_data_dict['temp_desc']			=line[2]

				component_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "posts":component_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get Template for drop down
@app.route('/payroll/get/payroll-v2/payment-templates-drop-down/',methods=['GET','POST'])
def ApiGetPaymentTemplatesDropDown():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		component_data = dbhelper.GetData().GetPaymentTemplatesDropDown(cmpid)
		print component_data
		component_data_db=[]
		if(len(component_data))>0:
			for line in component_data:
				test_data_dict={}
				test_data_dict['label']					=line[0]
				test_data_dict['value']					=line[1]

				component_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "posts":component_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################
#PAYSLIP TEMPLATE

#Set Default Payslip Template
#Change component active status earning

@app.route('/payroll/set-default/payroll-v2/payslip-template/',methods=['GET','POST'])
def ApiSetDefaultPayslipTemplate():
	if request.method=='GET':
		print request
		#configure_data  = json.loads(request.data)
		temp_name= request.args.get('temp_name')
		cid = request.args.get('cid')
		print cid,temp_name
		DefaultPayslipTemplate = dbhelper.UpdateData().DefaultPayslipTemplate(temp_name, cid)
		print DefaultPayslipTemplate
		if (DefaultPayslipTemplate==1):
			success= 1
			db={'Activity': 'Toggled'}
		else:
			db={'Activity': 'could not change'}
			success = 0
		
		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

@app.route('/payroll/get/payroll-v2/default-payslip-template/',methods=['GET','POST'])
def ApiGetDefaultPayslipTemplate():
	if request.method=='GET':
		print request
		#configure_data  = json.loads(request.data)
		# temp_name= request.args.get('temp_name')
		cid = request.args.get('cid')
		print cid
		DefaultPayslipTemplate = dbhelper.GetData().GetDefaultPayslipTemplate(cid)
		print DefaultPayslipTemplate
		DefaultPayslipTemplate_db=[]
		if(len(DefaultPayslipTemplate))>0:
			for line in DefaultPayslipTemplate:
				DefaultPayslipTemplate_dict={}
				DefaultPayslipTemplate_dict['DEFAULT']					=line[0]
									

				DefaultPayslipTemplate_db.append(DefaultPayslipTemplate_dict)

		resp = Response(json.dumps({"success": True, "posts":DefaultPayslipTemplate_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################
#Add Pay Schedule

@app.route('/payroll/add/payroll-v2/PaySchedule/',methods=['GET','POST'])
def ApiAddPaySchedule():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		working_days= configure_data['weekdays']
		if(configure_data['days']=='actualdays'):
			salary_basis='Actual Days in a month'
		else:
			salary_basis=configure_data['days']+' Days'

		if(configure_data['days1']=='lastday'):
			payment_date='Last Day of Month'
		else:
			payment_date=configure_data['days1']+"th of next month"
		
		cid = configure_data['cid']
		print configure_data
		print working_days
		PaySchedule = dbhelper.AddData().addPaySchedule(working_days, salary_basis, payment_date, cid)
		
		if PaySchedule:
			db={'message':'Pay Schedule added'}
			success = 1
		else:
			db={'message': 'Pay Schedule not added'}
			success = 0

		
		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Get Pay Schedule
@app.route('/payroll/get/payroll-v2/PaySchedule/',methods=['GET','POST'])
def ApiGetPaySchedule():
	if request.method =='GET':
		cid = request.args.get('cid')
		print cid
		schedule_data = dbhelper.GetData().GetPaySchedule(cid)
		print schedule_data
		schedule_data_db=[]
		if(len(schedule_data))>0:
			for line in schedule_data:
				test_data_dict={}
				test_data_dict['Salary_Basis']					=line[0]
				test_data_dict['Working_Days']					=line[1]
				test_data_dict['Payment_Date']					=line[2]
									

				schedule_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "posts":schedule_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Update Pay Schedule

@app.route('/payroll/update/payroll-v2/pay-schedule/',methods=['GET','POST'])
def ApiUpdatePaySchedule():
	if request.method=='POST':
		print 'data', request.data
		configure_data = json.loads(request.data)
		working_days= configure_data['weekdays']
		if(configure_data['days']=='actualdays'):
			salary_basis='Actual Days in a month'
		else:
			salary_basis=configure_data['days']+' Days'

		if(configure_data['days1']=='lastday'):
			payment_date='Last Day of Month'
		else:
			payment_date=configure_data['days1']+"th of next month"
		
		cid = configure_data['cid']
		UpdatePaySchedule = dbhelper.UpdateData().UpdatePaySchedule( working_days, salary_basis, payment_date, cid)

		if UpdatePaySchedule:
			db={'message': 'company could not be updated'}
			success = 0
			
		else:
			db={'message':'company updated'}
			success = 1

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

###################################################################################################

#AddTaxDetails
@app.route('/payroll/add/payroll-v2/taxDetails/',methods=['GET','POST'])
def ApiAddTaxDetails():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		pan = configure_data['pan']
		tan = configure_data['tan']
		tds_ao = configure_data['tdscircle']
		payment_frequency = configure_data['taxfreq']
		deductor_name = configure_data['deductname']
		deductor_father_name = configure_data['deductfname']
		cid= configure_data['cid']
		AddTaxDetails = dbhelper.AddData().addTaxDetails(pan, tan, tds_ao, payment_frequency, deductor_name, deductor_father_name, cid)
		if AddTaxDetails:
			db={'message':'Tax Details Added'}
			success = 1
		else:
			db={'message': 'Tax Details already exists'}
			success = 0
			
		resp = Response(json.dumps({"success": success, "datasets": db}))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get Tax Details
@app.route('/payroll/get/payroll-v2/tax-details/',methods=['GET','POST'])
def ApiGetTaxDetails():
	if request.method =='GET':
		
		empid=101
		tax_data = dbhelper.GetData().GetTaxDetails(empid)
		print tax_data
		tax_data_db=[]
		if(len(tax_data))>0:
			for line in tax_data:
				test_data_dict={}
				test_data_dict['PAN']					=line[0]
				test_data_dict['TAN']					=line[1]
				test_data_dict['TDS/AO']				=line[2]
				test_data_dict['Payment Frequency']		=line[3]
				test_data_dict['Deductor Name']			=line[4]
				test_data_dict['Deductor Father Name']	=line[5]
				test_data_dict['Company ID']			=line[6]
									

				tax_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "posts":tax_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#send otp to phone
@app.route('/payroll/add/payroll-v2/phone-verification/',methods=['GET','POST'])
def ApiPhoneVerification():
	if request.method=='POST':
		details=json.loads(request.data)
		print request.data
		#text=details['text']
		phone=details['phone']
		otp=details['otp']

		text ="Welcome to Innopayroll. Your Login OTP is %s."%(str(otp)) 
		m_phone="91"+str(phone)
		url ='http://enterprise.smsgatewaycenter.com/SMSApi/rest/send'
		querystring = {"userId":"servtrans","password":"Tgb@12345","senderId":"SERVSM","sendMethod":"simpleMsg","msgType":"text","mobile":m_phone,"msg":text,"duplicateCheck":"true","format":"json"}
		params = urllib.urlencode(querystring)
		response = urllib2.urlopen(url, params)
		json_response = json.loads(response.read())
		print json_response
		resp = Response(json.dumps({"success": True, "posts":json_response }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#generate otp
@app.route('/payroll/add/payroll-v2/otp-generator/',methods=['GET','POST'])
def ApiOtpGenerator():
	if request.method=='GET':
		otp = random.randint(0,9999)
		print otp

		resp = Response(json.dumps({"success": True, "security":otp }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################
#EMPLOYEE

#add Employee
@app.route('/payroll/add/payroll-v2/employee/',methods=['GET','POST'])
def ApiAddEmployee():
	if request.method=='POST':
		print 'data', request
		configure_data  = json.loads(request.data)
		name = configure_data['name']
		gender = configure_data['gender1']
		doj = configure_data['doj']
		desg = configure_data['desg']
		department = configure_data['department']
		company_email = configure_data['email']
		if(configure_data['portal_access']=='true'):
			portal_access=1
		else:
			portal_access=0
		if(configure_data['director']=='true'):
			substantial_interest=1
		else:
			substantial_interest=0

		branchid= configure_data['branch']
		cmpid = configure_data['cmpid']

		addEmployee = dbhelper.AddData().addEmployee(name, gender, doj, desg, department, company_email, portal_access, substantial_interest, branchid, cmpid)
		if addEmployee:
			db={'message':'employee added'}
			success = 1
			empid = addEmployee
		else:
			db={'message': 'could not add employee'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db, "employee_ID": empid}))
		return after_request(resp)

#Add Employee Personal Details
@app.route('/payroll/add/payroll-v2/employee-personal/',methods=['GET','POST'])
def ApiAddEmployeePersonalDetails():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		empid = configure_data['empid']
		email = configure_data['personalised_email']
		phone = configure_data['mobile_number']
		dob = configure_data['dob']
		guardian = configure_data['fathers_name']
		pan = configure_data['pan']
		address1 = configure_data['address1']
		address2 = configure_data['address2']
		city = configure_data['city']
		state = configure_data['state']
		pin = configure_data['pin']
		address= address1 + address2 + city + state + pin								
		cmpid = configure_data['cmpid']
		ApiAddEmployeePersonalDetails = dbhelper.AddData().addEmployeePersonalDetails(empid, email, phone, dob, guardian, pan, address, cmpid)
		if ApiAddEmployeePersonalDetails:
			db={'message':'employee personal details added'}
			success = 1
		else:
			db={'message': 'could not add employee personal details'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Add Employee Payment
@app.route('/payroll/add/payroll-v2/employee-payment/',methods=['GET','POST'])
def ApiAddEmployeePaymentDetails():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		account_holder_name = configure_data['account_holder_name']
		bank_name = configure_data['bank_name']
		account_number = configure_data['account_number']
		ifsc_code = configure_data['ifsc_code']
		account_type = configure_data['account_type']
		empid = configure_data['empid']
		cmpid = configure_data['cmpid']
		AddEmployeePaymentDetails = dbhelper.AddData().addEmployeePaymentDetails(account_holder_name, bank_name, account_number, ifsc_code, account_type, empid, cmpid)
		if AddEmployeePaymentDetails:
			db={'message':'employee payment details added'}
			success = 1
		else:
			db={'message': 'could not add employee payment details'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Employee load Salary Template
@app.route('/payroll/add/payroll-v2/employee-salary-template/',methods=['GET','POST'])
def ApiAddEmployeeSalaryTemplate():
	if request.method=='POST':
		print 'data', request
		configure_data  = json.loads(request.data)
		tempid = configure_data['tempid']
		cmpid = configure_data['cmpid']
		template = dbhelper.GetData().GetTemplateData(tempid)
		print template
		template_db={}
		if(len(template))>0:
			for line in template:
				earning_monthly=[]
				earning_annually=[]
				reimburse_monthly=[]
				reimburse_annually=[]
				template_db['template_id']							=line[0]
				template_db['template_name']						=line[1]
				template_db['template_description']					=line[2]
				template_db['template_ctc']							=line[3]
				template_db['template_earning_components']			=line[4]
				earning_monthly = line[5].strip().split(',')
				template_db['template_earning_monthly']     		=earning_monthly
				earning_annually = line[6].strip().split(',')
				template_db['template_earning_annually']     		=earning_annually
				template_db['template_reimbursement_components'] 	=line[7]
				reimburse_monthly = line[8].strip().split(',')
				template_db['template_reimbursement_monthly']     	=reimburse_monthly
				reimburse_annually = line[9].strip().split(',')
				template_db['template_reimbursement_annually']     	=reimburse_annually
				template_db['template_fixed_monthly']				=line[10]
				template_db['template_fixed_annually']				=line[11]
				template_db['template_total_monthly']				=line[12]
				template_db['template_total_annually']				=line[13]				


		earning_components_ids = (template_db['template_earning_components']).strip().split(',')
		print earning_components_ids
		earning_names = dbhelper.GetData().GetEarningName(earning_components_ids)

		template_db['earning_names']=earning_names
		
		reimbursement_components_ids = (template_db['template_reimbursement_components']).strip().split(',')
		print reimbursement_components_ids
		reimbursement_names = dbhelper.GetData().GetReimbursementName(reimbursement_components_ids)

		template_db['reimbursement_names']=reimbursement_names

		resp = Response(json.dumps({"template_data":template_db}))
		return after_request(resp)

#Employee save salary details
@app.route('/payroll/save/payroll-v2/employee-salary-details/',methods=['GET','POST'])
def ApiAddEmployeeSalaryDetails():
	if request.method=='POST':
		print 'data', request
		configure_data  = json.loads(request.data)
		tempid = configure_data['tempid']
		cmpid = configure_data['cmpid']
		empid = configure_data['empid']
		employee_ctc = configure_data['ctc']
		#employee_earning_monthly = configure_data['template_earning_monthly']
		employee_earning_monthly = ''
		test= configure_data['template_earning_monthly']
		print "test="
		print test
		for i in range(0, len(test)):
			employee_earning_monthly= employee_earning_monthly+ str(test[i])+', '

		#employee_earning_annually = configure_data['template_earning_annually']
		employee_earning_annually = ''
		test= configure_data['template_earning_annually']
		print "test="
		print test
		for i in range(0, len(test)):
			employee_earning_annually= employee_earning_annually+ str(test[i])+', '
		#employee_reimbursement_monthly = configure_data['template_reimbursement_monthly']
		employee_reimbursement_monthly = ''
		test= configure_data['template_reimbursement_monthly']
		print "test="
		print test
		for i in range(0, len(test)):
			employee_reimbursement_monthly= employee_reimbursement_monthly+ str(test[i])+', '
		#employee_reimbursement_annually = configure_data['template_reimbursement_annually']
		employee_reimbursement_annually = ''
		test= configure_data['template_reimbursement_annually']
		print "test="
		print test
		for i in range(0, len(test)):
			employee_reimbursement_annually= employee_reimbursement_annually+ str(test[i])+', '
		employee_fixed_monthly= configure_data['template_fixed_monthly']
		employee_fixed_annually = configure_data['template_fixed_annually']
		employee_total_monthly = configure_data['template_total_monthly']
		employee_total_annually = configure_data['template_total_annually']
		AddEmployeeSalaryDetails = dbhelper.AddData().addEmployeeSalaryDetails(tempid, employee_ctc, empid, cmpid, employee_earning_monthly, employee_reimbursement_monthly, employee_earning_annually, employee_reimbursement_annually, employee_fixed_monthly, employee_fixed_annually, employee_total_monthly, employee_total_annually)
		if AddEmployeeSalaryDetails:
			db = {"message":"Added"}
			updateBNS = dbhelper.UpdateData().UpdateBNS(str(int(employee_ctc)/12), employee_total_monthly, cmpid, empid)
			success=1
		else:
			db = {"message":"Not added"}
			success=0


		resp = Response(json.dumps({"success":success, "datasets": db}))
		return after_request(resp)

#Get Employee Info
@app.route('/payroll/get/payroll-v2/employees-info/',methods=['GET','POST'])
def ApiGetEmployeeInfo():
	if request.method =='GET':
		empid = request.args.get('empid')
		print empid
		employee_data = dbhelper.GetData().GetEmployeeInfo(empid)
		print employee_data
		employee_data_db=[]
		if(len(employee_data))>0:
			for line in employee_data:
				test_data_dict={}
				test_data_dict['name']					=line[0]
				test_data_dict['id']					=line[1]
				test_data_dict['desg']					=line[2]
				test_data_dict['email']					=line[3]
				test_data_dict['gender']				=line[4]
				test_data_dict['doj']					=line[5]
				test_data_dict['branchid']				=line[6]
				test_data_dict['deptid']				=line[7]
				test_data_dict['company_id']			=line[8]
				if(line[9]==0):
					test_data_dict['portal_access']		='Disabled'
				else:
					test_data_dict['portal_access']		='Enabled'
				
				test_data_dict['branch']			= dbhelper.GetData().GetBranchName(test_data_dict['branchid'])
				test_data_dict['department']		= dbhelper.GetData().GetDepartmentName(test_data_dict['deptid'])					

				employee_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "posts":employee_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get Employee Personal Details
@app.route('/payroll/get/payroll-v2/employees-personal/',methods=['GET','POST'])
def ApiGetEmployeePersonalInfo():
	if request.method =='GET':
		empid = request.args.get('empid')
		print empid
		employee_data = dbhelper.GetData().GetEmployeePersonal(empid)
		print employee_data
		employee_data_db=[]
		if(len(employee_data))>0:
			for line in employee_data:
				test_data_dict={}
				test_data_dict['info_id']					=line[0]
				test_data_dict['personal_email']			=line[1]
				test_data_dict['personal_phone']			=line[2]
				test_data_dict['dob']						=line[3]
				test_data_dict['fathers_name']				=line[4]
				test_data_dict['pan']						=line[5]
				test_data_dict['personal_address']			=line[6]
				test_data_dict['employee_id']				=line[7]
				test_data_dict['company_id']				=line[8]
				
				

				employee_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "details":employee_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get Employee Payment Details
@app.route('/payroll/get/payroll-v2/employees-payment/',methods=['GET','POST'])
def ApiGetEmployeePaymentInfo():
	if request.method =='GET':
		empid = request.args.get('empid')
		print empid
		employee_data = dbhelper.GetData().GetEmployeePayment(empid)
		print employee_data
		employee_data_db=[]
		if(len(employee_data))>0:
			for line in employee_data:
				test_data_dict={}
				test_data_dict['info_id']						=line[0]
				test_data_dict['account_holder_name']			=line[1]
				test_data_dict['bank_name']						=line[2]
				test_data_dict['account_number']				=line[3]
				test_data_dict['ifsc_code']						=line[4]
				test_data_dict['account_type']					=line[5]
				test_data_dict['employee_id']					=line[6]
				test_data_dict['company_id']					=line[7]
				
				

				employee_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "info":employee_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)


#Get All Empoyees
@app.route('/payroll/get/payroll-v2/all-employees/',methods=['GET','POST'])
def ApiGetAllEmployee():
	if request.method =='GET':
		userid = request.args.get('userid')
		cmpid = request.args.get('cmpid')
		print userid
		print cmpid
		employee_data = dbhelper.GetData().GetAllEmployees(userid,cmpid)
		print employee_data
		employee_data_db=[]
		if(len(employee_data))>0:
			for line in employee_data:
				test_data_dict={}
				test_data_dict['id']					=line[0]
				test_data_dict['name']					=line[1]
				test_data_dict['gender']				=line[2]
				test_data_dict['email']					=line[3]
				test_data_dict['designation']			=line[4]
				
									

				employee_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "posts":employee_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################

#image upload
@app.route('/payroll/profile/upload/',methods=['GET','POST'])
def apiprofileUpload():
	if request.method=='POST':
		file_object = request.files['file']

		BUCKET_NAME = 'lotus-1193.appspot.com'
		storage = googleapiclient.discovery.build('storage', 'v1')

		print '**',file_object, type(file_object)
		GCS_UPLOAD_FOLDER = 'Profile' 

		filename = file_object.filename
		print filename
		string_io_file = StringIO.StringIO(file_object.stream.read())

		fullName = GCS_UPLOAD_FOLDER + '/'+ filename
		print fullName
		body = {
		'name': fullName,
		}
		url='https://storage.cloud.google.com/lotus-1193.appspot.com/Profile/'+filename
		req = storage.objects().insert(bucket=BUCKET_NAME, body=body, media_body=googleapiclient.http.MediaIoBaseUpload(string_io_file, 'application/octet-stream'))
		response = req.execute()
		resp = Response(json.dumps({"success": True, "datasets": 'Image Upload Complete', "URL": url}))
		return after_request(resp) 

###################################################################################################
#PAYSLIP

#Get Payslip Data
@app.route('/payroll/get/payroll-v2/payslip-data/',methods=['GET','POST'])
def ApiGetPayslipData():
	if request.method =='GET':
		empid = request.args.get('empid')
		cmpid = request.args.get('cmpid')
		print empid
		print cmpid
		payslip_data = dbhelper.GetData().GetPayslipDataCompany(empid, cmpid)
		print payslip_data
		payslip_data_db=[]
		payslip_data_dict={}
		if(len(payslip_data))>0:
			for line in payslip_data:

				payslip_data_dict['COMPANY_NAME']					=line[0]
				payslip_data_dict['COMPANY_ADDRESS']				=line[1]
				

		payslip_data = dbhelper.GetData().GetPayslipDataEmployee(empid, cmpid)
		print payslip_data
		if(len(payslip_data))>0:
			for line in payslip_data:

				payslip_data_dict['EMPLOYEE_NAME']					=line[0]
				payslip_data_dict['EMPLOYEE_DESG']					=line[1]							
				payslip_data_dict['EMPLOYEE_DOJ']					=line[2]
				
				
		payslip_data_db.append(payslip_data_dict)
		print payslip_data_db
		resp = Response(json.dumps({"success": True, "posts":payslip_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################
#SHIFTS

#add shifts
@app.route('/payroll/add/payroll-v2/shifts/',methods=['GET','POST'])
def ApiAddShift():
	if request.method=='POST':
		print 'data', request
		configure_data  = json.loads(request.data)
		
		shift_name = configure_data['shift_name']
		shift_code = configure_data['shift_code']
		shift_type = configure_data['shift_type']
		time_in = configure_data['time_in']
		time_out = configure_data['time_out']
		late_mark_upto_half_day_absent = configure_data['late_mark_upto_half_day_absent']
		in_time_for_full_absent = configure_data['in_time_for_full_absent']
		grace_in_time = configure_data['grace_in_time']
		grace_out_time = configure_data['grace_out_time']
		time_out_for_full_day_absent = configure_data['time_out_for_full_day_absent']
		early_leaving_upto_half_day = configure_data['early_leaving_upto_half_day']
		in_cut_off = configure_data['in_cut_off']
		break_start = configure_data['break_start']
		break_end = configure_data['break_end']
		gravity_shift_max = configure_data['gravity_shift_max']
		is_gravity_shift = configure_data['gravity_check']
		is_half_day = configure_data['half_day']
		cmpid = configure_data['cmpid']

		shift = dbhelper.AddData().addShift(shift_name, shift_type, shift_code, time_in, time_out, late_mark_upto_half_day_absent, in_time_for_full_absent, grace_in_time, grace_out_time, time_out_for_full_day_absent, early_leaving_upto_half_day, in_cut_off, break_start, break_end, gravity_shift_max, is_gravity_shift, is_half_day, cmpid)
		if shift:
			db={'message':'Shift added'}
			success = 1
			
		else:
			db={'message': 'could not add shift'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#get shifts
@app.route('/payroll/get/payroll-v2/shifts/',methods=['GET','POST'])
def ApiGetShifts():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		shift_data = dbhelper.GetData().getShifts(cmpid)
		print shift_data
		shift_data_db=[]
		if(len(shift_data))>0:
			for line in shift_data:
				test_data_dict={}
				test_data_dict['shift_id']					=line[0]
				test_data_dict['shift_name']				=line[1]
				test_data_dict['shift_type']				=line[2]
				test_data_dict['shift_code']				=line[3]
				test_data_dict['time_in']					=line[4]
				test_data_dict['time_out']					=line[5]
									

				shift_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "posts":shift_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get Shift Drop-down
@app.route('/payroll/get/payroll-v2/shifts-drop-down/',methods=['GET','POST'])
def ApiGetShiftsDropDown():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		shift_data = dbhelper.GetData().getShiftsDropDown(cmpid)
		print shift_data
		shift_data_db=[]
		if(len(shift_data))>0:
			for line in shift_data:
				test_data_dict={}
				test_data_dict['label']					=line[0]
				test_data_dict['value']					=line[1]
									
									
				shift_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "posts":shift_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#delete shifts
@app.route('/payroll/delete/payroll-v2/shift/',methods=['GET','POST','DELETE'])
def ApiDeleteShift():
	if request.method=='DELETE':
		print 'data', request.data
		sid= request.args.get('sid')
		deleteShift = dbhelper.DeleteData().deleteShift(sid)
		if deleteShift:
			db={'message':'Shift Deleted'}
			success = 1
		else:
			db={'message': 'Shift could not be deleted'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

# #Input list and put into data table
# @app.route('/payroll/add/payroll-v2/read-csv/',methods=['GET','POST'])
# def ApiReadCSV():
# 	if request.method=='POST':
# 		print 'data', request
# 		configure_data  = json.loads(request.data)
# 		print configure_data
# 		array = []
# 		array = configure_data['array']
# 		rows=[]
# 		for i in range(1,len(array)):
# 			row=[]
# 			for j in range(0,len(array[i])):
# 				row.append(array[i][j])
# 			rows.append(row)
# 		# addRow = dbhelper.AddData().addCSV()
			
# 		resp = Response(json.dumps({"rows": rows}))
# 		return after_request(resp)

#Get Shift Details
@app.route('/payroll/get/payroll-v2/shift-details/',methods=['GET','POST'])
def ApiGetShiftDetails():
	if request.method =='GET':
		shiftid = request.args.get('shiftid')
		print shiftid
		shift_data = dbhelper.GetData().GetShiftDetails(shiftid)
		print shift_data
		shift_data_db=[]
		if(len(shift_data))>0:
			for line in shift_data:
				test_data_dict={}
				test_data_dict['shift_name']					=line[0]
				test_data_dict['shift_type']					=line[1]
				test_data_dict['shift_code']					=line[2]
				test_data_dict['time_in']						=line[3]
				test_data_dict['time_out']						=line[4]
				test_data_dict['grace_in_time']					=line[5]
				test_data_dict['grace_out_time']				=line[6]
				
				
									

				shift_data_db.append(test_data_dict)

		resp = Response(json.dumps({"success": True, "posts":shift_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Edit
@app.route('/payroll/edit/payroll-v2/shifts/',methods=['GET','POST'])
def ApiUpdateShift():
	if request.method=='POST':
		print 'data', request
		configure_data  = json.loads(request.data)
		shiftid = configure_data['shiftid']
		shift_name = configure_data['shift_name']
		shift_code = configure_data['shift_code']
		shift_type = configure_data['shift_type']
		time_in = configure_data['time_in']
		time_out = configure_data['time_out']
		late_mark_upto_half_day_absent = configure_data['late_mark_upto_half_day_absent']
		in_time_for_full_absent = configure_data['in_time_for_full_absent']
		grace_in_time = configure_data['grace_in_time']
		grace_out_time = configure_data['grace_out_time']
		time_out_for_full_day_absent = configure_data['time_out_for_full_day_absent']
		early_leaving_upto_half_day = configure_data['early_leaving_upto_half_day']
		in_cut_off = configure_data['in_cut_off']
		break_start = configure_data['break_start']
		break_end = configure_data['break_end']
		gravity_shift_max = configure_data['gravity_shift_max']
		is_gravity_shift = configure_data['gravity_check']
		is_half_day = configure_data['half_day']
		cmpid = configure_data['cmpid']

		shift = dbhelper.UpdateData().UpdateShift(shiftid, shift_name, shift_type, shift_code, time_in, time_out, late_mark_upto_half_day_absent, in_time_for_full_absent, grace_in_time, grace_out_time, time_out_for_full_day_absent, early_leaving_upto_half_day, in_cut_off, break_start, break_end, gravity_shift_max, is_gravity_shift, is_half_day, cmpid)
		if shift:
			db={'message':'Shift Updated'}
			success = 1
			
		else:
			db={'message': 'could not Update shift'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Get Edit
@app.route('/payroll/get-edit/payroll-v2/shifts/',methods=['GET','POST'])
def ApiEditShift():
	if request.method=='GET':
		print 'data', request
		sid= request.args.get('sid')
		print sid
		shift_data = dbhelper.UpdateData().EditShift(sid)
		shift_data_db=[]
		if(len(shift_data))>0:
			for line in shift_data:
				test_data_dict={}				
				test_data_dict['shift_id']											=line[0]
				test_data_dict['shift_type']										=line[1]
				test_data_dict['shift_code']										=line[2]
				test_data_dict['shift_name']										=line[3]
				test_data_dict['time_in']											=line[4]
				test_data_dict['time_out']											=line[5]
				test_data_dict['late_mark_upto_half_day_absent']					=line[6]
				test_data_dict['in_time_for_full_absent']							=line[7]
				test_data_dict['grace_in_time']										=line[8]
				test_data_dict['grace_out_time']									=line[9]
				test_data_dict['time_out_for_full_day_absent']						=line[10]
				test_data_dict['early_leaving_upto_half_day']						=line[11]
				test_data_dict['in_cut_off']										=line[12]
				test_data_dict['break_start']										=line[13]
				test_data_dict['break_end']											=line[14]
				test_data_dict['gravity_shift_max']									=line[15]
				test_data_dict['is_gravity_shift']									=line[16]
				test_data_dict['is_half_day']										=line[17]
				test_data_dict['company_id']										=line[18]

				
									

				shift_data_db.append(test_data_dict)

		resp = Response(json.dumps({"posts":shift_data_db}))
		return after_request(resp)

###################################################################################################
#PAYRUN_REVIEW_BNS

#API Bonus & Salary Revision
@app.route('/payroll/get/payroll-v2/bonus-salary-revision/',methods=['GET','POST'])
def ApiBonusSalaryRevision():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		idnos = dbhelper.GetData().GetEmployeeID(cmpid)
		print idnos
		payrun_data_db=[]
		for i in range(0, len(idnos)):
			
			employee_data = dbhelper.GetData().GetBNS(idnos[i])
			print employee_data
			payrun_data_dict={}
			if(len(employee_data))>0:
				for line in employee_data:

					payrun_data_dict['EMPLOYEE_ID']					=line[0]
					payrun_data_dict['EMPLOYEE_NAME']				=line[1]
					payrun_data_dict['MONTH']						=line[2]
					payrun_data_dict['GUARANTEED_CTC']				=line[3]
					payrun_data_dict['NET_SALARY']					=line[4]
					payrun_data_dict['BONUS']						=line[5]
					payrun_data_dict['EFFECTIVE_FROM']				=line[6]

					payrun_data_db.append(payrun_data_dict)
		
		print payrun_data_db
		resp = Response(json.dumps({"success": True, "posts":payrun_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get BNS employee detail to edit
@app.route('/payroll/get/payroll-v2/edit-bns/',methods=['GET','POST'])
def ApiGetEditableBNS():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		print cmpid, empid
		BNSDetails = dbhelper.GetData().GetEditableBNS(cmpid, empid)
		print BNSDetails
		payrun_data_db=[]
		if(len(BNSDetails))>0:
			for line in BNSDetails:
				payrun_data_dict={}
				payrun_data_dict['EMPLOYEE_ID']					=line[0]
				payrun_data_dict['EMPLOYEE_NAME']				=line[1]
				payrun_data_dict['GUARANTEED_CTC']				=line[2]
				payrun_data_dict['NET_SALARY']					=line[3]
				payrun_data_dict['BONUS']						=line[4]
				payrun_data_dict['EFFECTIVE_FROM']				=line[5]

				payrun_data_db.append(payrun_data_dict)
		
		resp = Response(json.dumps({"success": True, "Datasets": payrun_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Update BNS
@app.route('/payroll/update/payroll-v2/bns/',methods=['GET','POST'])
def ApiUpdateBNS():
	if request.method=='POST':
		print 'data', request
		configure_data  = json.loads(request.data)
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		guaranteed_ctc = configure_data['guaranteed_ctc']
		effective_from = configure_data['effective_from']
		net_salary = configure_data['salary']
		bonus = configure_data['bonus']
		UpdateBNS = dbhelper.UpdateData().UpdateBNSdata(cmpid, empid, guaranteed_ctc, effective_from, net_salary, bonus)
		if UpdateBNS:
			db={'message':'Update added'}
			success = 1
			
		else:
			db={'message': 'could not add Update'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Delete from BNS
@app.route('/payroll/delete/payroll-v2/bns/',methods=['GET','POST','DELETE'])
def ApiDeleteBNS():
	if request.method=='DELETE':
		print 'data', request
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		DeleteBNS = dbhelper.DeleteData().DeleteBNSRow(cmpid, empid)
		if DeleteBNS:
			db={'message':'row deleted'}
			success = 1	
		else:
			db={'message': 'row not deleted'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Lock BNS
@app.route('/payroll/lock/payroll-v2/BNS/',methods=['GET','POST'])
def ApiLockBNS():
	if request.method=='POST':
		print request
		cmpid = request.args.get('cmpid')
		BNSlock = dbhelper.UpdateData().BNSlock(cmpid)
  		if BNSlock:
			db={'message':'Table Locked'}
			success = 1
		else:
			db={'message': 'Table Not Locked'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Get BNS Lock
@app.route('/payroll/get/payroll-v2/BNS-lock/',methods=['GET','POST'])
def ApiBNSLock():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		lock_status = dbhelper.GetData().GetBNSLock(cmpid)
		if (lock_status==1):
			status= True
		else:
			status = False
		
		resp = Response(json.dumps({"success": True, "status":status }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

######################################################################################################################################
#ONE_TIME PND

#GET PAYMENTS
@app.route('/payroll/get/payroll-v2/pnd-payments/',methods=['GET','POST'])
def ApiPNDpayments():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		idnos = dbhelper.GetData().GetEmployeeID(cmpid)
		print idnos
		payrun_data_db=[]
		for i in range(0, len(idnos)):
			
			employee_data = dbhelper.GetData().GetPNDPayments(idnos[i])
			print employee_data
			payrun_data_dict={}
			if(len(employee_data))>0:
				for line in employee_data:

					payrun_data_dict['EMPLOYEE_ID']					=line[0]
					payrun_data_dict['EMPLOYEE_NAME']				=line[1]
					payrun_data_dict['MONTH']						=line[2]
					payrun_data_dict['PAYMENT_AMOUNT']				=line[3]
					payrun_data_dict['PAYMENT_TYPE']				=line[4]
					payrun_data_dict['PAYMENT_COMMENT']				=line[5]

					payrun_data_db.append(payrun_data_dict)
		
		print payrun_data_db
		resp = Response(json.dumps({"success": True, "payments":payrun_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#GET DEDUCTIONS
@app.route('/payroll/get/payroll-v2/pnd-deductions/',methods=['GET','POST'])
def ApiPNDDeduction():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		idnos = dbhelper.GetData().GetEmployeeID(cmpid)
		print idnos
		payrun_data_db=[]
		for i in range(0, len(idnos)):
			
			employee_data = dbhelper.GetData().GetPNDDeductions(idnos[i])
			print employee_data
			payrun_data_dict={}
			if(len(employee_data))>0:
				for line in employee_data:

					payrun_data_dict['EMPLOYEE_ID']					=line[0]
					payrun_data_dict['EMPLOYEE_NAME']				=line[1]
					payrun_data_dict['MONTH']						=line[2]
					payrun_data_dict['DEDUCTION_AMOUNT']			=line[3]
					payrun_data_dict['DEDUCTION_TYPE']				=line[4]
					payrun_data_dict['DEDUCTION_COMMENT']			=line[5]

					payrun_data_db.append(payrun_data_dict)
		
		print payrun_data_db
		resp = Response(json.dumps({"success": True, "deducts":payrun_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get PND Payments detail to edit
@app.route('/payroll/get/payroll-v2/edit-pnd-payments/',methods=['GET','POST'])
def ApiGetEditablePNDPayments():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		print cmpid, empid
		BNSDetails = dbhelper.GetData().GetEditablePNDPayments(cmpid, empid)
		print BNSDetails
		payrun_data_db=[]
		if(len(BNSDetails))>0:
			for line in BNSDetails:
				payrun_data_dict={}
				payrun_data_dict['EMPLOYEE_ID']					=line[0]
				payrun_data_dict['EMPLOYEE_NAME']				=line[1]
				payrun_data_dict['PAYMENT_AMOUNT']				=line[2]
				payrun_data_dict['PAYMENT_TYPE']				=line[3]
				payrun_data_dict['PAYMENT_COMMENT']				=line[4]

				payrun_data_db.append(payrun_data_dict)
		
		resp = Response(json.dumps({"success": True, "payments": payrun_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get PND  detail to edit
@app.route('/payroll/get/payroll-v2/edit-pnd-deductions/',methods=['GET','POST'])
def ApiGetEditablePNDDeductions():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		print cmpid, empid
		BNSDetails = dbhelper.GetData().GetEditablePNDDeductions(cmpid, empid)
		print BNSDetails
		payrun_data_db=[]
		if(len(BNSDetails))>0:
			for line in BNSDetails:
				payrun_data_dict={}
				payrun_data_dict['EMPLOYEE_ID']					=line[0]
				payrun_data_dict['EMPLOYEE_NAME']				=line[1]
				payrun_data_dict['DEDUCTION_AMOUNT']			=line[2]
				payrun_data_dict['DEDUCTION_TYPE']				=line[3]
				payrun_data_dict['DEDUCTION_COMMENT']			=line[4]

				payrun_data_db.append(payrun_data_dict)
		
		resp = Response(json.dumps({"success": True, "deducts": payrun_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Update PND Payments
@app.route('/payroll/update/payroll-v2/pnd-payments/',methods=['GET','POST'])
def ApiUpdatePNDPayments():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		payment_amount = configure_data['payment_amount']
		payment_type = configure_data['payment_type']
		payment_comment = configure_data['payment_comment']
		UpdateBNS = dbhelper.UpdateData().UpdatePNDPayments(cmpid, empid, payment_amount, payment_type, payment_comment)
		if UpdateBNS:
			db={'message':'Update added'}
			success = 1
			
		else:
			db={'message': 'could not add Update'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Update PND Deductions
@app.route('/payroll/update/payroll-v2/pnd-deductions/',methods=['GET','POST'])
def ApiUpdatePNDDeductions():
	if request.method=='POST':
		print 'data', request
		configure_data  = json.loads(request.data)
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		deduction_amount = configure_data['deduction_amount']
		deduction_type = configure_data['deduction_type']
		deduction_comment = configure_data['deduction_comment']
		UpdateBNS = dbhelper.UpdateData().UpdatePNDDeductions(cmpid, empid, deduction_amount, deduction_type, deduction_comment)
		if UpdateBNS:
			db={'message':'Update added'}
			success = 1
			
		else:
			db={'message': 'could not add Update'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Delete from PND
@app.route('/payroll/delete/payroll-v2/pnd/',methods=['GET','POST','DELETE'])
def ApiDeletePND():
	if request.method=='DELETE':
		print 'data', request
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		DeleteBNS = dbhelper.DeleteData().DeletePNDRow(cmpid, empid)
		if DeleteBNS:
			db={'message':'row deleted'}
			success = 1	
		else:
			db={'message': 'row not deleted'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Lock PND
@app.route('/payroll/lock/payroll-v2/PND/',methods=['GET','POST'])
def ApiLockPND():
	if request.method=='POST':
		print request
		cmpid = request.args.get('cmpid')
		BNSlock = dbhelper.UpdateData().PNDlock(cmpid)
  		if BNSlock:
			db={'message':'Table Locked'}
			success = 1
		else:
			db={'message': 'Table Not Locked'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Get PND Lock
@app.route('/payroll/get/payroll-v2/PND-lock/',methods=['GET','POST'])
def ApiPNDLock():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		lock_status = dbhelper.GetData().GetPNDLock(cmpid)
		if (lock_status==1):
			status= True
		else:
			status = False
		
		resp = Response(json.dumps({"success": True, "status":status }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################
#SALARY HOLD AND ARREARS

#GET DATA

@app.route('/payroll/get/payroll-v2/salary-hold-arrears/',methods=['GET','POST'])
def ApiSHApayments():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		idnos = dbhelper.GetData().GetEmployeeID(cmpid)
		print idnos
		payrun_data_db=[]
		for i in range(0, len(idnos)):
			
			employee_data = dbhelper.GetData().GetSHATable(idnos[i])
			print employee_data
			payrun_data_dict={}
			if(len(employee_data))>0:
				for line in employee_data:

					payrun_data_dict['EMPLOYEE_ID']					=line[0]
					payrun_data_dict['EMPLOYEE_NAME']				=line[1]
					payrun_data_dict['MONTH']						=line[2]
					payrun_data_dict['SALARY_HOLD_PAY_AMOUNT']		=line[3]
					payrun_data_dict['SALARY_HOLD_PAY_CYCLE']		=line[4]
					payrun_data_dict['SALARY_HOLD_ACTION']			=line[5]
					payrun_data_dict['SALARY_HOLD_COMMENT']			=line[6]
     
					payrun_data_db.append(payrun_data_dict)
		
		print payrun_data_db
		resp = Response(json.dumps({"success": True, "payments":payrun_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get SHA detail to edit
@app.route('/payroll/get/payroll-v2/edit-sha/',methods=['GET','POST'])
def ApiGetEditableSHA():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		print cmpid, empid
		BNSDetails = dbhelper.GetData().GetEditableSHA(cmpid, empid)
		print BNSDetails
		payrun_data_db=[]
		if(len(BNSDetails))>0:
			for line in BNSDetails:
				payrun_data_dict={}
				payrun_data_dict['EMPLOYEE_ID']					=line[0]
				payrun_data_dict['EMPLOYEE_NAME']				=line[1]
				payrun_data_dict['SALARY_HOLD_PAY_AMOUNT']		=line[2]
				payrun_data_dict['SALARY_HOLD_PAY_CYCLE']		=line[3]
				payrun_data_dict['SALARY_HOLD_ACTION']			=line[4]
				payrun_data_dict['SALARY_HOLD_COMMENT']			=line[5]

				payrun_data_db.append(payrun_data_dict)
		
		resp = Response(json.dumps({"success": True, "payments": payrun_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Update SHA
@app.route('/payroll/update/payroll-v2/salary-hold-arrears/',methods=['GET','POST'])
def ApiUpdateSHA():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		payment_amount = configure_data['pay_amount']
		payment_cycle= configure_data['pay_cycle']
		payment_action = configure_data['action']
		payment_comment= configure_data['pay_comment']
		UpdateBNS = dbhelper.UpdateData().UpdateSHA(cmpid, empid, payment_amount, payment_cycle, payment_action, payment_comment)
		if UpdateBNS:
			db={'message':'Update added'}
			success = 1
			
		else:
			db={'message': 'could not add Update'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Delete from SHA
@app.route('/payroll/delete/payroll-v2/sha/',methods=['GET','POST','DELETE'])
def ApiDeleteSHA():
	if request.method=='DELETE':
		print 'data', request
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		DeleteBNS = dbhelper.DeleteData().DeleteSHARow(cmpid, empid)
		if DeleteBNS:
			db={'message':'row deleted'}
			success = 1	
		else:
			db={'message': 'row not deleted'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Lock SHA
@app.route('/payroll/lock/payroll-v2/SHA/',methods=['GET','POST'])
def ApiLockSHA():
	if request.method=='POST':
		print request
		cmpid = request.args.get('cmpid')
		BNSlock = dbhelper.UpdateData().SHAlock(cmpid)
  		if BNSlock:
			db={'message':'Table Locked'}
			success = 1
		else:
			db={'message': 'Table Not Locked'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Get SHA Lock
@app.route('/payroll/get/payroll-v2/sha-lock/',methods=['GET','POST'])
def ApiSHALock():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		lock_status = dbhelper.GetData().GetSHALock(cmpid)
		if (lock_status==1):
			status= True
		else:
			status = False
		
		resp = Response(json.dumps({"success": True, "status":status }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################
#Review All Employees
@app.route('/payroll/get/payroll-v2/review-all/',methods=['GET','POST'])
def ApiReviewAll():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		idnos = dbhelper.GetData().GetEmployeeID(cmpid)
		print idnos
		payrun_data_db=[]
		for i in range(0, len(idnos)):
			
			employee_data = dbhelper.GetData().GetReviewTable(idnos[i])
			print employee_data
			payrun_data_dict={}
			if(len(employee_data))>0:
				for line in employee_data:

					payrun_data_dict['EMPLOYEE_ID']					=line[0]
					payrun_data_dict['EMPLOYEE_NAME']				=line[1]
					payrun_data_dict['MONTH']						=line[2]
					payrun_data_dict['LOP_DAYS']					=line[3]
					payrun_data_dict['GROSS_PAY']					=line[4]
					payrun_data_dict['PAYABLE_DAYS']				=line[5]
					payrun_data_dict['LEAVE_REASON']				=line[6]
					payrun_data_dict['LEAVE_DETAILS'] 				=line[7]



     
					payrun_data_db.append(payrun_data_dict)
		
		print payrun_data_db
		resp = Response(json.dumps({"success": True, "review":payrun_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get Review detail to edit
@app.route('/payroll/get/payroll-v2/edit-review/',methods=['GET','POST'])
def ApiGetEditableReview():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		print cmpid, empid
		BNSDetails = dbhelper.GetData().GetEditableReview(cmpid, empid)
		print BNSDetails
		payrun_data_db=[]
		if(len(BNSDetails))>0:
			for line in BNSDetails:
				payrun_data_dict={}
				payrun_data_dict['EMPLOYEE_ID']					=line[0]
				payrun_data_dict['EMPLOYEE_NAME']				=line[1]
				payrun_data_dict['LOP_DAYS']					=line[2]
				payrun_data_dict['GROSS_PAY']					=line[3]
				payrun_data_dict['PAYABLE_DAYS']				=line[4]
				payrun_data_dict['LEAVE_REASON']				=line[5]
				payrun_data_dict['LEAVE_DETAILS'] 				=line[6]

				payrun_data_db.append(payrun_data_dict)
		
		resp = Response(json.dumps({"success": True, "datasets": payrun_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Update Review
@app.route('/payroll/update/payroll-v2/review/',methods=['GET','POST'])
def ApiUpdateReview():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		gross_pay = configure_data['gross_pay']
		lop_days  = configure_data['lop_days']
		payable_days = configure_data['payable_days']
		leave_reason = configure_data['leave_reason']
		leave_details = configure_data['leave_details']
		UpdateBNS = dbhelper.UpdateData().UpdateReview(cmpid, empid, lop_days,gross_pay, payable_days, leave_reason, leave_details)
		if UpdateBNS:
			db={'message':'Update added'}
			success = 1
			
		else:
			db={'message': 'could not add Update'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Delete from Review
@app.route('/payroll/delete/payroll-v2/review/',methods=['GET','POST','DELETE'])
def ApiDeleteReview():
	if request.method=='DELETE':
		print 'data', request
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		DeleteBNS = dbhelper.DeleteData().DeleteSHARow(cmpid, empid)
		if DeleteBNS:
			db={'message':'row deleted'}
			success = 1	
		else:
			db={'message': 'row not deleted'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Lock Review
@app.route('/payroll/lock/payroll-v2/REVIEW/',methods=['GET','POST'])
def ApiLockReview():
	if request.method=='POST':
		print request
		cmpid = request.args.get('cmpid')
		BNSlock = dbhelper.UpdateData().Reviewlock(cmpid)
  		if BNSlock:
			db={'message':'Table Locked'}
			success = 1
		else:
			db={'message': 'Table Not Locked'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Get Review Lock
@app.route('/payroll/get/payroll-v2/review-lock/',methods=['GET','POST'])
def ApiReviewLock():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		lock_status = dbhelper.GetData().GetReviewLock(cmpid)
		if (lock_status==1):
			status= True
		else:
			status = False
		
		resp = Response(json.dumps({"success": True, "status":status }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################

#Leave and Attendance Table
@app.route('/payroll/get/payroll-v2/leave-and-attendance/',methods=['GET','POST'])
def ApiLeaveAttendance():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		idnos = dbhelper.GetData().GetEmployeeID(cmpid)
		print idnos
		payrun_data_db=[]
		for i in range(0, len(idnos)):
			
			employee_data = dbhelper.GetData().GetLeaveTable(idnos[i])
			print employee_data
			payrun_data_dict={}
			if(len(employee_data))>0:
				for line in employee_data:

					payrun_data_dict['EMPLOYEE_ID']					=line[0]
					payrun_data_dict['EMPLOYEE_NAME']				=line[1]
					payrun_data_dict['MONTH']						=line[2]
					payrun_data_dict['WORKING_DAYS']				=line[3]
					payrun_data_dict['PRESENT_DAYS']				=line[4]
					payrun_data_dict['TOTAL_LEAVE']					=line[5]
					payrun_data_dict['TYPE_OF_LEAVE']				=line[6]
					payrun_data_dict['LEAVE_DEDUCTIONS'] 			=line[7]



     
					payrun_data_db.append(payrun_data_dict)
		
		print payrun_data_db
		resp = Response(json.dumps({"success": True, "leave":payrun_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

#Get Leave detail to edit
@app.route('/payroll/get/payroll-v2/edit-Leave/',methods=['GET','POST'])
def ApiGetEditableLeave():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		print cmpid, empid
		BNSDetails = dbhelper.GetData().GetEditableLeave(cmpid, empid)
		print BNSDetails
		payrun_data_db=[]
		if(len(BNSDetails))>0:
			for line in BNSDetails:
				payrun_data_dict={}
				payrun_data_dict['EMPLOYEE_ID']					=line[0]
				payrun_data_dict['EMPLOYEE_NAME']				=line[1]
				payrun_data_dict['WORKING_DAYS']				=line[2]
				payrun_data_dict['PRESENT_DAYS']				=line[3]
				payrun_data_dict['TOTAL_LEAVE']					=line[4]
				payrun_data_dict['TYPE_OF_LEAVE']				=line[5]
				payrun_data_dict['LEAVE_DEDUCTIONS'] 			=line[6]


				payrun_data_db.append(payrun_data_dict)
		
		resp = Response(json.dumps({"success": True, "datasets": payrun_data_db }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

@app.route('/payroll/update/payroll-v2/leave/',methods=['GET','POST'])
def ApiUpdateLeave():
	if request.method=='POST':
		print 'data', request.data
		configure_data  = json.loads(request.data)
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		working_days = configure_data['working_days']
		present_days  = configure_data['present_days']
		total_leave = configure_data['total_leave']
		type_of_leave = configure_data['type_of_leave']
		leave_deductions = configure_data['leave_deductions']
		UpdateBNS = dbhelper.UpdateData().UpdateLeave(cmpid, empid, working_days,present_days, total_leave, type_of_leave, leave_deductions)
		if UpdateBNS:
			db={'message':'Update added'}
			success = 1
			
		else:
			db={'message': 'could not add Update'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Delete from leave
@app.route('/payroll/delete/payroll-v2/leave/',methods=['GET','POST','DELETE'])
def ApiDeleteLeave():
	if request.method=='DELETE':
		print 'data', request
		cmpid = request.args.get('cmpid')
		empid = request.args.get('empid')
		DeleteBNS = dbhelper.DeleteData().DeleteSHARow(cmpid, empid)
		if DeleteBNS:
			db={'message':'row deleted'}
			success = 1	
		else:
			db={'message': 'row not deleted'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Lock Leave
@app.route('/payroll/lock/payroll-v2/Leave/',methods=['GET','POST'])
def ApiLockLeave():
	if request.method=='POST':
		print request
		cmpid = request.args.get('cmpid')
		BNSlock = dbhelper.UpdateData().Leavelock(cmpid)
  		if BNSlock:
			db={'message':'Table Locked'}
			success = 1
		else:
			db={'message': 'Table Not Locked'}
			success = 0

		resp = Response(json.dumps({"success": success, "datasets": db}))
		return after_request(resp)

#Get Leave Lock
@app.route('/payroll/get/payroll-v2/leave-lock/',methods=['GET','POST'])
def ApiLeaveLock():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		lock_status = dbhelper.GetData().GetLeaveLock(cmpid)
		if (lock_status==1):
			status= True
		else:
			status = False
		
		resp = Response(json.dumps({"success": True, "status":status }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

###################################################################################################
#GET ALL LOCKS
@app.route('/payroll/get/payroll-v2/all-locks/',methods=['GET','POST'])
def ApiAllLocks():
	if request.method =='GET':
		cmpid = request.args.get('cmpid')
		print cmpid
		lock_status = dbhelper.GetData().GetLeaveLock(cmpid)
		if (lock_status==1):
			status1= True
		else:
			status1 = False
		lock_status = dbhelper.GetData().GetBNSLock(cmpid)
		if (lock_status==1):
			status2= True
		else:
			status2 = False
		lock_status = dbhelper.GetData().GetPNDLock(cmpid)
		if (lock_status==1):
			status3= True
		else:
			status3 = False
		lock_status = dbhelper.GetData().GetSHALock(cmpid)
		if (lock_status==1):
			status4= True
		else:
			status4 = False
		lock_status = dbhelper.GetData().GetReviewLock(cmpid)
		if (lock_status==1):
			status5= True
		else:
			status5 = False
		
		if (status1 and status2 and status3 and status4 and status5):
			status = True
		else:
			status = False

	
		resp = Response(json.dumps({"success": True, "status":status }))
		resp.headers['Content-type']='application/json'
		return after_request(resp)

