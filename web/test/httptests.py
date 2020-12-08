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



# TEST ADDING SYSTEM CONFIGURATION
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

# TEST ADDING SYSTEM NOTIFICATIONS
    def test_sys_notif_form(self):
        form_data = {"nactivate": "On","channel": "1665165","botname": "Test1","token_id": "51616161"}
        r = requests.post("http://127.0.0.1:5000/not_config_table/new", data = form_data)
        if r.status_code != 200:
            self.fail(" failed to post notificationconfig")
        r = requests.get("http://127.0.0.1:5000/configurations")
        page_src = r.text
        if page_src.find("<td>51616161</td>") < 0:
            self.fail(" failed to post notificationconfig")
        delete_from_mongo('sys_notifications', {"token_id": "51616161"})


# TEST DELETING FROM SYSTEM NOTIFICATIONS
    def test_delete_sys_notif_form(self):
        form_data = {"nactivate": "On","channel": "D01BEB4JD2F","botname": "Test3","token_id": "xoxp-1400029591719"}
        r = requests.post("http://127.0.0.1:5000/not_config_table/new", data = form_data)
        token_data = {"token_id": "xoxp-1400029591719"}
        r = requests.get("http://127.0.0.1:5000/not_config_table/delete/xoxp-1400029591719")
        if r.status_code != 200:
            self.fail(" failed to post notificationconfig")
        r = requests.get("http://127.0.0.1:5000/configurations")
        page_src = r.text
        if page_src.find("<td>xoxp-1400029591719</td>") > 0:
            self.fail(" failed to delete notificationconfig")
        


# TEST DELETING FROM SYSTEM CONFIGURATIONS
    def test_delete_sys_config_form(self):
        form_data = {"systemip": "192.168.1.110","systemname": "test_ip10","systemgroup": "Test10","activation": "ON","scantype": "Full","frequency": "Weekly"}
        r = requests.post("http://127.0.0.1:5000/sys_config_table/new", data = form_data)
        r = requests.get("http://127.0.0.1:5000/sys_config_table/delete/192.168.1.110")
        if r.status_code != 200:
            self.fail(" failed to post sysconfig")
        r = requests.get("http://127.0.0.1:5000/configurations")
        page_src = r.text
        if page_src.find("<td>xoxp-1400029591719</td>") > 0:
            self.fail(" failed to delete sysconfig")


if __name__ == "__main__":
    unittest.main(warnings='ignore', failfast = True)