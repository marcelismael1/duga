from mongoengine import 
import datetime

connect(
    db=Duga,
    username=root,
    password=,
    authentication_source=,
    host=localhost,
    port=27017
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