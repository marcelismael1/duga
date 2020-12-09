from mongoengine import *
import datetime, os
import configparser
from bson.objectid import ObjectId


config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(dir_path+'/../config.ini')

# Mongo
mongodb = config['db']['mongodb']
mongoport = int(config['db']['mongoport'])
cve_collection = config['db']['cve_collection']
mongo_database = config['db']['mongodatabase']

connect(
    db=mongo_database,
    host=mongodb,
    port=mongoport
)

#Creating a collection and document schema

class Cve(Document):
    _id = ObjectIdField(default=ObjectId)
    id = StringField(required=True, unique=True)
    url = StringField()
    cvssV3 = DictField()
    cvssV2 = DictField()
    cpe = ListField()
    publishedDate = StringField()
    lastModifiedDate = StringField()

class Cpe(Document):
    cpe_value = StringField(required=True, unique=True)
    version = StringField()
    cve = ListField()
    publishedDate = IntField()
    lastModifiedDate = IntField()

class Alarms(Document):
    ip = StringField()
    name = StringField()
    resolved = BooleanField()
    creationDate = IntField()
    package_name = StringField()
    package_version = StringField()
    cve_list = DictField()

class Baseline(Document):
    name = StringField()
    ip = StringField(required=True, unique=True)
    os_release = StringField()
    addedTime = IntField()
    modifiedTime = IntField()
    packages = ListField()
    updated = BooleanField()
    comment = StringField()
    internalNmap = ListField()
    externalNmap = ListField()

class Notif_conf(Document):
    nactivate = StringField()
    channel = StringField()
    botname = StringField()
    token_id = StringField(required=True, unique=True)

class Sys_conf(Document):
    systemip = StringField(required=True, unique=True)
    systemname = StringField()
    systemgroup = StringField()
    activation = StringField()
    scantype = StringField()
    frequency = StringField()



# Save 

#config = Notif_conf(nactivate = req.get("nactivate"), channel= req.get("channel"), botname = req.get("botname") , token_id= req.get("token_id")).save()

# read data
# all data
#sys_config = Sys_conf.objects

# query search
#sys_config = Sys_conf.objects(id = 'XXXX')
#sys_config[0].systemip
