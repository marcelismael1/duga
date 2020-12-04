from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import requests
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from functions import *

class TestFlask(unittest.TestCase):

    def test_web_app_running(self):
        try:
             r = requests.get("http://127.0.0.1:5000/")
        except:
            self.fail("Main Page.Test Failed")


    def test_web_alerts_running(self):
        try:
             r = requests.get("http://127.0.0.1:5000/alerts")
        except:
            self.fail("Alerts Page.Test Failed")


    def test_web_configuration_running(self):
        try:
             r = requests.get("http://127.0.0.1:5000/configurations")
        except:
            self.fail("Configurations Page.Test Failed")




    def test_web_about_running(self):
        try:
             r = requests.get("http://127.0.0.1:5000/about")
        except:
            self.fail("About Page.Test Failed")


    def test_alerts_page(self):

        r = requests.get("http://127.0.0.1:5000/alerts")
        page_src = r.text

        if page_src.find("AFFECTED PACKAGES") < 0:
            self.fail("Can't find AFFECTED PACKAGES columns")

    def test_alerts_page_severty(self):

        r = requests.get("http://127.0.0.1:5000/alerts")
        page_src = r.text

        if page_src.find("SEVERITY") < 0:
            self.fail("Can't find SEVERITY columns")

    def test_alerts_page_date(self):

        r = requests.get("http://127.0.0.1:5000/alerts")
        page_src = r.text

        if page_src.find("DATE") < 0:
            self.fail("Can't find DATE columns")

    def test_sys_config_form(self):
    	form_data = {"systemip": "1.1.1.1","systemname": "test_ip1","systemgroup": "Test1","activation": "ON","scantype": "Full","frequency": "Weekly"}
    	r = requests.post("http://127.0.0.1:5000/sys_config_table/new", data = form_data)
    	if r.status_code != 200:
            self.fail(" failed to post sysconfig")
    	r = requests.get("http://127.0.0.1:5000/configurations")
    	page_src = r.text
    	if page_src.find("<td>1.1.1.1</td>") < 0:
            self.fail(" failed to post sysconfig")
    	delete_from_mongo('configurations', {"systemip": "1.1.1.1"})

    





if __name__ == "__main__":
    unittest.main(warnings='ignore', failfast = True)