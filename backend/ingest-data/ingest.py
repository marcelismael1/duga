import json
import os, sys
#import cvss
#import cpe
import configparser
import datetime
import CVE
from pymongo import MongoClient


currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from functions import *
from mongodb_engine.py import *

config = configparser.ConfigParser()
config.read(currentdir+'/../../config.ini')

# Mongo
mongodb = config['db']['mongodb']
mongoport = int(config['db']['mongoport'])
cve_collection = config['db']['cve_collection']
mongo_database = config['db']['mongodatabase']

# nvd files dir
nvd_files_dir = f'{currentdir}/../get_files/files'

def load_cve_db(file_name):
    '''
    Loads nvdcve.json file, and then checks if the CVE is stored in DB, if not stores it.
    It also checks if the CVE was modified in the new version and if yes, it updates it
    notes: json files should be stored in files dir
    Example:
    load_cve_db('nvdcve-1.1-2020.json')
    '''
    with open(f'{nvd_files_dir}/{file_name}', 'r') as fp: # load json file
        data = json.load(fp)

    replaced = 0
    new_cves = []
    new_cpes = {}
    updated_cpes = 0
    try:
        # get a list of stored CVEs
        mongoclient = MongoClient(mongodb,mongoport) # Connect to mongo
        db = mongoclient[mongo_database]             # get database
        coll = db['cve']                             # get Collection
        stored_cve_list = list(coll.find({},{"id": 1,"lastModifiedDate": 1})) # get 2 columns from mongo
        # make the list as a dict
        stored_cve_dict = list_cve_to_dict(stored_cve_list)
        del stored_cve_list

        # get a list of stored CPES and assosiated CVEs
        coll = db['cpe']                             # get Collection
        stored_cpe_list = list(coll.find({},{"cpe_value": 1,"cve": 1})) # get 2 columns from mongo
        stored_cpe_dict = list_cpe_to_dict(stored_cpe_list)
        del stored_cpe_list

        for cve in data['CVE_Items']:
            if cve['cve']['CVE_data_meta']['ID'] not in list(stored_cve_dict.keys()):
                record = construct_cve(cve)
                if record:
                    new_cves.append(record)

            elif cve['lastModifiedDate'] > stored_cve_dict[cve['cve']['CVE_data_meta']['ID']]:
                record = construct_cve(cve)
                if record:
                    replace_in_mongo('cve', {'id':cve['cve']['CVE_data_meta']['ID']},record)
                    replaced += 1
            else:
                pass

            #--------------------#
            try: # save CPEs
                cve_name = cve['cve']['CVE_data_meta']['ID']
                cpes = get_cpes_from_nvdcve(cve)
                for cpe in cpes:
                    if cpe in list(stored_cpe_dict.keys()): # CPE is already saved in DB
                        if cve_name not in  stored_cpe_dict[cpe]:
                            stored_cpe_dict[cpe].append(cve_name)
                            save_cpe(cpe,cve_name) # update CPE with new CVE value
                            updated_cpes += 1

                    elif cpe in list(new_cpes.keys()):
                        if cve_name not in new_cpes[cpe]['cve']:
                            new_cpes[cpe]['cve'].append(cve_name)
                            new_cpes[cpe]['cve'] = list(set(new_cpes[cpe]['cve']))
                    else:
                        new_cpes[cpe] = construct_new_cpe(cpe,cve_name)

            except Exception as e:
                print('<load-cpe> ',e)
                log('<load-cpe> '+str(e))
            #--------------------#

    except Exception as e:
        print('<load> ',e)
        log('<load> '+str(e))

    saved_cves = save_to_mongo('cve',new_cves)
    saved_cpes = save_to_mongo('cpe',list(new_cpes.values()))

    del new_cves
    del new_cpes
    del stored_cpe_dict
    del stored_cve_dict
    del data

    if saved_cpes: saved_cpes = len(saved_cpes)
    else: saved_cpes = 0

    if saved_cves: saved_cves = len(saved_cves)
    else: saved_cves = 0

    return {'cves':(saved_cves, replaced), 'cpes':(saved_cpes, updated_cpes)}



def construct_cve(cve):
    '''
    Reconstructs the standard nvdcve form to a shorter version to be stored in the DB
    key values are:
    (id, url,cpe, cvssV3, cvssV2,lastModifiedDate, publishedDate)
    '''
    record = {}
    try:
        record['id'] = cve['cve']['CVE_data_meta']['ID']
        record['url'] = ''
        record['cpe'] = []
        record["cvssV3"] = {}
        record["cvssV2"] = {}

        try: # save url
            record['url'] = cve['cve']['references']["reference_data"][0]['url']
        except Exception as e:
            print('<url> ',e)

        try: # save cpe list
            record['cpe'] = cve['configurations']['nodes']
        except Exception as e:
            print('<cpe> ',e)
            log('<cpe> '+str(e))

        try: # save cvss (Common Vulnerability Scoring System)
            for metric in list(cve['impact'].keys()):
                if metric == "baseMetricV3":
                    record["cvssV3"] = {"version":cve['impact'][metric]["cvssV3"]['version'],\
                                        "vectorString":cve['impact'][metric]["cvssV3"]['vectorString'],\
                                        "baseScore":cve['impact'][metric]["cvssV3"]['baseScore'],\
                                        "exploitabilityScore":cve['impact'][metric]['exploitabilityScore'],\
                                        "impactScore":cve['impact'][metric]['impactScore'],\
                                        "baseSeverity":cve['impact'][metric]["cvssV3"]['baseSeverity']}

                elif metric == "baseMetricV2":
                    record["cvssV2"] = {"version":cve['impact'][metric]["cvssV2"]['version'],\
                                        "vectorString":cve['impact'][metric]["cvssV2"]['vectorString'],\
                                        "baseScore":cve['impact'][metric]["cvssV2"]['baseScore'],\
                                        "exploitabilityScore":cve['impact'][metric]['exploitabilityScore'],\
                                        "impactScore":cve['impact'][metric]['impactScore'],\
                                        "severity":cve['impact'][metric]['severity']}

        except Exception as e:
            print('<impact> ',e)
            log('<impact> '+str(e))

        record['lastModifiedDate'] = cve['lastModifiedDate']
        record['publishedDate'] = cve['publishedDate']

    except Exception as e:
        print('<general> ',e)
        log('<general> '+str(e))
    finally:
        if record != {}:
            return record
    return False


def list_cve_to_dict (cve_list):
    '''
    change list of cve entries to dictionary where CVE ID is the key and lastModifiedDate is the value
    Example:
    [{"id" : "CVE-0001", "lastModifiedDate" : "2020-01-14"}, {"id" : "CVE-0002", "lastModifiedDate" : "2020-01-15"}]
    becomes
    {"CVE-0001":"2020-01-14",
    "CVE-0002": "2020-01-15"}
    '''
    cve_dict = {}
    for cve in cve_list:
        cve_dict[cve['id']] = cve['lastModifiedDate']
    return cve_dict

def list_cpe_to_dict(cpe_list):
    '''
    change list of cpe entries to dictionary where cpe_value is the key and assosiated cve_list is the value
    '''
    cpe_dict = {}
    for cpe in cpe_list:
        cpe_dict[cpe['cpe_value']] = cpe['cve']
    return cpe_dict

def save_cpe(cpe_value, cve_name,version = '2.3'):
    '''
    This can save or modify a cpe record, if the cpe is new, it will save add a new record for it
    and if the cpe is existed check the cve list and update it if needed
    save_cpe("cpe:2.3:o:google:android:8.0:*:*:*:*:*:*:*",'2.3', "CVE-2020-0024")
    '''
    cpe = read_from_mongo('cpe', {'cpe_value':cpe_value})
    if cpe != []:
        cpe = cpe[0]
        if cve_name in cpe['cve']:
            return False
        cpe['cve'].append(cve_name)
        cpe['cve'] = list(set(cpe['cve']))
        cpe['lastModifiedDate']  = int(time.time())
        try:
            replace_in_mongo('cpe', {'cpe_value':cpe_value},cpe)
            return  cpe['cpe_value'],cpe['cve']
        except Exception as e:
            print('<sv-cpe> ',e)
            log('<sv-cpe> '+str(e))
            return False
    else:
        result = {}
        result['cpe_value'] = cpe_value
        result['version'] = version
        result['cve'] = [cve_name]
        result['publishedDate'] = int(time.time())
        result['lastModifiedDate'] = int(time.time())
        try:
            save_to_mongo('cpe',result)
            return result['cpe_value'],result['cve']
        except Exception as e:
            print('<sv-cpe> ',e)
            log('<sv-cpe> '+str(e))
            return False

def construct_new_cpe(cpe_value, cve,version = '2.3'):
    '''
    construct new cpe record
    EXAMPLE:
    {"cpe_value" : "cpe:2.3:h:intel:nuc_kit_nuc7i7dnhe:-:*:*:*:*:*:*:*",
    "version" : "2.3",
    "cve" : ["CVE-2020-0526",CVE-2020-0530"],
    "publishedDate" : 1598161157,
    "lastModifiedDate" : 1598161157}
    '''
    result = {}
    result['cpe_value'] = cpe_value
    result['version'] = version
    result['cve'] = [cve]
    result['publishedDate'] = int(time.time())
    result['lastModifiedDate'] = int(time.time())
    return result

def get_cpes_from_nvdcve(nvdcve):
    '''
    Take a NVDCVE input cve and extract the list of CPE entries assosiated with it
    '''
    cpe_list = []
    for node in nvdcve["configurations"]["nodes"]:
        if node['operator'] == 'AND':
            if "children" in list(node.keys()):
                for child in node["children"]:
                    if child['operator'] == 'OR':
                        for cpe in child["cpe_match"]:
                            cpe_list.append(cpe['cpe23Uri'])
                    else:
                        print('get_cpes_from_nvdcve - NEW CASE 1')

            elif "cpe_match" in list(node.keys()):
                for cpe in node["cpe_match"]:
                    cpe_list.append(cpe['cpe23Uri'])
            else:
                print('get_cpes_from_nvdcve - NEW CASE 2')

        elif node['operator'] == 'OR':
            for cpe in node["cpe_match"]:
                cpe_list.append(cpe['cpe23Uri'])
        else:
            print('get_cpes_from_nvdcve - NEW CASE 3')

    return set(cpe_list)

if __name__ == "__main__":
    list_of_files = os.listdir(nvd_files_dir)
    list_of_files_to_ingest = [f for f in list_of_files if f[:10] == 'nvdcve-1.1' and f[-4:] == 'json']

    log('NVDCVE files ingestion started')
    for nvdcve_file in list_of_files_to_ingest:
        loaded = load_cve_db(nvdcve_file)
        log(f"{nvdcve_file} was loaded as follows: {loaded}")
