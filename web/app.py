from flask import Flask, render_template, url_for, redirect, request, jsonify
import pymongo
from functions import *
import uuid
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Mongo
mongodb = config['db']['mongodb']
mongoport = int(config['db']['mongoport'])
cve_collection = config['db']['cve_collection']
mongo_database = config['db']['mongodatabase']
sys_config_coll = config['db']['sys_config_coll']



app = Flask(__name__)

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.duga



# Static Data
headings = ("System IP","DATE", "CVE NO", "SEVERITY", "AFFECTED PACKAGES", "PACKAGE NUMBER")

data = (
	("210.x.x.x", "2020-Sep-27 18:20", "CVE-210.x.x.x 2020-Sep-27 18:20 2019-1010298", "Critical", "Chrome", "50.23"),
	("210.x.x.x", "2020-Sep-27 18:20", "CVE-210.x.x.x 2020-Sep-28 18:20 2019-1010298", "Normal", "Chrome", "50.23"),
	("210.x.x.x", "2020-Sep-27 18:20", "CVE-210.x.x.x 2020-Sep-29 18:20 2019-1010298", "Critical", "Chrome", "50.23"),

	)


notificationdata = (
	("On", "1", "Test", "123"),
	("Off", "2", "Test", "456"),

	)

SOFAlarms = [300,50,100,200]
Totalseverity = [600,50,100,200]










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
	sys_config = get_sys_config()
	return render_template("configurations.html" , configurationdata=sys_config)

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





@app.route('/sys_config_table/<action>', methods=['POST', 'GET'])
@app.route('/sys_config_table/<action>/<ip>', methods=['GET'])
def sys_config_table(action,ip):

	if action == 'new':
		req = request.form
		data = {
		"systemip" : request.form.get("systemip"),
		"systemname" : request.form.get("systemname"),
		"systemgroup" :request.form.get("systemgroup"),
		"activation" : request.form.get("activation"),
		"scantype" : request.form.get("scantype"),
		"frequency" : request.form.get("frequency"),
		"scantype" : request.form.get("scantype"),
		}
		save_to_mongo(sys_config_coll, data)
		# return redirect(url_for("configurations"))
	elif action == 'delete':
		delete_from_mongo(sys_config_coll, {'systemip':ip})
	else:
		return None
	return redirect(url_for("configurations"))

########################################################################
#							FUNCTIONS
########################################################################

def get_sys_config():
	sys_config = read_from_mongo(sys_config_coll, {})
	sys_config_data = []
	for i in sys_config:
		data = [i['systemname'],i['systemip'],i['systemgroup'],i['activation'],i['scantype'],i['frequency']]
		sys_config_data.append(data)
	return sys_config_data


if __name__ == "__main__":
    app.run(debug=True)