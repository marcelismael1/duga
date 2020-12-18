import os, sys
import time
import json
import configparser
import datetime
import slack

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from functions import *


config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(dir_path+'/../../config.ini')

# Mongo
mongodb =           config['db']['mongodb']
mongoport =         int(config['db']['mongoport'])
cve_collection =    config['db']['cve_collection']
mongo_database =    config['db']['mongodatabase']
cpe_collection =    config['db']['cpe_collection']
baseline_coll =     config['db']['baseline']
alarms_collection = config['db']['alarms_collection']

# Slack config
slack_bot_token = 	config['slack']['token']
to_channel = 		config['slack']['channel']
bot_name =          config['slack']['bot_name']

sc = slack.WebClient(token=slack_bot_token)

#############################        
### System Baseline Class ###
#############################
class System_Baseline:
    
    def __init__(self):
        return None
    
    # Load the baseline
    def load(self,baseline):
        try:
            baseline_keys = ['name', 'ip', 'os_release', 'addedTime', 'modifiedTime', 'packages', 'updated', 'comment', 'internalNmap', 'externalNmap']
            if len(set(baseline_keys) - set(baseline.keys())) == 0:
                for k,v in baseline.items():
                    setattr(self,k,v)
        except Exception as e:
            print(e)
    
    # search for cve from the package list of the baseline
    def search_for_cve(self):
        if len(self.packages)>0:
            for package in self.packages:
                self.check_package(package['name'], package['version'])

    # check if a cetain package has Vulnrabilites            
    def check_package(self, package_name, package_version):
                
        ####################################################################################################
        cpe = f"cpe:2.3:a:mariadb:{package_name}:*:*:*:*:*:*:*:*"
        ####################################################################################################
        cpe_details = read_from_mongo(cpe_collection, {'cpe_value':cpe})
        if len(cpe_details) > 0:
            cve_list = cpe_details[0]['cve']
            self.issue_alarm(package_name, package_version,cve_list)
        else:
            return False

    # issue an alarm
    def issue_alarm(self, package_name, package_version, cve_list):
        cve_list_with_severity = {}
        for cve in cve_list:
            cve_list_with_severity[cve] = get_severity(cve)        
        alarm = {
            'ip': self.ip,
            'name': self.name,
            'resolved': False,
            'creationDate':int(time.time()),
            'package_name' : package_name,
            'package_version': package_version,
            'cve_list': cve_list_with_severity
        }

        m1 = f":warning: System _*{alarm['ip']}*_ has vulnerable package:\n*Package Name* : {alarm['package_name']}\n*Package Version* : {alarm['package_version']}\n*CVE List* :\n"
        m2 = ''
        count = 0
        for k,v in alarm['cve_list'].items():
            if v == 'LOW':
                m2 += f'• {k} severity is {v}\n'
            elif v == 'MEDIUM':
                 m2 += f'• {k} severity is {v}\n'
            elif v == 'HIGH':
                 m2 += f'• {k} severity is {v} :exclamation:\n'
            elif v == 'CRITICAL':
                 m2 += f'• {k} severity is {v} :no_entry_sign:\n'
            
            count += 1
            if count >= 5:
                m2 += f'.... Others (total CVEs are {len(alarm.keys())})'
                break
        message = m1 + m2
        notify(message)

        return save_to_mongo(alarms_collection, alarm)



##########################        
### general Operations ###
##########################

# get the severity of a certain cve
def get_severity(cve):
    try:
        cve_details = read_from_mongo(cve_collection, {'id':cve})
        if len(cve_details) > 0:
            severity = cve_details[0]['cvssV3']['baseSeverity']
            return severity
    except Exception as e:
        print(e)

def notify(message):
    try:
        sc.chat_postMessage(channel= to_channel,text=message, username=bot_name)
    except Exception as e:
        print(e)
    return None

if __name__ == "__main__":
        baseline_list =  read_from_mongo(baseline_coll, {})
        if len(baseline_list) > 0:
            for baseline in baseline_list:    
                server = System_Baseline()
                server.load(baseline)
                server.search_for_cve()
                del server