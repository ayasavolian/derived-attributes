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


@app.route("/")
def home():
	return render_template('upload.html')

@app.route("/upload")
def upload_route():
	return render_template('upload.html')

@app.route("/uploader", methods=['POST'])
def uploader_route():
	if request.method == 'POST':
		print "01"
		csv = request.files['file']
		uploaded = initiater("uploader", csv)
		print "05"
		return json.dumps(uploaded)

@app.route("/upload-preview", methods=['POST'])
def upload_preview():
	if request.method == 'POST':
		data = request.json
		preview = initiater("preview", data)
		return json.dumps(preview)

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
