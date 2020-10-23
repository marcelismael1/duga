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

class CVE(Document)
    ID = StringField(required=True, unique=True)
    URL = StringField()
    CVSSV3 = StringField()
    CVSSV2 = StringField()
    CPE = ListField()
    PublishedDate = DateTimeField()
    LastModifiedDate = DateTimeField(default=datetime.utcnow)

class CPE(Document)
    CPE_Value = StringField(required=True, unique=True)
    Version = StringField()
    CVE = ListField()
    PublishedDate = DateTimeField()
    LastModifiedDate = DateTimeField(default=datetime.utcnow)

#Saving a document to the database
CVE_post = CVE(
    title=Saving CVE,
    content=First Saving command,
    date_published=datetime.utcnow(),
    author=Abdelrahim,
).save()

CPE_post = CPE(
    title=Saving CPE,
    content=First Saving command,
    date_published=datetime.utcnow(),
    author=Marcel,
).save()