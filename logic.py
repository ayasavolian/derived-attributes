# *************************************************************************************
#
#  @author - Arrash
#  @last_modified - 1/4/2016
#  @date - 1/4/2016
#  @version - 1.0.0
#  @purpose - This is the logic page of the Flask application for Derived Attributes
#  this will communicate with the logic.py page in order to complete tasks
#
# *************************************************************************************

import csv
import re
from datetime import datetime

# *************************************************************************************
#
# This class performs all the computation for the uploaded file from CS that needs to have
# derived attribute
#
# *************************************************************************************

class Upload(object):
	def __init__(self, file_passed):
		self.passed = file_passed

# *************************************************************************************
#
# This is a function that spits back the dictionary which the proper formatting to pass
# back for routing
#
# *************************************************************************************

	@staticmethod
	def error_check(error, receipt):
		resp = {
			'error' : error,
			'receipt' :	receipt
		}
		return resp

# *************************************************************************************
#
# This is for the initial upload. It will read the csv and convert everything into an
# array within an array
#
# *************************************************************************************

	def uploader_csv(self):
		fileUploaded = self.passed
		read = csv.reader(fileUploaded)
		return_val = []
		for row in read:
			return_val.append(row)
		vals = {
			'csv_response' : return_val
		}
		return vals

# *************************************************************************************
#
# this method will take the values that have been chosen for the drop down options for the different fields 
# and automatically create the additional columns necessary based on the values passed. The values it calculates are 
# based on 8 fields. The Date Type field, the Original Hire Date, the Position's Start Date, the Email Address, 
# the Employee ID, the Manager Employee ID, the Termination Date, and the Age/Birth Date field. Based on the values provided
# the additional columsn are added. Below is an outline of the columns added based on the values provided.

# -> Tenure : Current Date - Original Hire Date
# -> Generation : Current Date - Age/Birth Date
# -> Active/Inactive : Current Date - Termination Date
# -> Directs : Lookup logic based on the manager employee ID and mapping of values (rows_by_manager_id, manager_indirects, rows_by_email address)
# -> Indirects : Lookup logic based on the manager employee ID and mapping of values and the manager hierarchy (rows_by_manager_id, manager_indirects, rows_by_email address)
# -> Time in Position : Current Date - Position Start Date
# -> Manager Email : email address of the manager based on the Manager Employee ID
#
# *************************************************************************************

	def preview(self):
		# This is the dictionary that has been passed in that holds a variety of values, such as the csv, dateFormat, and the field locations
		vals = self.passed
		# This bool lets us know if there is a critical error that has occurred. If there has been one it will become true
		no_error = True
		# This dictionary just lets us know if there has been an error.
		error = {"no date chosen": 0, "missing age fields": 0, "missing essential date fields": 0, "missing termination date": 0, "missing manager fields": 0, "manager missing": 0}
		# X is used for the first iteration of the loop through the csv array
		x = 0
		# positions holds the location of all of the fields that are used to be manipulated
		positions = vals['positions']
		# csv is the actual csv that has been converted to an array within an array
		csv = vals['csv']
		# this is essentially a boolean that helps us determine if age is used or if birth year has been used
		age = 0
		# This is testing to see if dateformat is available. If its not available then perform no more logic and pass back the error
		# if at any point no_error is False then there will be no more computation of values
		if positions['dateFormat'] != "None":
			date = positions['dateFormat']	
		else:
			no_error = False
			error["no date chosen"] = 1	
		# checking to see if age exists or if its birthYear thats provided
		try:
			positions['age']
		except KeyError:
			pass
		else:
			age = 1
			age_num = positions['age']
		try:
			positions['birthYear'] and age != 0
		except KeyError:
			error["missing age fields"] = 1
		else:
			birth_year_num = positions['birthYear']
		try:
			str(positions['hireDate']) and str(positions['startDate']) and no_error
		except KeyError:
			error["missing essential date fields"] = 1
			no_error = False
		else:		
			hire_date = positions['hireDate']
			start_date = positions['startDate']
		try:
			str(positions['terminationDate']) and no_error
		except KeyError:
			error["missing termination date"] = 1
		else:		
			termination_date = positions['terminationDate']
		try:
			str(positions['managerEmployeeID']) and str(positions['employeeID']) and str(positions['email']) and no_error
		except KeyError:
			error["missing manager fields"] = 1
		else:
			employee_manager_ID = positions['managerEmployeeID']
			employee_ID = positions['employeeID']
			email_address = positions['email']
			no_header_csv = csv[1:]
			rows_by_manager_id = dict((arr[employee_ID], arr[employee_manager_ID]) for arr in no_header_csv)
			manager_indirects = dict((arr[employee_ID], 0) for arr in no_header_csv)
			rows_by_email_address = dict((arr[employee_ID], arr[email_address]) for arr in no_header_csv)
			manager_undefined = []
			manager_list = []
			manager_hierarchy = {}
			manager_email_by_id = {}
			manager_directs = {}
			for arr in rows_by_manager_id:
				try:
					rows_by_email_address[str(rows_by_manager_id[arr])]
				except KeyError:
					no_error = False
					error["manager missing"] = 1
					manager_undefined.append(rows_by_manager_id[arr])
				else:
					manager_email_by_id[rows_by_manager_id[arr]] = rows_by_email_address[str(rows_by_manager_id[arr])]
					manager_directs[rows_by_manager_id[arr]] = 0
			if no_error:
				for arr in no_header_csv:
					hierarchy = True
					val = 1
					if arr[employee_ID] != arr[employee_manager_ID] and arr[employee_manager_ID] != "":
						manager_hierarchy[arr[employee_ID]] = {val: arr[employee_manager_ID]}
						val += 1
						if arr[employee_manager_ID] != rows_by_manager_id[str(arr[employee_manager_ID])] and rows_by_manager_id[str(arr[employee_manager_ID])] != "":
							manager_hierarchy[str(arr[employee_ID])][val] = rows_by_manager_id[str(arr[employee_manager_ID])]
							temp_manager = rows_by_manager_id[str(arr[employee_manager_ID])]
							val +=1
							if rows_by_manager_id[str(arr[employee_manager_ID])] != rows_by_manager_id[temp_manager] and rows_by_manager_id[str(arr[employee_manager_ID])] != "":
								manager_hierarchy[str(arr[employee_ID])][val] = rows_by_manager_id[temp_manager]
								temp_manager_two = rows_by_manager_id[temp_manager]
								val += 1
								while hierarchy:
									if rows_by_manager_id[temp_manager_two] != rows_by_manager_id[temp_manager] and rows_by_manager_id[temp_manager_two] != "":
										manager_hierarchy[str(arr[employee_ID])][val] = rows_by_manager_id[temp_manager_two]
										temp_manager = temp_manager_two
										temp_manager_two = rows_by_manager_id[temp_manager_two]
										val += 1
										if val == 25:
											break;
									else:
										hierarchy = False							
					else:
						pass
		if no_error:
			if error["missing manager fields"] == 0:
				for arr in csv:
					try:
						manager_directs[str(arr[employee_manager_ID])]
					except KeyError:
						pass
					else:
						manager_directs[str(arr[employee_manager_ID])] = int(manager_directs[str(arr[employee_manager_ID])]) + 1
				for arr in manager_directs:
					try:
						manager_hierarchy[arr]
					except KeyError:
						pass
					else:
						for i in xrange(1,len(manager_hierarchy[arr])+1):
							manager_indirects[str(manager_hierarchy[arr][i])] += manager_directs[arr]
			for array in csv:
				if x == 0:
					array.append("Tenure")
					array.append("Generation")
					array.append("Time in Position")
					if error["missing manager fields"] == 0:
						array.append("Manager Email")
						array.append("Directs")
						array.append("Indirects")
					if error["missing termination date"] == 0:
						array.append("Active/Inactive")
					x = 1
				else:
					dash = r'-'
					slash = '/'
					person_hire_date = array[hire_date]
					person_start_date = array[start_date]
					person_hire_date = re.sub(dash, slash, person_hire_date)
					person_start_date = re.sub(dash, slash, person_start_date)
					term_exists = True
					if error["missing termination date"] == 0:
						try:
							person_termination_date = array[termination_date]
						except KeyError:
							term_exists = False
						else:
							if person_termination_date is not None and person_termination_date != "":
								person_termination_date = re.sub(dash, slash, person_termination_date)
							else:
								term_exists = False
					long_date_format_chosen = r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}'
					long_date_reverse_format_chosen = r'\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2}'
					date_format_chosen = r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{1,2}'
					short_end = r'\d{2}$'
					if date == "mm/dd/yy or mm-dd-yy":
						m = re.findall(date_format_chosen, person_hire_date)
						if m:
							end_year = re.findall(short_end, person_hire_date)
							start_end_year = re.findall(short_end, person_start_date)
							if int(start_end_year[0]) < 25:
								final_start_year = "20" + start_end_year[0]
							else:
								final_start_year = "19" + start_end_year[0]
							if int(end_year[0]) < 25:
								final_year = "20" + end_year[0]
							else:
								final_year = "19" + end_year[0]
							if error["missing termination date"] == 0 and term_exists:
								termination_year = re.findall(short_end, person_termination_date)
								if int(termination_year[0]) < 25:
									final_termination_year = "20" + termination_year[0]
								else:
									final_termination_year = "19" + termination_year[0]
								person_termination_date = re.sub(short_end, final_termination_year , person_termination_date)
								final_termination_date = datetime.strptime(person_termination_date, '%m/%d/%Y')
							person_start_date = re.sub(short_end, final_start_year , person_start_date)
							person_hire_date = re.sub(short_end, final_year , person_hire_date)
							final_start_date = datetime.strptime(person_start_date, '%m/%d/%Y')
							final_hire_date = datetime.strptime(person_hire_date, '%m/%d/%Y')
						else:
							return self.error_check("date format match", csv)
							# return "date format chosen does not match the date of the actual field"
					elif date == "mm/dd/yyyy or mm-dd-yyyy":
						m = re.findall(long_date_format_chosen, person_hire_date)
						if m:					
							final_start_date = datetime.strptime(person_start_date, '%m/%d/%Y')
							final_hire_date = datetime.strptime(person_hire_date, '%m/%d/%Y')
							if error["missing termination date"] == 0 and term_exists:
								final_termination_date = datetime.strptime(person_termination_date, '%m/%d/%Y')
						else:
							return self.error_check("date format match", csv)
					elif date == "dd/mm/yy or dd-mm-yy":
						formatMM  = r'[\/\-]\d{1,2}'
						formatDD = r'\d{1,2}'
						m = re.findall(date_format_chosen, person_hire_date)
						if m:
							end_year = re.findall(short_end, person_hire_date)
							start_end_year = re.findall(short_end, person_start_date)
							if int(start_end_year[0]) < 25:
								final_start_year = "20" + start_end_year[0]
							else:
								final_start_year = "19" + start_end_year[0]
							if int(end_year[0]) < 25:
								final_year = "20" + end_year[0]
							else:
								final_year = "19" + end_year[0]
							if error["missing termination date"] == 0 and term_exists:
								termination_year = re.findall(short_end, person_termination_date)
								if int(termination_year[0]) < 25:
									final_termination_year = "20" + termination_year[0]
								else:
									final_termination_year = "19" + termination_year[0]
								person_termination_date = re.sub(short_end, final_termination_year , person_termination_date)
								final_termination_date = datetime.strptime(person_termination_date, '%d/%m/%Y')
							person_start_date = re.sub(short_end, final_start_year , person_start_date)
							person_hire_date = re.sub(short_end, final_year , person_hire_date)
							final_start_date = datetime.strptime(person_start_date, '%d/%m/%Y')
							final_hire_date = datetime.strptime(person_hire_date, '%d/%m/%Y')
						else:
							return self.error_check("date format match", csv)
					elif date == "yyyy/mm/dd or yyyy-mm-dd":
						m = re.findall(long_date_reverse_format_chosen, person_hire_date)
						if m:					
							final_start_date = datetime.strptime(person_start_date, '%Y/%m/%d')
							final_hire_date = datetime.strptime(person_hire_date, '%Y/%m/%d')
							if error["missing termination date"] == 0 and term_exists:
								final_termination_date = datetime.strptime(person_termination_date, '%Y/%m/%d')
						else:
							return self.error_check("date format match", csv)

					elif date == "mm/dd/yyyy or mm-dd-yyyy":
						m = re.findall(long_date_format_chosen, person_hire_date)
						if m:					
							final_start_date = datetime.strptime(person_start_date, '%d/%m/%Y')
							final_hire_date = datetime.strptime(person_hire_date, '%d/%m/%Y')
							if error["missing termination date"] == 0 and term_exists:
								final_termination_date = datetime.strptime(person_termination_date, '%d/%m/%Y')
						else:
							return error_check("date format match", csv)
					else:
						return self.error_check("no date chosen", csv)
					curr_date = datetime.now()
					year = datetime.now().year
					final_time_diff = abs((curr_date - final_start_date).days)
					final_start_time_diff = abs((curr_date - final_hire_date).days)
					if age_num:
						year_born = year - int(array[age_num])
					elif birth_year_num:
						year_born = int(array[birth_year_num])
					if  not vals['generationArr']:
						if year_born < 1925:
							generation = "G.I. Generation"
						elif year_born >= 1925 and year_born <= 1946:
							generation = "Silent Generation"
						elif year_born > 1946 and year_born <= 1965:
							generation = "Baby Boomer"
						elif year_born > 1965 and year_born <= 1980:
							generation = "Generation X"
						elif year_born > 1980 and year_born <= 2000:
							generation = "Generation Y"
						else:
							generation = "Generation Z"
					else:
						for gen in vals['generationArr']:
							print gen
							if year_born > int(gen['start']) and year_born <= int(gen['end']):
								generation = gen['title']
								print generation
								break
						if generation is None:
							generation = vals['generationArr'][len(vals['generationArr'])-1]['title']
					if not vals['tenureArr']:	
						if final_time_diff < 365:
							tenure = "<1 Year"
						elif final_time_diff > 365 and final_time_diff <= 730:
							tenure = "1-2 Years"
						elif final_time_diff > 730 and final_time_diff <= 1095:
							tenure = "2-3 Years"
						elif final_time_diff > 1095 and final_time_diff <= 1460:
							tenure = "3-4 Years"
						elif final_time_diff > 1460 and final_time_diff <= 1825:
							tenure = "4-5 Years"
						elif final_time_diff > 1825 and final_time_diff <= 2555:
							tenure = "5-7 Years"
						else:
							tenure = "7+ Years"
						if final_start_time_diff < 365:
							start_tenure = "<1 Year"
						elif final_start_time_diff > 365 and final_start_time_diff <= 730:
							start_tenure = "1-2 Years";
						elif final_start_time_diff > 730 and final_start_time_diff <= 1095:
							start_tenure = "2-3 Years";
						elif final_start_time_diff > 1095 and final_start_time_diff <= 1460:
							start_tenure = "3-4 Years";
						elif final_start_time_diff > 1460 and final_start_time_diff <= 1825:
							start_tenure = "4-5 Years";
						elif final_start_time_diff > 1825 and final_start_time_diff <= 2555:
							start_tenure = "5-7 Years"
						else:
							start_tenure = "7+ Years"
					else:
						for ten in vals['tenureArr']:
							if final_time_diff > int(ten['start']) and final_time_diff <= int(ten['end']):
								tenure = ten['title']
							if final_start_time_diff > int(ten['start']) and final_start_time_diff <= int(ten['end']):
								start_tenure = ten['title']
						if tenure is None:
							tenure = vals['tenureArr'][len(vals['tenureArr'])-1]['title']
						if start_tenure is None:
							start_tenure = vals['tenureArr'][len(vals['tenureArr'])-1]['title']
					array.append(start_tenure)
					array.append(generation)
					array.append(tenure)
					if error["missing manager fields"] == 0:
						final_manager_email = manager_email_by_id[str(array[employee_manager_ID])]
						array.append(final_manager_email)
						try:
							manager_directs[str(array[employee_ID])]
						except KeyError:
							array.append(0)
						else:
							array.append(manager_directs[str(array[employee_ID])])
						try:
							manager_indirects[str(array[employee_ID])]
						except KeyError:
							array.append(0)
						else:
							total_indirects = manager_indirects[str(array[employee_ID])] + array[len(array)-1]
							array.append(total_indirects)
					if error["missing termination date"] == 0 and term_exists:
						if curr_date > final_termination_date:
							array.append("INACTIVE")
						else:
							array.append("ACTIVE")
					elif error["missing termination date"] == 0:
						array.append("ACTIVE")
		else:
			if error["manager missing"] == 1:
				for manager in manager_undefined:
				  if manager not in manager_list:
				    manager_list.append(manager)
				return self.error_check(error, manager_list)
		return self.error_check(error, csv)

# *************************************************************************************
#
# This is the function that communicates with route.py in order to perform specific
# functions. 
#
# *************************************************************************************

def initiater(run, val):
	if run == "uploader":
		upload = Upload(val)
		return upload.uploader_csv()
	if run == "preview":
		upload_preview = Upload(val)
		return upload_preview.preview()

