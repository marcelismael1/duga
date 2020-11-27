from flask import Flask, render_template, url_for, redirect, request, jsonify
import pymongo

import uuid
# from models import *



app = Flask(__name__)

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.duga

# # Routes
# from alldata import routes

# Static Data
headings = ("System IP","DATE", "CVE NO", "SEVERITY", "AFFECTED PACKAGES", "PACKAGE NUMBER")

data = (
	("210.x.x.x", "2020-Sep-27 18:20", "CVE-210.x.x.x 2020-Sep-27 18:20 2019-1010298", "Critical", "Chrome", "50.23"),
	("210.x.x.x", "2020-Sep-27 18:20", "CVE-210.x.x.x 2020-Sep-28 18:20 2019-1010298", "Normal", "Chrome", "50.23"),
	("210.x.x.x", "2020-Sep-27 18:20", "CVE-210.x.x.x 2020-Sep-29 18:20 2019-1010298", "Critical", "Chrome", "50.23"),

	)

configurationdata = [
	["WindowsOS1", "200.100.2.2", "Full Scan", "On", "Full Scan", "Weekly"],
	["WindowsOS2", "200.100.2.3", "Full Scan", "On", "Full Scan", "Daily"],

	]

notificationdata = (
	("On", "1", "Test", "123"),
	("Off", "2", "Test", "456"),

	)

SOFAlarms = [300,50,100,200]
Totalseverity = [600,50,100,200]





# def adddata():


# 	alldata = {
# 	"_id" : "",
# 	"systemip" : "",
# 	"systemname" : "",
# 	"systemgroup" : "",
# 	"activation" : "",
# 	"scantype" : "",
# 	"frequency" : "",
# 	"scantype" : "",
	

# 	}

# 	return jsonify(alldata), 200




# Main route
@app.route('/')
def main():
    return dashboard()

# dashboards endpoint
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", headings=headings, data=data, SOFAlarms=SOFAlarms, Totalseverity=Totalseverity)

# alerts endpoint
@app.route('/alerts')
def alerts():
    return render_template("alerts.html", headings=headings, data=data)

# Config endpoint
@app.route('/configurations')
def configurations():
    return render_template("configurations.html" , configurationdata=configurationdata, notificationdata=notificationdata)
    # return redirect(url_for('configurations.html') , confdata=configurationdata, notificationdata=notificationdata)

# about endpoint
@app.route('/about')
def about():
    return render_template("about.html")

# default route
@app.route('/<name>')
def default_route(name):
    return redirect(url_for('main'))

@app.route('/addconf/', methods=["POST", "GET"])
def addconf():
	if request.method == 'POST':

		systemname = request.form["systemname"]
		systemip = request.form["systemip"] 
		systemgroup = request.form["systemgroup"]
		activation = request.form["activation"]
		scantype = request.form["scantype"]
		frequency = request.form["frequency"]
		# configurationdata.extend((systemname, systemip, systemgroup, activation, scantype, frequency))
		newconfig = [systemname, systemip, systemgroup, activation, scantype, frequency]
		configurationdata = configurationdata + newconfig
		print(configurationdata)
		return redirect(url_for("configurations"))
	else:
		return render_template("configurations.html")



# @app.route('/alldata/', methods=['GET', 'POST'])
# def adddata():
# 	# return adddata()
# 	alldata = {
# 	"_id" : "",
# 	"systemip" : "",
# 	"systemname" : "",
# 	"systemgroup" : "",
# 	"activation" : "",
# 	"scantype" : "",
# 	"frequency" : "",
# 	"scantype" : "",
	

# 	}

# 	return jsonify(alldata), 200

@app.route('/alldata/', methods=['POST', 'GET'])
# def adddata():
# 	return Alldata().adddata()
def adddata():

	req = request.form
	alldata = {
	"_id" : uuid.uuid4().hex,
	"systemip" : request.form.get("systemip"),
	"systemname" : request.form.get("systemname"),
	"systemgroup" :request.form.get("systemgroup"),
	"activation" : request.form.get("activation"),
	"scantype" : request.form.get("scantype"),
	"frequency" :request.form.get("frequency"),
	"scantype" : request.form.get("scantype"),
	

	}




	db.alldata.insert_one(alldata)
	

	return jsonify(req), 200






if __name__ == "__main__":
    app.run(debug=True)