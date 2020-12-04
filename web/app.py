from flask import Flask, render_template, url_for, redirect, request, jsonify
import pymongo
from functions import *
import uuid
import configparser
import time

config = configparser.ConfigParser()
config.read('../config.ini')

# Mongo
mongodb = config['db']['mongodb']
mongoport = int(config['db']['mongoport'])
cve_collection = config['db']['cve_collection']
mongo_database = config['db']['mongodatabase']
sys_config_coll = config['db']['sys_config_coll']
not_config_coll = config['db']['not_config_coll']
alarms_coll = config['db']['alarms_coll']

app = Flask(__name__)

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.duga

# Static Data for Dashboard
headings = ("System IP","DATE", "CVE NO", "SEVERITY", "AFFECTED PACKAGES", "PACKAGE NUMBER")

alertsdata = (
	("210.x.x.x", "2020-Sep-27 18:20", "CVE-210.x.x.x 2020-Sep-27 18:20 2019-1010298", "Critical", "Chrome", "50.23"),
	("210.x.x.x", "2020-Sep-27 18:20", "CVE-210.x.x.x 2020-Sep-28 18:20 2019-1010298", "Normal", "Chrome", "50.23"),
	("210.x.x.x", "2020-Sep-27 18:20", "CVE-210.x.x.x 2020-Sep-29 18:20 2019-1010298", "Critical", "Chrome", "50.23"),

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
    return render_template("dashboard.html", headings=headings, data=alertsdata, SOFAlarms=SOFAlarms, Totalseverity=Totalseverity)

# alerts endpoint
@app.route('/alerts')
def alerts():
	alertsdata = get_alarms_data()
	return render_template("alerts.html" , data=alertsdata)

# Config endpoint
@app.route('/configurations')
def configurations():
	sys_config = get_sys_config()
	not_config = get_not_config()
	return render_template("configurations.html" , configurationdata=sys_config, configurationnot=not_config)

# about endpoint
@app.route('/about')
def about():
    return render_template("about.html")

# default route
@app.route('/<name>')
def default_route(name):
    return redirect(url_for('main'))

@app.route('/sys_config_table/<action>', methods=['POST', 'GET'])
@app.route('/sys_config_table/<action>/<ip>', methods=['GET'])
def sys_config_table(action,ip=None):

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

@app.route('/not_config_table/<action>', methods=['POST', 'GET'])
@app.route('/not_config_table/<action>/<id>', methods=['GET'])
def not_config_table(action,id=None):

	if action == 'new':
		req = request.form
		data = {
		"nactivate" : request.form.get("nactivate"),
		"channel" : request.form.get("channel"),
		"botname" :request.form.get("botname"),
		"token_id" : request.form.get("token_id"),
		}
		save_to_mongo(not_config_coll, data)
		# return redirect(url_for("configurations"))
	elif action == 'delete':
		delete_from_mongo(not_config_coll, {'token_id':id})
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

def get_not_config():
	not_config = read_from_mongo(not_config_coll, {})
	not_config_data = []
	for i in not_config:
		data = [i['nactivate'],i['channel'],i['botname'],i['token_id']]
		not_config_data.append(data)
	return not_config_data

def get_alarms_data():
	alerts = read_from_mongo(alarms_coll, {})
	alertsdata = []
	for i in alerts:
		cve_list = []
		for k,v in i['cve_list'].items():
			cve_list.append([k,v])
		alarmtime = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(int(i['creationDate'])))
		data = [i['ip'],alarmtime,cve_list[0][0],cve_list[0][1],i['package_name'],i['package_version']]
		alertsdata.append(data)
	return alertsdata

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")