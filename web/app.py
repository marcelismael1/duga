from flask import Flask, render_template, url_for, redirect, request, jsonify
import pymongo
from functions import *
import uuid
import configparser
import time, os, sys
from collections import Counter



currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from backend.orm_engine import *

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(dir_path+'/../config.ini')

# Mongo
mongodb = config['db']['mongodb']
mongoport = int(config['db']['mongoport'])
cve_collection = config['db']['cve_collection']
mongo_database = config['db']['mongodatabase']
sys_config_coll = config['db']['sys_config_coll']
not_config_coll = config['db']['not_config_coll']
alarms_coll = config['db']['alarms_collection']

app = Flask(__name__)

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.duga

# Main route
@app.route('/')
def main():
    return dashboard()

# dashboards endpoint
@app.route('/dashboard')
def dashboard():
	alarms_count, unresolved_alarms_count = get_alarms_summary()
	systems_count = get_number_of_systems()
	return render_template("dashboard.html", alarms_count= alarms_count, unresolved_alarms_count=unresolved_alarms_count, systems_count=systems_count)

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
		}
		config = Sys_conf(systemip = req.get("systemip"), systemname= req.get("systemname"), systemgroup = req.get("systemgroup") , activation= req.get("activation"), scantype= req.get("scantype"), frequency= req.get("frequency")).save()
		# return redirect(url_for("configurations"))
	elif action == 'delete':
		obj = Sys_conf.objects(systemip = ip)
		obj.delete()
	else:
		return None
	return redirect(url_for("configurations"))

@app.route('/not_config_table/<action>', methods=['POST', 'GET'])
@app.route('/not_config_table/<action>/<id>', methods=['GET'])
def not_config_table(action,id=None):

	if action == 'new':
		req = request.form
		config = Notif_conf(nactivate = req.get("nactivate"), channel= req.get("channel"), botname = req.get("botname") , token_id= req.get("token_id")).save()
	elif action == 'delete':
		obj = Notif_conf.objects(token_id = id)
		obj.delete()
	else:
		return None
	return redirect(url_for("configurations"))


#########################################################################
#							Charts										#
#########################################################################
@app.route('/charts/<action>', methods=['GET'])
def charts(action):

    if action == 'get_cve_types_chart':
        get_cve_types_data = get_cve_severity()
        return get_cve_types_data




#########################################################################
#							FUNCTIONS									#
#########################################################################

# dashboard functions
def get_alarms_summary():
		alerts = Alarms.objects
		unresolved_count = 0

		for a in alerts:
    			if a.resolved == False:
    					unresolved_count += 1
		return len(alerts), unresolved_count

def get_number_of_systems():
		sys_config = Sys_conf.objects
		return len(sys_config)

def get_crit_severity(severity_list):
            severity = ["CRITICAL", "HIGH", "MEDIUEM", "LOW"]
            s = [ i  for i in severity if i in severity_list ]
            if len(s) > 0:
                return s[0]

def get_cve_severity():
		alarms = Alarms.objects.only("cve_list")
		alarms = [alarm.cve_list for alarm in alarms]
		alarms = [get_crit_severity(list(alarm.values())) for alarm in alarms]
		alarms = [alarm for alarm in alarms if alarm != None]
		data = {
        'labels' : list(Counter(alarms).keys()),
        'values' : list(Counter(alarms).values())
        }
		return data


###-------------------------------------––-----------###
def get_sys_config():
	sys_config = Sys_conf.objects
	sys_config_data = []
	for i in sys_config:
		data = [i.systemname,i.systemip,i.systemgroup,i.activation,i.scantype,i.frequency]
		sys_config_data.append(data)
	return sys_config_data

def get_not_config():
	not_config = Notif_conf.objects
	not_config_data = []
	for i in not_config:
		data = [i.nactivate,i.channel,i.botname,i.token_id]
		not_config_data.append(data)
	return not_config_data

def get_alarms_data():
	alerts = Alarms.objects
	alertsdata = []
	for i in alerts:
		cve_list = []
		for k,v in i.cve_list.items():
			cve_list.append([k,v])
		alarmtime = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(int(i['creationDate'])))
		data = [i.ip,alarmtime,cve_list[0][0],cve_list[0][1],i.package_name,i.package_version]
		alertsdata.append(data)
	return alertsdata


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")