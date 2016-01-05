# *************************************************************************************
#
#  @author - Arrash
#  @last_modified - 1/5/2016
#  @date - 1/5/2016
#  @version - 1.0.0
#  @purpose - This is the routing page of the Flask application for Derived Attributes
#  this will communicate with the logic.py page in order to complete tasks
#
# *************************************************************************************

from flask import *
from logic import *
import string
import random
import json
from urllib import urlencode
import StringIO 
import io
import csv
import pyexcel as pe


app = Flask(__name__)
app.secret_key = "F8u15h9hgd09hgaw4nogo23i188"


# *************************************************************************************
#
# This is the actual home page that should run the upload.html page and allow CS
# to upload whatever file they receive from the customer and automatically derive attributes
#
# *************************************************************************************

@app.route("/")
def home():
	return render_template('upload.html')

@app.route("/upload")
def upload_route():
	return render_template('upload.html')

# *************************************************************************************
#
# This will accept the uploaded file and pass the file to a function in logic that will
# turn the file into an array within an array to be displayed to the user on the FE
#
# *************************************************************************************

@app.route("/uploader", methods=['POST'])
def uploader_route():
	if request.method == 'POST':
		csv = request.files['file']
		uploaded = initiater("uploader", csv)
		return json.dumps(uploaded)

# *************************************************************************************
#
# This will accept the uploaded file and pass the file to a function in logic that will
# turn the file into an array within an array to be displayed to the user on the FE
#
# *************************************************************************************

@app.route("/upload-preview", methods=['POST'])
def upload_preview():
	if request.method == 'POST':
		data = request.json
		preview = initiater("preview", data)
		return json.dumps(preview)

# *************************************************************************************
#
# this route provides the user with the final csv thats pushed into their downloads
# folder after the attributes are derived. We do this by taking the dictionary thats
# provided and splitting the dictionary upon commas. We then split for end of the line
# using the length of the arrays within the dictionary which is provided by "length". 
# After we turn the array into an excel sheet using pe and save it to memory to pass
# back to the user.
#
# *************************************************************************************

@app.route("/download-csv", methods=['POST'])
def download():
	if request.method == 'POST':
		data = request.form['csv']
		data_length = request.form['length']
		csv = data.split(',')
		final_csv = []
		temp_arr = []
		for index, val in enumerate(csv):
			index = index + 1
			temp_arr.append(str(val))
			if index % int(data_length) == 0 and index != 1:
				final_csv.append(temp_arr)
				temp_arr = []
		sheet = pe.Sheet(final_csv)
		io = StringIO.StringIO()
		sheet.save_to_memory("csv", io)
		output = make_response(io.getvalue())
		output.headers["Content-Disposition"] = "attachment; filename=customer_export.csv"
		output.headers["Content-type"] = "text/csv"
		return output

if __name__ == "__main__":
    app.secret_key = "F8u15h9hgd09hgaw4nogo23i188"
    app.run()
