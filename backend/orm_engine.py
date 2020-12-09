from mongoengine import *
import datetime
import configparser



config = configparser.ConfigParser()
config.read('config.ini')

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
    ip = StringField()
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
    token_id = StringField()

class Sys_conf(Document):
    systemip = StringField()
    systemname = StringField()
    systemgroup = StringField()
    activation = StringField()
    scantype = StringField()
    frequency = StringField()


#Saving a document to the database
