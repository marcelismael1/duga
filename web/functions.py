import datetime, os
import time
import configparser
from pymongo import MongoClient

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(dir_path+'/../config.ini')

# Mongo
mongodb = config['db']['mongodb']
mongoport = int(config['db']['mongoport'])
cve_collection = config['db']['cve_collection']
mongo_database = config['db']['mongodatabase']

def save_to_mongo(collection, data, db_server = mongodb, port = mongoport, db_name = mongo_database):
    mongoclient = MongoClient(db_server,port)
    db = mongoclient[db_name]
    coll = db[collection]
    try:
        if type(data) == type([]):
            result = coll.insert_many(data)
            return result.inserted_ids
        elif type(data) == type({}):
            result = coll.insert_one(data)
            return result.inserted_id
        else:
            return False
    except Exception as e:
        if str(e) != 'documents must be a non-empty list':
            print('<mongosave> ',e)
            log('<mongosave> '+str(e))
        return False
#  save_to_mongo('collection', {'id':'myid'})

def replace_in_mongo(collection,find, data, db_server = mongodb, port = mongoport, db_name = mongo_database):
    mongoclient = MongoClient(db_server,port)
    db = mongoclient[db_name]
    coll = db[collection]
    try:
        replaced = coll.replace_one(find,data)
        return replaced.matched_count, replaced.modified_count
    except Exception as e:
        print('<mongoreplace> ',e)
        log('<mongoreplace> '+str(e))
        return False
# replace_in_mongo('collection', {'id':'myid'}, {'id':'myid22'})

def read_from_mongo(collection, find = None, db_server = mongodb, port = mongoport, db_name = mongo_database):
    mongoclient = MongoClient(db_server,port)
    db = mongoclient[db_name]
    coll = db[collection]
    return list(coll.find(find))
# read_from_mongo('collection', {'id':'myid'})

def delete_from_mongo(collection, find = None, db_server = mongodb, port = mongoport, db_name = mongo_database):
    mongoclient = MongoClient(db_server,port)
    db = mongoclient[db_name]
    coll = db[collection]
    try:
        deleted = coll.delete_many(find)
        return deleted.deleted_count
    except Exception as e:
        print('<mongodelete> ',e)
        log('<mongodelete> '+str(e))
        return False
    return False
# delete_from_mongo('collection', {'id':'myid'})

# log function
def log(log_message):
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    with open('ingest.log', 'a') as fp:
        fp.write(current_time+"  "+log_message+'\n')
#log("first log message")

def now_formatted():
    '''
    get time as below format
    08/23/2020, 17:32:26
    '''
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")
