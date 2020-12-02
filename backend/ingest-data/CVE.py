

class CVE:
    def __init__(self, cve_dict):
        #print('This is the class')
        self.cve_id= cve_dict['id']
        self.url=cve_dict['url']
        self.cpe=cve_dict['cpe']
        self.cvssV3=cve_dict['cvssV3']
        self.cvssV2=cve_dict['cvssV2']
        self.lastModifiedDate=cve_dict['lastModifiedDate']
        self.publishedDate=cve_dict['publishedDate']
