from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import wget
import os
from zipfile import ZipFile
import configparser
import datetime
import time

config = configparser.ConfigParser()
config.read('../config.ini')

# URL
url = config['nvd']['url']
files_url = config['nvd']['files_url']

dir_path = os.getcwd()

# log function
def log(log_message):
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(f'{dir_path}/nvdcve_getfiles.log', 'a') as fp:
        fp.write(current_time+"  "+log_message+'\n')

# Change working directory
os.chdir(dir_path+'/files')
nvdcve_files_dir = os.getcwd()
all_files = os.listdir(nvdcve_files_dir)

json_files = [f for f in all_files if f[:10] == 'nvdcve-1.1' and f[-4:] == 'json']
zip_files = [f for f in all_files if f[:10] == 'nvdcve-1.1' and f[-3:] == 'zip']
list(map(os.remove, json_files)) # remove previous json files
list(map(os.remove, zip_files)) # remove previous zip files if any


log('Beginning file download')
html_page = urllib2.urlopen(files_url)
soup = BeautifulSoup(html_page, 'html.parser')
for link in soup.findAll('a', attrs={'href': re.compile("nvdcve-1.1.*zip")}): # save NVDCVE files
    wget.download(url+link.get('href'))

log('Completed files download')

# Get list of zip files
all_files = os.listdir(nvdcve_files_dir)
zip_files = [f for f in all_files if f[:10] == 'nvdcve-1.1' and f[-3:] == 'zip']

log(f'{len(zip_files)} files were downloaded')

for zf in zip_files: # extract and delete zip files
    with ZipFile(zf, 'r') as zipObj:
        zipObj.extractall()
    os.remove(zf)
