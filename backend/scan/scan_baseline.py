import os, sys
import time
import json
import configparser
import datetime

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from functions import *


config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(dir_path+'/../config.ini')

# Mongo
mongodb =           config['db']['mongodb']
mongoport =         int(config['db']['mongoport'])
cve_collection =    config['db']['cve_collection']
mongo_database =    config['db']['mongodatabase']
cpe_collection =    config['db']['cpe_collection']
baseline_coll =     config['db']['baseline']
alarms_collection = config['db']['alarms_collection']


class System_Baseline:
    
    def __init__(self):
        return None
    
    def load(self,baseline):
        for k,v in baseline.items():
            setattr(self,k,v)
        
    def search_for_cve(self):
        if len(self.packages)>0:
            for package in self.packages:
                self.check_package(package['name'], package['version'])
                
    def check_package(self, package_name, package_version):
                
        ####################################################################################################
        cpe = f"cpe:2.3:a:pandorafms:{package_name}:{package_version}:*:*:*:*:*:*:*"
        ####################################################################################################
        cpe_details = read_from_mongo(cpe_collection, {'cpe_value':cpe})
        if len(cpe_details) > 0:
            cve_list = cpe_details[0]['cve']
            self.issue_alarm(package_name, package_version,cve_list)
        else:
            return False

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
        return save_to_mongo(alarms_collection, alarm)

        
# general Operations
def get_severity(cve):
    try:
        cve_details = read_from_mongo(cve_collection, {'id':cve})
        if len(cve_details) > 0:
            severity = cve_details[0]['cvssV3']['baseSeverity']
            return severity
    except Exception as e:
        print(e)


if __name__ == "__main__":
    server_baseline = {
    'name': 'server.test3',
    'ip': '192.168.0.201',
    'os_release': 'CentoS',
    'addedTime':1605368029,
    'modifiedTime':1605368029,
    'packages': [
        {'name':'package1','version':'1.5.4'},
        {'name':'pandor_fms','version':'7.44'},
        {'name':'package5','version':'4.5.4'},
        
        ],
    'updated':False,
    'comment':'',
    'internalNmap':[],
    'externalNmap':[]
    }


    server1 = System_Baseline()
    server1.load(server_baseline)
    server1.search_for_cve()