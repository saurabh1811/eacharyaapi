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

	def addUser(self, name, username, phone, email, password, signupdate, trialperiod):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()

			# #see if username is unique
			# _sqlc_="SELECT COUNT(*) FROM users WHERE (USER_USERNAME='%s')"%(username)
			# cursor.execute(_sqlc_)
			# unique= (cursor.fetchone())[0]
			# if(unique==None):
				

			#create user
			_sqlc_ = "INSERT INTO users (USER_NAME, USER_USERNAME, USER_EMAIL, USER_PASSWORD, USER_PHONE, USER_SIGNUP_DATE, USER_TRIAL_PERIOD) VALUES ('%s', '%s', '%s','%s','%s','%s', '%s')"%(name, username, email, password, phone, signupdate, trialperiod)
			cursor.execute(_sqlc_)	
			userid = cursor.lastrowid

			#create demo company
			_sqlc_ = "INSERT INTO company_info (COMPANY_NAME, COMPANY_COUNTRY,  PRIMARY_ADDRESS,  COMPANY_CITY,  COMPANY_STATE,  COMPANY_PIN,  COMPANY_FILING,  COMPANY_INDUSTRY, USERS_USER_ID, COMPANY_ACTIVE_STATUS) VALUES ('Demo Company', 'India', 'Demo Location', 'Demo City', 'Demo State', 000000, 'Demo Filing Address', 'Demo Industry', %s, 1 )"%(userid)
			cursor.execute(_sqlc_)
			cmpid = cursor.lastrowid
			
			#create demo branch
			_sqlc_ = "INSERT INTO branch (BRANCH_NAME, BRANCH_ADDRESS, BRANCH_CITY,  BRANCH_STATE,  BRANCH_COUNTRY, BRANCH_PIN, COMPANY_INFO_COMPANY_ID) VALUES ('Demo Branch', 'Demo Location', 'Demo City', 'Demo State', 'Demo Country', 000000, %s)"%cmpid
			cursor.execute(_sqlc_)
			branchid= cursor.lastrowid

			#create demo department
			today= date.today()
			_sqlc_="INSERT INTO departments (DEPARTMENT_NAME, COMPANY_INFO_COMPANY_ID, DEPARTMENT_CREATED_BY, DEPARTMENT_CREATED_ON) VALUES ('Demo Branch', %s, %s, '%s')"%(cmpid, userid, str(today))
			cursor.execute(_sqlc_)
			deptid=cursor.lastrowid

			#create demo employee
			_sqlc_="INSERT INTO employee_info (EMPLOYEE_NAME, EMPLOYEE_GENDER, EMPLOYEE_DOJ, EMPLOYEE_DESG, EMPLOYEE_LEVEL_CODE, EMPLOYEE_COMPANY_EMAIL, EMPLOYEE_PORTAL_ACCESS, EMPLOYEE_SUBSTANTIAL_INTEREST, BRANCH_BRANCH_ID, DEPARTMENTS_DEPARTMENT_ID, COMPANY_INFO_COMPANY_ID) VALUES ('Demo Employee', 'Male', '2019-28-06','Demo','2','demo1@demo.com', 0,0, %s,%s,%s)"%(branchid,deptid,cmpid)
			cursor.execute(_sqlc_)
			empid= cursor.lastrowid

			#create demo earning components
			_sqlc_="INSERT INTO salary_components_earning (component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, component_description, optional_state, active_state, COMPANY_ID) VALUES ('Basic', 'Basic', 'Basic', 'Fixed', 1, 50, 'Basic Pay', 0, 1, %s)" %(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_earning (component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, component_description, optional_state, active_state, COMPANY_ID) VALUES ('House Rent Allowance', 'House Rent Allowance', 'House Rent Allowance', 'Fixed', 2, 12, 'Allowance for House Rent', 0, 1, %s)" %(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_earning (component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, component_description, optional_state, active_state, COMPANY_ID) VALUES ('Fixed Allowance', 'Fixed Allowance', 'Fixed Allowance', 'Fixed', 1, 10, 'Fixed Money for Allowance', 0, 1, %s)" %(cmpid)
			cursor.execute(_sqlc_)
			
			#create reimbursement components
			_sqlc_="INSERT INTO salary_components_reimbursements (component_name, component_type, component_amount, optional_status, active_state, COMPANY_ID) VALUES ('Fuel Reimbursement','Fuel Reimbursement', 5000, 0, 1, %s)"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_reimbursements (component_name, component_type, component_amount, optional_status, active_state, COMPANY_ID) VALUES ('Telephone Reimbursement','Telephone Reimbursement', 5000, 0, 1, %s)"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_reimbursements (component_name, component_type, component_amount, optional_status, active_state, COMPANY_ID) VALUES ('Driver Reimbursement','Driver Reimbursement', 5000, 0, 1, %s)"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_reimbursements (component_name, component_type, component_amount, optional_status, active_state, COMPANY_ID) VALUES ('Leave Travel Allowance','Leave Travel ALlowance', 5000, 0, 1, %s)"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_reimbursements (component_name, component_type, component_amount, optional_status, active_state, COMPANY_ID) VALUES ('Vehicle Maintenance Reimbursement','Vehicle Maintenance Reimbursement', 5000, 0, 1, %s)"%(cmpid)
			cursor.execute(_sqlc_)
			
			conn.commit()
			conn.commit			
			conn.close()
			return userid 
		except Exception,e:
			print str(e)
	
	

	def addCompany(self, name, country, industry, address, city, state, pin, filing_address,userid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor() 
			_sqlc_ = "INSERT INTO company_info  (COMPANY_NAME, COMPANY_COUNTRY, COMPANY_INDUSTRY, PRIMARY_ADDRESS, COMPANY_CITY, COMPANY_STATE, COMPANY_PIN, COMPANY_FILING, USERS_USER_ID) VALUES ( '%s','%s','%s', '%s','%s','%s', '%s','%s', '%s')"%(name, country, industry, address, city, state, pin, filing_address, userid)
			cursor.execute(_sqlc_)
			cmpid = cursor.lastrowid
			_sqlc_ = "INSERT INTO branch (BRANCH_NAME, BRANCH_ADDRESS, BRANCH_CITY,  BRANCH_STATE,  BRANCH_COUNTRY, BRANCH_PIN, COMPANY_INFO_COMPANY_ID) VALUES ('Head Office', '%s','%s','%s', '%s', '%s', '%s')"%(address,city,state,country,pin,cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_earning (component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, component_description, optional_state, active_state, COMPANY_ID) VALUES ('Basic', 'Basic', 'Basic', 'Fixed', 1, 50, 'Basic Pay', 0, 1, %s)" %(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_earning (component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, component_description, optional_state, active_state, COMPANY_ID) VALUES ('House Rent Allowance', 'House Rent Allowance', 'House Rent Allowance', 'Fixed', 2, 12, 'Allowance for House Rent', 0, 1, %s)" %(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_earning (component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, component_description, optional_state, active_state, COMPANY_ID) VALUES ('Fixed Allowance', 'Fixed Allowance', 'Fixed Allowance', 'Fixed', 1, 10, 'Fixed Money for Allowance', 0, 1, %s)" %(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_reimbursements (component_name, component_type, component_amount, optional_status, active_state, COMPANY_ID) VALUES ('Fuel Reimbursement','Fuel Reimbursement', 5000, 0, 1, '%s')"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_reimbursements (component_name, component_type, component_amount, optional_status, active_state, COMPANY_ID) VALUES ('Telephone Reimbursement','Telephone Reimbursement', 5000, 0, 1, '%s')"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_reimbursements (component_name, component_type, component_amount, optional_status, active_state, COMPANY_ID) VALUES ('Driver Reimbursement','Driver Reimbursement', 5000, 0, 1, '%s')"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_reimbursements (component_name, component_type, component_amount, optional_status, active_state, COMPANY_ID) VALUES ('Leave Travel Allowance','Leave Travel ALlowance', 5000, 0, 1, '%s')"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO salary_components_reimbursements (component_name, component_type, component_amount, optional_status, active_state, COMPANY_ID) VALUES ('Vehicle Maintenance Reimbursement','Vehicle Maintenance Reimbursement', 5000, 0, 1, '%s')"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO payslip_template (PAYSLIP_TEMPLATE_NAME, ACTIVE_STATUS, COMPANY_ID) VALUES ('Standard Template', 1, '%s')"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO payslip_template (PAYSLIP_TEMPLATE_NAME, ACTIVE_STATUS, COMPANY_ID) VALUES ('Mini Template', 0, '%s')"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO payslip_template (PAYSLIP_TEMPLATE_NAME, ACTIVE_STATUS, COMPANY_ID) VALUES ('Simple Template', 0, '%s')"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO payslip_template (PAYSLIP_TEMPLATE_NAME, ACTIVE_STATUS, COMPANY_ID) VALUES ('Lite Template', 0, '%s')"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO payslip_template (PAYSLIP_TEMPLATE_NAME, ACTIVE_STATUS, COMPANY_ID) VALUES ('Simple Spreadsheet Template', 0, '%s')"%(cmpid)
			cursor.execute(_sqlc_)
			_sqlc_="INSERT INTO payslip_template (PAYSLIP_TEMPLATE_NAME, ACTIVE_STATUS, COMPANY_ID) VALUES ('Professional Template', 0, '%s')"%(cmpid)
			cursor.execute(_sqlc_)
			conn.commit()
			conn.close()
			return cmpid 
		except Exception,e:
			print str(e)

	def addTaxDetails(self, pan, tan, tds_ao, payment_frequency, deductor_name, deductor_father_name, cid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO company_tax_info  (COMPANY_PAN, COMPANY_TAN, COMPANY_TDS_AO, COMPANY_PAYMENT_FREQUENCY, COMPANY_DEDUCTOR_NAME, COMPANY_DEDUCTOR_FATHER_NAME, COMPANY_INFO_COMPANY_ID) VALUES ('%s', '%s','%s','%s', '%s','%s', '%s')"%(pan, tan, tds_ao, payment_frequency, deductor_name, deductor_father_name, cid)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addSalaryComponentEarning(self, component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, active_state, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			optional_state= '1'
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO salary_components_earning (component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, optional_state, active_state, COMPANY_ID) VALUES ('%s', '%s','%s', '%s', '%s','%s', '%s', '%s','%s')"%(component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, optional_state, active_state, cmpid)
			print _sqlc_
   			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addSalaryComponentDeduction(self, name, amt_type, amt, active_state, preorposttax, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			component_type='DEDUCTION'
			description='Added Component'
			optional_state= '1'
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO salary_components_deduction (component_name, component_type, description, optional_state, active_state, COMPANY_ID, component_amt_type, component_amt, preorposttax) VALUES ('%s', '%s','%s', '%s', '%s', '%s','%s', '%s', '%s')"%(name, component_type, description, optional_state, active_state, cmpid, amt_type, amt, preorposttax)
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addBranch(self, name, address, city, state, country, pin, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO branch (BRANCH_NAME, BRANCH_ADDRESS, BRANCH_CITY, BRANCH_STATE, BRANCH_COUNTRY, BRANCH_PIN, COMPANY_INFO_COMPANY_ID) VALUES ('%s','%s','%s', '%s','%s', '%s', '%s')"%( name, address, city, state, country, pin, cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addDepartment(self, name, cmpid, userid, creation):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO departments (DEPARTMENT_NAME, COMPANY_INFO_COMPANY_ID, DEPARTMENT_CREATED_BY, DEPARTMENT_CREATED_ON) VALUES ('%s','%s', '%s', '%s')"%( name, cmpid, userid, creation)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addDesignation(self, name, cmpid, userid, creation):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO company_grade (DESIGNATION_NAME, COMPANY_INFO_COMPANY_ID, DESIGNATION_CREATED_BY, DESIGNATION_CREATED_ON) VALUES ('%s','%s', '%s', '%s')"%( name, cmpid, userid, creation)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addEmployee(self, name, gender, doj, desg, department, company_email, portal_access, substantial_interest, branchid, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			#add employee
			_sqlc_ = "INSERT INTO employee_info (EMPLOYEE_NAME, EMPLOYEE_GENDER, EMPLOYEE_DOJ, EMPLOYEE_DESG, DEPARTMENTS_DEPARTMENT_ID, EMPLOYEE_COMPANY_EMAIL, EMPLOYEE_PORTAL_ACCESS, EMPLOYEE_SUBSTANTIAL_INTEREST, BRANCH_BRANCH_ID, COMPANY_INFO_COMPANY_ID) VALUES ('%s', '%s','%s','%s', %s,'%s', '%s', '%s', '%s', '%s')"%(name, gender, doj, desg, department, company_email, portal_access, substantial_interest, branchid, cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			_sqlc_ = "INSERT INTO payrun_review (EMPLOYEE_ID, EMPLOYEE_NAME, MONTH, EFFECTIVE_FROM, COMPANY_ID) VALUES ('%s', '%s', 'JULY_2019','%s','%s')"%(testid, name, doj, cmpid)
			cursor.execute(_sqlc_)
			conn.commit()
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addEmployeePersonalDetails(self, empid, email, phone, dob, guardian, pan, address, cmpid):
		try:
			print 1
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			#add employee details
			_sqlc_ = "INSERT INTO employee_personal_info (EMPLOYEE_PERSONAL_EMAIL, EMPLOYEE_PERSONAL_PHONE, EMPLOYEE_PERSONAL_DOB, EMPLOYEE_PERSONAL_GUARDIAN, EMPLOYEE_PERSONAL_PAN, EMPLOYEE_PERSONAL_ADDRESS, EMPLOYEE_ID, COMPANY_ID) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(email, phone, dob, guardian, pan, address, empid, cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addEmployeePaymentDetails(self, account_holder_name, bank_name, account_number, ifsc_code, account_type, empid, cmpid):
		try:
			print 1
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			#add employee details
			_sqlc_ = "INSERT INTO employee_payment_info (ACCOUNT_HOLDER_NAME, BANK_NAME, ACCOUNT_NUMBER, IFSC_CODE, ACCOUNT_TYPE, EMPLOYEE_ID, COMPANY_ID) VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s')"%(account_holder_name, bank_name, account_number, ifsc_code, account_type, empid, cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)		

	def addEmployeeSalaryDetails(self, tempid, employee_ctc, empid, cmpid, employee_earning_monthly, employee_reimbursement_monthly, employee_earning_annually, employee_reimbursement_annually, employee_fixed_monthly, employee_fixed_annually, employee_total_monthly, employee_total_annually):
		try:
			print 1
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			#add employee details
			_sqlc_ = "INSERT INTO employee_salary_details (salary_template_id, employee_ctc, EMPLOYEE_ID, COMPANY_ID, employee_earning_monthly, employee_reimbursement_monthly, employee_earning_annually, employee_reimbursement_annually, employee_fixed_monthly, employee_fixed_annually, employee_total_monthly, employee_total_annually) VALUES ('%s', '%s', %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )"%(tempid, employee_ctc, empid, cmpid, employee_earning_monthly, employee_reimbursement_monthly, employee_earning_annually, employee_reimbursement_annually, employee_fixed_monthly, employee_fixed_annually, employee_total_monthly, employee_total_annually)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			_sqlc_ = "UPDATE payrun_review SET GUARANTEED_CTC='%s', NET_SALARY='%s' WHERE (EMPLOYEE_ID='%s' AND COMPANY_ID='%s')"%(str(int(employee_ctc)/12), employee_total_monthly, empid, cmpid  )
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addPaySchedule(self, working_days, salary_basis, payment_date, cid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "INSERT INTO payment_schedule (SALARY_BASIS, WORKING_DAYS, PAYMENT_DATE, COMPANY_INFO_COMPANY_ID) VALUES ('%s','%s','%s','%s')"%( salary_basis, working_days, payment_date, cid)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)
			   
	def addPaymentTemplate(self, template_name, template_description, template_ctc, template_earning_components, template_earning_monthly, template_earning_annually, template_reimbursement_components, template_reimbursement_monthly, template_reimbursement_annually, template_fixed_monthly, template_fixed_annually,template_total_monthly, template_total_annually, cmpid ):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			print 1
			_sqlc_ = "INSERT INTO payment_templates (template_name, template_description, template_ctc, template_earning_components, template_earning_monthly, template_earning_annually, template_reimbursement_components, template_reimbursement_monthly, template_reimbursement_annually, template_fixed_monthly, template_fixed_annually, template_total_monthly, template_total_annually, COMPANY_ID ) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s', '%s')"%( template_name, template_description, template_ctc, template_earning_components, template_earning_monthly, template_earning_annually, template_reimbursement_components, template_reimbursement_monthly, template_reimbursement_annually, template_fixed_monthly, template_fixed_annually, template_total_monthly, template_total_annually, cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def addShift(self, shift_name, shift_type, shift_code, time_in, time_out, late_mark_upto_half_day_absent, in_time_for_full_absent, grace_in_time, grace_out_time, time_out_for_full_day_absent, early_leaving_upto_half_day, in_cut_off, break_start, break_end, gravity_shift_max, is_gravity_shift, is_half_day, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			print 1
			_sqlc_ = "INSERT INTO shifts (shift_name,  shift_type, shift_code, time_in, time_out, late_mark_upto_half_day_absent, in_time_for_full_absent, grace_in_time, grace_out_time, time_out_for_full_day_absent, early_leaving_upto_half_day, in_cut_off, break_start, break_end, gravity_shift_max, is_gravity_shift, is_half_day, COMPANY_ID) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', '%s', '%s','%s','%s','%s', %s)"%( shift_name, shift_type, shift_code, time_in, time_out, late_mark_upto_half_day_absent, in_time_for_full_absent, grace_in_time, grace_out_time, time_out_for_full_day_absent, early_leaving_upto_half_day, in_cut_off, break_start, break_end, gravity_shift_max, is_gravity_shift, is_half_day, cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def	addBNS(self, empid, emp_name, guaranteed_ctc, bonus, net_salary, effective_from, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			print 1
			_sqlc_ = "UPDATE payrun_review SET SALARY_REVISION_LOCK=1 WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			testid= cursor.lastrowid
			conn.commit()
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

	def	addPaymentAndDeduction(self, EMPLOYEE_ID,EMPLOYEE_NAME, PAYMENT_AMOUNT, PAYMENT_TYPE, PAYMENT_COMMENT, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			print 1
			_sqlc_ = "SELECT PAYMENT_DEDUCTION_LOCK FROM payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			if cursor.fetchone():
				lock = int ((cursor.fetchone())[0])
				print lock
				if(lock == 1):
					lock = 0
				else:
					lock = 1
				print 2
				_sqlc_ = "SELECT EMPLOYEE_ID FROM payrun_review WHERE EMPLOYEE_ID='%s'"%(EMPLOYEE_ID)
				print _sqlc_
				cursor.execute(_sqlc_)
				if cursor.fetchone():
					_sqlc_ = "UPDATE payrun_review SET PAYMENT_AMOUNT='%s', PAYMENT_TYPE='%s', PAYMENT_COMMENT='%s', PAYMENT_DEDUCTION_LOCK='%s' WHERE (EMPLOYEE_ID='%s' AND COMPANY_ID='%s')"%(PAYMENT_AMOUNT, PAYMENT_TYPE, PAYMENT_COMMENT, lock, EMPLOYEE_ID, cmpid)
					print _sqlc_
					print 3
					cursor.execute(_sqlc_)
					testid = cursor.lastrowid
				else:
					lock=1
					print lock
					_sqlc_ = "INSERT INTO payrun_review (EMPLOYEE_ID, EMPLOYEE_NAME, PAYMENT_AMOUNT, PAYMENT_TYPE, PAYMENT_COMMENT, COMPANY_ID, PAYMENT_DEDUCTION_LOCK ) VALUES ('%s', '%s', '%s','%s','%s', '%s', '%s')"%( EMPLOYEE_ID, EMPLOYEE_NAME, PAYMENT_AMOUNT, PAYMENT_TYPE, PAYMENT_COMMENT, cmpid, lock)
					print _sqlc_
					cursor.execute(_sqlc_)
					testid = cursor.lastrowid
			else:
				print 2
				lock=1
				print lock
				_sqlc_ = "INSERT INTO payrun_review (EMPLOYEE_ID, EMPLOYEE_NAME, PAYMENT_AMOUNT, PAYMENT_TYPE, PAYMENT_COMMENT, COMPANY_ID, PAYMENT_DEDUCTION_LOCK ) VALUES ('%s', '%s', '%s','%s','%s', '%s', '%s')"%( EMPLOYEE_ID, EMPLOYEE_NAME, PAYMENT_AMOUNT, PAYMENT_TYPE, PAYMENT_COMMENT, cmpid, lock)
				print _sqlc_
				cursor.execute(_sqlc_)
				testid = cursor.lastrowid
			print testid
			print 4
			conn.commit()
			conn.close()
			return testid 
		except Exception,e:
			print str(e)

class GetData():

	def GetUser(self, userid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="SELECT USER_NAME FROM users WHERE USER_ID='%s'"%(userid)
			print _sqlcmd_
			cursor.execute(_sqlcmd_)
			username = (cursor.fetchone())[0]
			print username
			conn.commit()
			conn.close()
			return username
		except Exception,e:
			print str(e)

	def returnSignupCookies(self, username):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT USER_ID, USER_NAME, USER_EMAIL, USER_PHONE, USER_ROLE, USER_MAX_COMPANIES, USER_CREATED_COMPANIES, USER_SIGNUP_DATE, USER_TRIAL_PERIOD FROM users WHERE USER_USERNAME='%s'"%(username)
			print	_sqlc_	
			cursor.execute(_sqlc_)
			dbDetails=[]
			dbDetails = cursor.fetchall()
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
	
	def LoginData(self, email):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="select id, USER_NAME, USER_EMAIL, USER_PASSWORD, USER_ROLE, USER_PHONE, USER_MAX_COMPANIES ,USER_CREATED_COMPANIES FROM users where USER_EMAIL = BINARY '%s' "%(str(email))
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

	def checkUsername(self, username):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="select COUNT(USER_USERNAME) from users WHERE (USER_USERNAME='%s')"%(username)
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

	def checkPhone(self, phone):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlcmd_ ="select COUNT(USER_PHONE) from users WHERE (USER_PHONE='%s')"%(phone)
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
	
	def GetUserCompanies(self, uid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "select id, COMPANY_NAME, PRIMARY_ADDRESS, COMPANY_CITY, COMPANY_STATE, COMPANY_COUNTRY, COMPANY_PIN, COMPANY_INDUSTRY, COMPANY_ACTIVE_STATUS  FROM company_info WHERE (USERS_USER_ID='%s')" %(uid)
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
	
	def GetCompany(self, uid,cid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "select id, COMPANY_NAME, PRIMARY_ADDRESS, COMPANY_CITY, COMPANY_STATE, COMPANY_COUNTRY, COMPANY_PIN, COMPANY_INDUSTRY, COMPANY_ACTIVE_STATUS  FROM company_info WHERE ((USERS_USER_ID='%s') AND (id='%s'))" %(uid,cid)
				print sqlcmd
				cursor.execute(sqlcmd)
				dbDetails=[]
				for row in cursor.fetchall():
					dbDetails.append(row)
				print dbDetails
				conn.commit()
				conn.close()
				return dbDetails
			except Exception,e:
				print str(e)
	
	def GetActiveCompany(self, uid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "select id, COMPANY_NAME  FROM company_info WHERE (USERS_USER_ID='%s') AND (COMPANY_ACTIVE_STATUS = 1)" %(uid)
				print sqlcmd
				cursor.execute(sqlcmd)
				dbDetails=[]
				for row in cursor.fetchall():
					dbDetails.append(row)
				conn.commit()
				conn.close()
				print dbDetails
				return dbDetails
			except Exception,e:
				print str(e)

	def GetSalaryComponentsEarning(self,cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT  id, component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, active_state  FROM salary_components_earning WHERE (COMPANY_ID='%s')"%(cmpid)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetActiveSalaryComponentsEarning(self,cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT  id, component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, active_state  FROM salary_components_earning WHERE ((COMPANY_ID='%s') AND (active_state=1))"%(cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
   
	def GetTemplateActiveSalaryComponentsEarning(self, id, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT  id, component_name, component_type, component_payslip_name, component_pay_type, component_calculation_type, component_calculation_amt, active_state  FROM salary_components_earning WHERE (((id='%s') AND ((COMPANY_ID='%s') AND (active_state=1))) AND (component_name <> 'Fixed Allowance'))"%(id, cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
   
	def GetTemplateActiveSalaryComponentsReimbursement(self, id, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id, component_name, component_type, component_amount, active_state FROM salary_components_reimbursements WHERE ((id='%s') AND ((COMPANY_ID='%s') AND (active_state=1)))"%(id, cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetSalaryComponentsDeductionPreTax(self,cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT component_name, component_amt_type, component_amt, active_state FROM salary_components_deduction WHERE (((optional_state=0) OR (COMPANY_ID='%s')) AND (preorposttax='PRE_TAX')) "%(cmpid)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetSalaryComponentsDeductionPostTax(self,cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT component_name, component_amt_type, component_amt, active_state FROM salary_components_deduction WHERE (((optional_state=0) OR (COMPANY_ID='%s')) AND (preorposttax='POST_TAX')) "%(cmpid)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetSalaryComponentsReimbursement(self,cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id, component_name, component_type, component_amount, active_state FROM salary_components_reimbursements WHERE (COMPANY_ID='%s')"%(cmpid)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetActiveSalaryComponentsReimbursement(self,cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id, component_name, component_type, component_amount, active_state FROM salary_components_reimbursements WHERE ((COMPANY_ID='%s') AND (active_state=1))"%(cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetSalaryComponentsReimbursementEdit(self, cmpid, compid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id, component_name, component_type, component_amount, active_state FROM salary_components_reimbursements WHERE component_id='%s'"%(compid)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetTaxDetails(self, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT *  FROM company_tax_info WHERE COMPANY_INFO_COMPANY_ID='%d'" %(cmpid)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetAllEmployees(self, userid, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()

			#get company id
			# _sqlc_= "SELECT COMPANY_ID FROM company_info WHERE (USERS_USER_ID = %s)"%(userid)
			# print _sqlc_
			# cursor.execute(_sqlc_)
			# cmpid = cursor.fetchone()
			# id = cmpid[0]

			sqlcmd = "SELECT id, EMPLOYEE_NAME, EMPLOYEE_GENDER, EMPLOYEE_COMPANY_EMAIL, EMPLOYEE_DESG  FROM employee_info WHERE COMPANY_INFO_COMPANY_ID='%s'" %(cmpid)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetEmployeeInfo(self, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()

			#get company id
			# _sqlc_= "SELECT COMPANY_ID FROM company_info WHERE (USERS_USER_ID = %s)"%(userid)
			# print _sqlc_
			# cursor.execute(_sqlc_)
			# cmpid = cursor.fetchone()
			# id = cmpid[0]

			sqlcmd = "SELECT EMPLOYEE_NAME, id, EMPLOYEE_DESG, EMPLOYEE_COMPANY_EMAIL, EMPLOYEE_GENDER, EMPLOYEE_DOJ, BRANCH_BRANCH_ID, DEPARTMENTS_DEPARTMENT_ID, COMPANY_INFO_COMPANY_ID, EMPLOYEE_PORTAL_ACCESS FROM employee_info WHERE id='%s'" %(empid)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetBranchName(self, bid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "SELECT BRANCH_NAME  FROM branch WHERE (BRANCH_ID='%s')" %(bid)
				print sqlcmd
				cursor.execute(sqlcmd)
				dbDetails= (cursor.fetchone())[0]
				conn.commit()
				conn.close()
				return dbDetails
			except Exception,e:
				print str(e)		

	def GetDepartmentName(self, did):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "SELECT DEPARTMENT_ID FROM departments WHERE (DEPARTMENT_ID='%s')" %(did)
				print sqlcmd
				cursor.execute(sqlcmd)
				dbDetails= (cursor.fetchone())[0]
				conn.commit()
				conn.close()
				return dbDetails
			except Exception,e:
				print str(e)

	def GetEmployeePersonal(self, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()

			#get company id
			# _sqlc_= "SELECT COMPANY_ID FROM company_info WHERE (USERS_USER_ID = %s)"%(userid)
			# print _sqlc_
			# cursor.execute(_sqlc_)
			# cmpid = cursor.fetchone()
			# id = cmpid[0]

			sqlcmd = "SELECT * FROM employee_personal_info WHERE (EMPLOYEE_ID='%s')" %(empid)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetEmployeePayment(self, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()

			#get company id
			# _sqlc_= "SELECT COMPANY_ID FROM company_info WHERE (USERS_USER_ID = %s)"%(userid)
			# print _sqlc_
			# cursor.execute(_sqlc_)
			# cmpid = cursor.fetchone()
			# id = cmpid[0]

			sqlcmd = "SELECT * FROM employee_payment_info WHERE (EMPLOYEE_ID='%s')" %(empid)
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetBranchDetails(self, cmpid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "SELECT *  FROM branch WHERE (COMPANY_INFO_COMPANY_ID='%s')" %(cmpid)
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

	def GetBranchDropDown(self, cmpid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "SELECT BRANCH_NAME, id  FROM branch WHERE (COMPANY_INFO_COMPANY_ID='%s')" %(cmpid)
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

	def GetDepartmentList(self, cmpid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "SELECT id, DEPARTMENT_NAME, DEPARTMENT_CREATED_ON, DEPARTMENT_CREATED_BY  FROM departments WHERE (COMPANY_INFO_COMPANY_ID='%s')" %(cmpid)
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

	def GetDepartmentDropDownList(self, cmpid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "SELECT DEPARTMENT_NAME, id  FROM departments WHERE (COMPANY_INFO_COMPANY_ID='%s')" %(cmpid)
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
	
	def GetDesignationList(self, cmpid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "SELECT id, DESIGNATION_NAME, DESIGNATION_CREATED_ON, DESIGNATION_CREATED_BY FROM company_grade WHERE (COMPANY_INFO_COMPANY_ID='%s')" %(cmpid)
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

	def GetDesignationDropDown(self, cmpid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "SELECT DESIGNATION_NAME, id FROM company_grade WHERE (COMPANY_INFO_COMPANY_ID='%s')" %(cmpid)
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

	def GetBranchEdit(self, bid, cmpid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "SELECT id, BRANCH_NAME, BRANCH_ADDRESS, BRANCH_CITY, BRANCH_STATE, BRANCH_COUNTRY, BRANCH_PIN  FROM branch WHERE ((id='%s') AND (COMPANY_INFO_COMPANY_ID=%s))" %(bid,cmpid)
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

	def GetDepartmentEdit(self, did, cmpid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "SELECT id, DEPARTMENT_NAME  FROM departments WHERE ((id='%s') AND (COMPANY_INFO_COMPANY_ID='%s'))" %(did,cmpid)
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
	
	def GetDesignationEdit(self, did, cmpid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "SELECT id, DESIGNATION_NAME  FROM company_grade WHERE ((id='%s') AND (COMPANY_INFO_COMPANY_ID='%s'))" %(did,cmpid)
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

	def GetDefaultPayslipTemplate(self, cid):
			try:
				dbname='payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				sqlcmd = "SELECT PAYSLIP_TEMPLATE_NAME FROM payslip_template WHERE ((ACTIVE_STATUS=1) AND (COMPANY_ID='%s'))" %(cid)
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

	def GetPayslipDataCompany(self, empid, cmpid):
			try:
				dbname = 'payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				_sqlc_ = "SELECT COMPANY_NAME, COMPANY_FILING FROM company_info WHERE (COMPANY_ID='%s') "%(cmpid)
				print _sqlc_
				cursor.execute(_sqlc_)
				dbDetails=[]
				for row in cursor.fetchall():
					dbDetails.append(row)
				conn.commit()
				conn.close()
				return dbDetails
			except Exception,e:
				print str(e)

	def GetPayslipDataEmployee(self, empid, cmpid):
			try:
				dbname = 'payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				_sqlc_ = "SELECT EMPLOYEE_NAME, EMPLOYEE_DESG, EMPLOYEE_DOJ FROM employee_info WHERE (EMPLOYEE_ID='%s') "%(empid)
				print _sqlc_
				cursor.execute(_sqlc_)
				dbDetails=[]
				for row in cursor.fetchall():
					dbDetails.append(row)
				conn.commit()
				conn.close()
				return dbDetails
			except Exception,e:
				print str(e)

	def GetPaySchedule(self, cid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT SALARY_BASIS, WORKING_DAYS, PAYMENT_DATE FROM payment_schedule WHERE (COMPANY_INFO_COMPANY_ID='%s') "%(cid)
			print _sqlc_
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
	 
	def GetPaymentTemplates(self, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id, template_name, template_description FROM payment_templates WHERE COMPANY_ID='%s'"%(cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetPaymentTemplatesDropDown(self, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT template_name, id FROM payment_templates WHERE COMPANY_ID='%s'"%(cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)		

	def GetTemplateData(self, tempid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id, template_name, template_description, template_ctc, template_earning_components, template_earning_monthly, template_earning_annually, template_reimbursement_components, template_reimbursement_monthly, template_reimbursement_annually, template_fixed_monthly, template_fixed_annually, template_total_monthly, template_total_annually  FROM payment_templates WHERE id='%s'"%(tempid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)	
	
	def GetEarningName(self, id_list):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			names=[]
			for i in range(0, len(id_list)):
				sqlcmd = "SELECT component_name FROM salary_components_earning WHERE component_id='%s'"%(id_list[i])
				print sqlcmd
				cursor.execute(sqlcmd)
				name=cursor.fetchone()[0]
				names.append(name)
			print names
			conn.commit()
			conn.close()
			return names
		except Exception,e:
			print str(e)

	def GetReimbursementName(self, id_list):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			names=[]
			for i in range(0, len(id_list)):
				sqlcmd = "SELECT component_name FROM salary_components_reimbursements WHERE component_id='%s'"%(id_list[i])
				print sqlcmd
				cursor.execute(sqlcmd)
				name=cursor.fetchone()[0]
				names.append(name)
			print names
			conn.commit()
			conn.close()
			return names
		except Exception,e:
			print str(e)

	def getShifts(self, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT id, shift_name, shift_type, shift_code, time_in, time_out FROM shifts WHERE COMPANY_ID='%s'"%(cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def getShiftsDropDown(self, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT shift_name, id FROM shifts WHERE COMPANY_ID='%s'"%(cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetShiftDetails(self, shiftid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT shift_name, shift_type, shift_code, time_in, time_out, grace_in_time, grace_out_time FROM shifts WHERE id='%s'"%(shiftid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetBNS(self, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, MONTH, GUARANTEED_CTC, NET_SALARY, BONUS, EFFECTIVE_FROM FROM payrun_review WHERE (EMPLOYEE_ID='%s')"%(empid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
 
	def GetEditableBNS(self, cmpid, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, GUARANTEED_CTC, NET_SALARY, BONUS, EFFECTIVE_FROM FROM payrun_review WHERE ((EMPLOYEE_ID='%s') AND (COMPANY_ID='%s'))"%(empid, cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
   
	def GetEditablePNDPayments(self, cmpid, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, PAYMENT_AMOUNT, PAYMENT_TYPE, PAYMENT_COMMENT FROM payrun_review WHERE ((EMPLOYEE_ID='%s') AND (COMPANY_ID='%s'))"%(empid, cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetEditablePNDDeductions(self, cmpid, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, DEDUCTION_AMOUNT, DEDUCTION_TYPE, DEDUCTION_COMMENT FROM payrun_review WHERE ((EMPLOYEE_ID='%s') AND (COMPANY_ID='%s'))"%(empid, cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
   
	def GetEditableSHA(self, cmpid, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, SALARY_HOLD_AMOUNT, SALARY_HOLD_PAY_CYCLE, SALARY_HOLD_ACTION, SALARY_HOLD_COMMENT FROM payrun_review WHERE ((EMPLOYEE_ID='%s') AND (COMPANY_ID='%s'))"%(empid, cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
   
	def GetEditableReview(self, cmpid, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, LOP_DAYS, GROSS_PAY, PAYABLE_DAYS, LEAVE_REASON, LEAVE_DETAILS FROM payrun_review WHERE ((EMPLOYEE_ID='%s') AND (COMPANY_ID='%s'))"%(empid, cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
   
	def GetEditableLeave(self, cmpid, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, WORKING_DAYS, PRESENT_DAYS, TOTAL_LEAVE, TYPE_OF_LEAVE, LEAVE_DEDUCTIONS FROM payrun_review WHERE ((EMPLOYEE_ID='%s') AND (COMPANY_ID='%s'))"%(empid, cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
 
	def GetEmployeeCOunt(self, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT COUNT(EMPLOYEE_ID) FROM employee_info WHERE COMPANY_INFO_COMPANY_ID='%s'"%(cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			count= (cursor.fetchone())[0]
			print count
			conn.commit()
			conn.close()
			return int(count)
		except Exception,e:
			print str(e)

	def GetBNSEmployeeData(self, idno):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, EMPLOYEE_DOJ FROM employee_info WHERE EMPLOYEE_ID='%s'"%(idno)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetBNSEmployeeSalary(self, eid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT employee_ctc, employee_total_monthly FROM employee_salary_details WHERE EMPLOYEE_ID='%s'"%(eid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetBNSBonusData(self, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT count(component_type) FROM salary_components_earning WHERE ((component_type= 'BASIC') AND (COMPANY_ID='%s'))"%(cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=cursor.fetchone()[0]
			print dbDetails
			if (int(dbDetails)>0):
				sqlcmd = "SELECT component_calculation_amt FROM salary_components_earning WHERE ((component_type= 'BASIC') AND (COMPANY_ID='%s'))"%(cmpid)
				cursor.execute(sqlcmd)
				bonus = dbDetails=cursor.fetchone()[0]
			else:
				bonus = 0
			print bonus
			conn.commit()
			conn.close()
			return int(bonus)
		except Exception,e:
			print str(e)

	def GetBNSLock(self, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT SALARY_REVISION_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			conn.commit()
			conn.close()
			return lock
		except Exception,e:
			print str(e)
   
	def GetPNDLock(self, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT PAYMENT_DEDUCTION_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			conn.commit()
			conn.close()
			return lock
		except Exception,e:
			print str(e)
 
	def GetEmployeeID(self, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID FROM employee_info WHERE COMPANY_INFO_COMPANY_ID='%s'"%(cmpid)
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

	def GetPaymentAndDeductionLock(self, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT PAYMENT_DEDUCTION_LOCK FROM payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			# if (cursor.fetchone()==None):
			# 	lock = 'not added'
			# else:
			# 	print 2
			# 	print cursor.fetchone()
			# 	lock= '0
			print dbDetails
			if dbDetails:
				for line in dbDetails:
					lock = line[0]
				else:
					lock = 'not added'
			print lock
			conn.commit()
			conn.close()
			return lock
		except Exception,e:
			print str(e)

	def GetPNDPayments(self, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, MONTH, PAYMENT_AMOUNT, PAYMENT_TYPE, PAYMENT_COMMENT FROM payrun_review WHERE (EMPLOYEE_ID='%s')"%(empid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def GetPNDDeductions(self, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, MONTH, DEDUCTION_AMOUNT, DEDUCTION_TYPE, DEDUCTION_COMMENT FROM payrun_review WHERE (EMPLOYEE_ID='%s')"%(empid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
   
	def GetSHATable(self, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, MONTH, SALARY_HOLD_AMOUNT, SALARY_HOLD_PAY_CYCLE, SALARY_HOLD_ACTION, SALARY_HOLD_COMMENT FROM payrun_review WHERE (EMPLOYEE_ID='%s')"%(empid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
   
	def GetReviewTable(self, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, MONTH, LOP_DAYS, GROSS_PAY, PAYABLE_DAYS, LEAVE_REASON, LEAVE_DETAILS FROM payrun_review WHERE (EMPLOYEE_ID='%s')"%(empid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
	
	def GetLeaveTable(self, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT EMPLOYEE_ID, EMPLOYEE_NAME, MONTH, WORKING_DAYS, PRESENT_DAYS, TOTAL_LEAVE, TYPE_OF_LEAVE, LEAVE_DEDUCTIONS FROM payrun_review WHERE (EMPLOYEE_ID='%s')"%(empid)
			print sqlcmd
			cursor.execute(sqlcmd)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			print dbDetails
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)
   
   	def GetSHALock(self, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT SALARY_HOLD_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			conn.commit()
			conn.close()
			return lock
		except Exception,e:
			print str(e)
   
	def GetReviewLock(self, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT EMPLOYEE_REVISION_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			conn.commit()
			conn.close()
			return lock
		except Exception,e:
			print str(e)
   
	def GetLeaveLock(self, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT LEAVE_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			conn.commit()
			conn.close()
			return lock
		except Exception,e:
			print str(e)
   
   
class UpdateData():
	
	def updateCompany(self, cid, name, country, industry, address, city, state, pin, filing_address, userid):
	# try:
		dbname = 'payroll_db'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor() 
		_sqlc_ = "UPDATE company_info SET COMPANY_NAME='%s', COMPANY_COUNTRY='%s', COMPANY_INDUSTRY='%s', PRIMARY_ADDRESS='%s', COMPANY_CITY='%s', COMPANY_STATE='%s', COMPANY_PIN='%s', COMPANY_FILING='%s' WHERE (id='%s')"%(name, country, industry, address, city, state, pin, filing_address, cid)
		print _sqlc_
		cursor.execute(_sqlc_)
		cmpid = cursor.lastrowid
		print cmpid
		conn.commit()
		conn.close()
		return cid 
	# except Exception,e:
	# 	print str(e)

	def ChangeActiveCompany(self, userid, cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			
			sqlcmd="UPDATE company_info SET COMPANY_ACTIVE_STATUS=1 WHERE ((USERS_USER_ID='%s') AND (id='%s'))"%(userid, cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)
			sqlcmd = "SELECT id, COMPANY_NAME FROM company_info WHERE ((USERS_USER_ID='%s') AND (COMPANY_ACTIVE_STATUS=1))" %(userid)
			cursor.execute(sqlcmd)
			print sqlcmd
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			print dbDetails
			return dbDetails
		except Exception,e:
		  print str(e)

	def ChangeActiveComponentEarning(self, compid, cid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT active_state FROM salary_components_earning WHERE (id='%s')"%(compid)
			print sqlcmd
			cursor.execute(sqlcmd)
			activity= (cursor.fetchone())[0]
			print activity
			if (activity==1):
				sqlcmd="UPDATE salary_components_earning SET active_state=0 WHERE ((id='%s') AND (COMPANY_ID ='%s'))"%(compid, cid)
			elif(activity==0):
				sqlcmd="UPDATE salary_components_earning SET active_state=1 WHERE ((id='%s') AND (COMPANY_ID = '%s'))"%(compid, cid)
			print sqlcmd
			cursor.execute(sqlcmd)
			status = 1
			conn.commit()
			conn.close()
			print status
			return status
		except Exception,e:
		  print str(e)

	def ChangeActiveComponentReimbursement(self, compid, cid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd = "SELECT active_state FROM salary_components_reimbursements WHERE (id='%s')"%(compid)
			print sqlcmd
			cursor.execute(sqlcmd)
			activity= (cursor.fetchone())[0]
			print activity
			if (activity==1):
				sqlcmd="UPDATE salary_components_reimbursements SET active_state=0 WHERE ((id='%s') AND (COMPANY_ID = '%s'))"%(compid, cid)
			elif(activity==0):
				sqlcmd="UPDATE salary_components_reimbursements SET active_state=1 WHERE ((id='%s') AND (COMPANY_ID = '%s'))"%(compid, cid)
			print sqlcmd
			cursor.execute(sqlcmd)
			status = 1
			conn.commit()
			conn.close()
			print status
			return status
		except Exception,e:
		  print str(e)

	def UpdateComponentReimbursement(self, component_name, component_type, amount, active_state, cid, compid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor() 
			_sqlc_ = "UPDATE salary_components_reimbursements SET component_name='%s', component_type='%s', component_amount=%s, active_state='%s' WHERE ((COMPANY_ID='%s') AND (component_id='%s'))"%(component_name, component_type, amount, active_state, cid, compid)
			print _sqlc_
			cursor.execute(_sqlc_)
			cmpid = cursor.lastrowid
			print cmpid
			conn.commit()
			conn.close()
			return cid 
		except Exception,e:
			print str(e)

	def updateBranch(self, name, address, city, state, country, pin, cmpid, bid):
			try:
				dbname = 'payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				_sqlc_ = "UPDATE branch  SET BRANCH_NAME='%s', BRANCH_ADDRESS='%s', BRANCH_CITY='%s', BRANCH_STATE='%s', BRANCH_COUNTRY='%s', BRANCH_PIN='%s' WHERE (BRANCH_ID='%s') "%( name, address, city, state, country, pin, bid)
				print _sqlc_
				cursor.execute(_sqlc_)
				conn.commit()
				testid = cursor.lastrowid
				conn.close()
				return bid
			except Exception,e:
				print str(e)

	def updateDepartment(self, name, cmpid, did):
			try:
				dbname = 'payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				_sqlc_ = "UPDATE departments  SET DEPARTMENT_NAME='%s' WHERE (id='%s') "%( name, did)
				print _sqlc_
				cursor.execute(_sqlc_)
				conn.commit()
				testid = cursor.lastrowid
				conn.close()
				return did
			except Exception,e:
				print str(e)

	def updateDesignation(self, name, cmpid, did):
			try:
				dbname = 'payroll_db'
				conn = connect_to_cloudsql(dbname)
				cursor = conn.cursor()
				_sqlc_ = "UPDATE company_grade SET DESIGNATION_NAME='%s' WHERE (id='%s') "%( name, did)
				print _sqlc_
				cursor.execute(_sqlc_)
				_sqlc = "UPDATE departments SET DEPARTMENT_NAME='%s' WHERE (id='%s') "%( name, did)
				print _sqlc
				cursor.execute(_sqlc)
				conn.commit()
				testid = cursor.lastrowid
				conn.close()
				return testid
			except Exception,e:
				print str(e)

	def DefaultPayslipTemplate(self, temp_name, cid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd="UPDATE payslip_template SET ACTIVE_STATUS=0 WHERE ACTIVE_STATUS=1"
			print sqlcmd
			cursor.execute(sqlcmd)
			sqlcmd="UPDATE payslip_template SET ACTIVE_STATUS=1 WHERE ((PAYSLIP_TEMPLATE_NAME = '%s' ) AND (COMPANY_ID='%s')) "%(temp_name, cid)
			print sqlcmd
			cursor.execute(sqlcmd)
			testid=cursor.lastrowid
			print testid			
			conn.commit()
			conn.close()
			return 1
		except Exception,e:
		  print str(e)

	def UpdatePaySchedule(self, working_days, salary_basis, payment_date, cid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "UPDATE payment_schedule SET SALARY_BASIS ='%s', WORKING_DAYS='%s', PAYMENT_DATE='%s' WHERE (COMPANY_INFO_COMPANY_ID='%s')"%( salary_basis, working_days, payment_date, cid)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)
	
	def UpdateShift(self, shiftid, shift_name, shift_type, shift_code, time_in, time_out, late_mark_upto_half_day_absent, in_time_for_full_absent, grace_in_time, grace_out_time, time_out_for_full_day_absent, early_leaving_upto_half_day, in_cut_off, break_start, break_end, gravity_shift_max, is_gravity_shift, is_half_day, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "UPDATE shifts SET shift_name ='%s', shift_type='%s', shift_code='%s', time_in='%s', time_out='%s', late_mark_upto_half_day_absent='%s', in_time_for_full_absent='%s', grace_in_time='%s', grace_out_time='%s', time_out_for_full_day_absent='%s', early_leaving_upto_half_day='%s', in_cut_off='%s', break_start='%s', break_end='%s', gravity_shift_max='%s', is_gravity_shift='%s', is_half_day='%s'  WHERE (shift_id='%s')"%(shift_name, shift_type, shift_code, time_in, time_out, late_mark_upto_half_day_absent, in_time_for_full_absent, grace_in_time, grace_out_time, time_out_for_full_day_absent, early_leaving_upto_half_day, in_cut_off, break_start, break_end, gravity_shift_max, is_gravity_shift, is_half_day, shiftid)
			print _sqlc_
			cursor.execute(_sqlc_)
			conn.commit()
			testid = cursor.lastrowid
			conn.close()
			return testid
		except Exception,e:
			print str(e)

	def EditShift(self, shiftid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT * FROM shifts WHERE id='%s'"%(shiftid)
			print _sqlc_
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			conn.commit()
			conn.close()
			return dbDetails
		except Exception,e:
			print str(e)

	def UpdateBNS(self, ctc, net_salary, cmpid, empid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "UPDATE payrun_review SET GUARANTEED_CTC='%s', NET_SALARY='%s' WHERE ((EMPLOYEE_ID='%s') AND (COMPANY_ID='%s'))"%(ctc, net_salary, empid, cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			testid= cursor.lastrowid
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
			print str(e)
	
	def UpdateBNSdata(self, cmpid, empid, guaranteed_ctc, effective_from, net_salary, bonus):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "UPDATE payrun_review SET GUARANTEED_CTC='%s', NET_SALARY='%s', BONUS='%s', EFFECTIVE_FROM='%s' WHERE ((EMPLOYEE_ID='%s') AND (COMPANY_ID='%s'))"%(guaranteed_ctc, net_salary, bonus, effective_from, empid ,cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			testid= cursor.rowcount
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
			print str(e)
	
	def UpdatePNDPayments(self, cmpid, empid, payment_amount, payment_type, payment_comment):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "UPDATE payrun_review SET PAYMENT_AMOUNT='%s', PAYMENT_TYPE='%s', PAYMENT_COMMENT='%s' WHERE ((EMPLOYEE_ID='%s') AND (COMPANY_ID='%s'))"%(payment_amount, payment_type, payment_comment, empid ,cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			testid= cursor.rowcount
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
			print str(e)
	
	def UpdatePNDDeductions(self, cmpid, empid, deduction_amount, deduction_type, deduction_comment):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "UPDATE payrun_review SET DEDUCTION_AMOUNT='%s', DEDUCTION_TYPE='%s', DEDUCTION_COMMENT='%s' WHERE ((EMPLOYEE_ID='%s') AND (COMPANY_ID='%s'))"%(deduction_amount, deduction_type, deduction_comment, empid ,cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			testid= cursor.rowcount
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
			print str(e)
   
	def UpdateSHA(self, cmpid, empid, payment_amount, payment_cycle, payment_action, payment_comment):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "UPDATE payrun_review SET SALARY_HOLD_AMOUNT='%s', SALARY_HOLD_PAY_CYCLE='%s', SALARY_HOLD_ACTION='%s' , SALARY_HOLD_COMMENT='%s' WHERE ((EMPLOYEE_ID='%s') AND (COMPANY_ID='%s'))"%(payment_amount, payment_cycle, payment_action, payment_comment, empid ,cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			testid= cursor.rowcount
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
			print str(e)
 
	def UpdateReview(self, cmpid, empid, lop_days,gross_pay, payable_days, leave_reason, leave_details):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "UPDATE payrun_review SET LOP_DAYS='%s', GROSS_PAY='%s', PAYABLE_DAYS='%s' , LEAVE_REASON='%s', LEAVE_DETAILS='%s' WHERE ((EMPLOYEE_ID=%s) AND (COMPANY_ID=%s))"%(lop_days,gross_pay, payable_days, leave_reason, leave_details, empid ,cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			testid= cursor.rowcount
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
			print str(e)
   
	def UpdateLeave(self, cmpid, empid, working_days,present_days, total_leave, type_of_leave, leave_deductions):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "UPDATE payrun_review SET WORKING_DAYS='%s', PRESENT_DAYS='%s', TOTAL_LEAVE='%s' , TYPE_OF_LEAVE='%s', LEAVE_DEDUCTIONS='%s' WHERE ((EMPLOYEE_ID='%s') AND (COMPANY_ID='%s'))"%(working_days,present_days, total_leave, type_of_leave, leave_deductions, empid ,cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			testid= cursor.rowcount
			conn.commit()
			conn.close()
			return testid
		except Exception,e:
			print str(e)
 
	def BNSlock(self, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT SALARY_REVISION_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			if lock==0:
				_sqlc_ = "UPDATE payrun_review SET SALARY_REVISION_LOCK=1 WHERE  (COMPANY_ID='%s')"%(cmpid)
			elif lock==1:
				_sqlc_ = "UPDATE payrun_review SET SALARY_REVISION_LOCK=0 WHERE  (COMPANY_ID='%s')"%(cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			_sqlc_ = "SELECT SALARY_REVISION_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			conn.commit()
			conn.close()
			return int(lock)
		except Exception,e:
			print str(e)
   
	def PNDlock(self, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT PAYMENT_DEDUCTION_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			if lock==0:
				_sqlc_ = "UPDATE payrun_review SET PAYMENT_DEDUCTION_LOCK=1 WHERE  (COMPANY_ID='%s')"%(cmpid)
			elif lock==1:
				_sqlc_ = "UPDATE payrun_review SET PAYMENT_DEDUCTION_LOCK=0 WHERE  (COMPANY_ID='%s')"%(cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			_sqlc_ = "SELECT PAYMENT_DEDUCTION_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			conn.commit()
			conn.close()
			return int(lock)
		except Exception,e:
			print str(e)
   
	def SHAlock(self, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT SALARY_HOLD_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			if lock==0:
				_sqlc_ = "UPDATE payrun_review SET SALARY_HOLD_LOCK=1 WHERE  (COMPANY_ID='%s')"%(cmpid)
			elif lock==1:
				_sqlc_ = "UPDATE payrun_review SET SALARY_HOLD_LOCK=0 WHERE  (COMPANY_ID='%s')"%(cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			_sqlc_ = "SELECT SALARY_HOLD_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			conn.commit()
			conn.close()
			return int(lock)
		except Exception,e:
			print str(e)
	
	def Reviewlock(self, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT EMPLOYEE_REVISION_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			if lock==0:
				_sqlc_ = "UPDATE payrun_review SET EMPLOYEE_REVISION_LOCK=1 WHERE  (COMPANY_ID='%s')"%(cmpid)
			elif lock==1:
				_sqlc_ = "UPDATE payrun_review SET EMPLOYEE_REVISION_LOCK=0 WHERE  (COMPANY_ID='%s')"%(cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			_sqlc_ = "SELECT EMPLOYEE_REVISION_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			conn.commit()
			conn.close()
			return int(lock)
		except Exception,e:
			print str(e)
   
	def Leavelock(self, cmpid):
		try:
			dbname = 'payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			_sqlc_ = "SELECT LEAVE_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			if lock==0:
				_sqlc_ = "UPDATE payrun_review SET LEAVE_LOCK=1 WHERE  (COMPANY_ID='%s')"%(cmpid)
			elif lock==1:
				_sqlc_ = "UPDATE payrun_review SET LEAVE_LOCK=0 WHERE  (COMPANY_ID='%s')"%(cmpid)
			print _sqlc_
			cursor.execute(_sqlc_)
			_sqlc_ = "SELECT LEAVE_LOCK FROM  payrun_review WHERE COMPANY_ID='%s'"%(cmpid)
			cursor.execute(_sqlc_)
			dbDetails=[]
			for row in cursor.fetchall():
				dbDetails.append(row)
			lock = int(dbDetails[0][0])
			conn.commit()
			conn.close()
			return int(lock)
		except Exception,e:
			print str(e)
   
class DeleteData():

	def deleteToken(self,mobile):
		try:
			dbname='server_simplified'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			sqlcmd='DELETE FROM cloudmessaging_token WHERE mobile="%s"'%(str(mobile))
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteCompany(self,cmpid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()
			
			#Delete Salary Components
			sqlcmd='DELETE FROM salary_components_reimbursements WHERE (COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			sqlcmd='DELETE FROM salary_components_deduction WHERE (COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			sqlcmd='DELETE FROM salary_components_earning WHERE (COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			print 1
			# Delete loans, payment schedules, payment_templates, payslip-templates
			sqlcmd='DELETE FROM payment_schedule WHERE (COMPANY_INFO_COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			# sqlcmd='DELETE FROM loans WHERE (EMPLOYEE_INFO_COMPANY_INFO_COMPANY_ID="%s")'%(cmpid)
			# cursor.execute(sqlcmd)
			sqlcmd='DELETE FROM payment_templates WHERE (COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			sqlcmd='DELETE FROM payslip_template WHERE (COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			print 2
			#Delete Employees
			sqlcmd='DELETE FROM employee_personal_info WHERE  (COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			sqlcmd='DELETE FROM employee_payment_info WHERE (COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			sqlcmd='DELETE FROM employee_info WHERE (COMPANY_INFO_COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			sqlcmd='DELETE FROM employee_salary_details WHERE (COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			print 3
			#Delete tax, epf, grade, preference settings
			sqlcmd='DELETE FROM company_tax_info WHERE (COMPANY_INFO_COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			sqlcmd='DELETE FROM company_preferences WHERE (COMPANY_INFO_COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			sqlcmd='DELETE FROM company_grade WHERE (COMPANY_INFO_COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			sqlcmd='DELETE FROM company_epf WHERE (COMPANY_INFO_COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			sqlcmd='DELETE FROM shifts WHERE (COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			print 4
			#Delete departments and branch
			sqlcmd='DELETE FROM departments WHERE (COMPANY_INFO_COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			sqlcmd='DELETE FROM branch WHERE (COMPANY_INFO_COMPANY_ID="%s")'%(cmpid)
			cursor.execute(sqlcmd)
			print 5
			#Delete Company
			sqlcmd='DELETE FROM company_info WHERE (id="%s")'%(cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)

			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def deleteBranch(self, bid):
	# try:
		dbname='payroll_db'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()

		#Delete Employees
		sqlcmd_='DELETE FROM employee_personal_info WHERE  EMPLOYEE_INFO_BRANCH_BRANCH_ID="%s"'%(bid)
		cursor.execute(sqlcmd_)
		sqlcmd='DELETE FROM employee_payment_info WHERE EMPLOYEE_INFO_BRANCH_BRANCH_ID="%s"'%(bid)
		cursor.execute(sqlcmd)
		_sqlcmd_='DELETE FROM employee_info WHERE BRANCH_BRANCH_ID="%s"'%(bid)
		cursor.execute(_sqlcmd_)


		
		sqlcmd='DELETE FROM branch WHERE id="%s"'%(bid)
		cursor.execute(sqlcmd)

		count = cursor.rowcount
		conn.commit()
		conn.close()
		return count
	# except Exception,e:
	# 	return 0
	# 	print str(e)
	
	def deleteDepartment(self, did):
	# try:
		dbname='payroll_db'
		conn = connect_to_cloudsql(dbname)
		cursor = conn.cursor()

		#Delete Employees
		sqlcmd='DELETE FROM employee_personal_info WHERE  EMPLOYEE_INFO_DEPARTMENTS_DEPARTMENT_ID="%s"'%(did)
		cursor.execute(sqlcmd)
		sqlcmd='DELETE FROM employee_payment_info WHERE EMPLOYEE_INFO_DEPARTMENTS_DEPARTMENT_ID="%s"'%(did)
		cursor.execute(sqlcmd)
		sqlcmd='DELETE FROM employee_info WHERE DEPARTMENTS_DEPARTMENT_ID="%s"'%(did)
		cursor.execute(sqlcmd)


		
		sqlcmd='DELETE FROM departments WHERE id="%s"'%(did)
		cursor.execute(sqlcmd)

		count = cursor.rowcount
		conn.commit()
		conn.close()
		return count
	# except Exception,e:
	# 	return 0
	# 	print str(e)
	
	def deleteDesignation(self, did):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()

			# Delete Employees
			# sqlcmd='DELETE FROM employee_personal_info WHERE  EMPLOYEE_INFO_DEPARTMENTS_DEPARTMENT_ID=%s'%(did)
			# cursor.execute(sqlcmd)
			# sqlcmd='DELETE FROM employee_payment WHERE EMPLOYEE_INFO_DEPARTMENTS_DEPARTMENT_ID=%s'%(did)
			# cursor.execute(sqlcmd)
			# sqlcmd='DELETE FROM employee_info WHERE DEPARTMENTS_DEPARTMENT_ID=%s'%(did)
			# cursor.execute(sqlcmd)


			
			sqlcmd='DELETE FROM company_grade WHERE id="%s"'%(did)
			cursor.execute(sqlcmd)

			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteComponentEarning(self, cid,compid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()		
			sqlcmd='DELETE FROM salary_components_earning WHERE ((id="%s") AND (COMPANY_ID="%s"))'%(compid,cid)
			cursor.execute(sqlcmd)
			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def deleteShift(self, sid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()

			# Delete Employees
			# sqlcmd='DELETE FROM employee_personal_info WHERE  EMPLOYEE_INFO_DEPARTMENTS_DEPARTMENT_ID=%s'%(did)
			# cursor.execute(sqlcmd)
			# sqlcmd='DELETE FROM employee_payment WHERE EMPLOYEE_INFO_DEPARTMENTS_DEPARTMENT_ID=%s'%(did)
			# cursor.execute(sqlcmd)
			# sqlcmd='DELETE FROM employee_info WHERE DEPARTMENTS_DEPARTMENT_ID=%s'%(did)
			# cursor.execute(sqlcmd)


			
			sqlcmd='DELETE FROM shifts WHERE id="%s"'%(sid)
			print sqlcmd
			cursor.execute(sqlcmd)

			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)

	def DeleteBNSRow(self, cmpid, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()			
			sqlcmd='DELETE FROM payrun_review WHERE (EMPLOYEE_ID="%s") AND (COMPANY_ID="%s")'%(empid, cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)

			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)
	
	def DeletePNDRow(self, cmpid, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()			
			sqlcmd='DELETE FROM payrun_review WHERE (EMPLOYEE_ID="%s") AND (COMPANY_ID="%s")'%(empid, cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)

			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)
   
	def DeleteSHARow(self, cmpid, empid):
		try:
			dbname='payroll_db'
			conn = connect_to_cloudsql(dbname)
			cursor = conn.cursor()			
			sqlcmd='DELETE FROM payrun_review WHERE (EMPLOYEE_ID="%s") AND (COMPANY_ID="%s")'%(empid, cmpid)
			print sqlcmd
			cursor.execute(sqlcmd)

			count = cursor.rowcount
			conn.commit()
			conn.close()
			return count
		except Exception,e:
			return 0
			print str(e)