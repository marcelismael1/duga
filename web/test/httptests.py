from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import requests

class TestFlask(unittest.TestCase):

    def test_web_app_running(self):
        try:
             r = requests.get("http://127.0.0.1:5000/")
        except:
            self.fail("Test Failed")


    def test_alerts_page(self):

        r = requests.get("http://127.0.0.1:5000/alerts")
        page_src = r.text

        if page_src.find("AFFECTED PACKAGES") < 0:
            self.fail("Can't find most common languages")



if __name__ == "__main__":
    unittest.main(warnings='ignore', failfast = True)