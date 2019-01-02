from utils import assignOrder
from utils import assertEqual
import logging
import configparser
import json
import os

global status
status = {}
logger = logging.getLogger("Test Run")
config = configparser.ConfigParser()
config.read('settings.conf')
ResponseTime = config.get('params', 'response_time')

DOWNLOAD_LOCATION_PATH = os.getcwd() + "/"
if not os.path.exists(DOWNLOAD_LOCATION_PATH):
    print("Making download directory")
    os.mkdir(DOWNLOAD_LOCATION_PATH)

global Testdata1

number = '0123456789'
alpha = 'abcdefghijklmnopqrstuvwxyz'


class requestmethods_APITest(object):
    def __init__(self, client):
        self.test_client = client

    @assignOrder(0)
    def Request_methods_test_data(self):
        passed = False
        global Testdata1
        with open('testdata.json', 'r') as f:
            data = json.load(f)

        Testdata1 = data["Scenario1"][0]["Testdata1"]
        print("Request methods Test Data\n" + "Test Data 1 :" + Testdata1 + "\n")
        print(Testdata1)
        if (Testdata1 is None):
            passed = False
        else:
            passed = True
        return passed

    @assignOrder(50)
    def Request_methods_get_request(self):
        passed = False
        resp, body = self.test_client.get_data()
        print(resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if passOfResponseCode:
            passed = True
        status['Requestmethods-APITest'] = passed
        return passed

    @assignOrder(51)
    def Request_methods_post_raw_data(self):
        passed = False
        body = "Duis posuere augue vel cursus pharetra. In luctus a ex nec pretium. Praesent neque quam, tincidunt"

        resp, body = self.test_client.post_raw_data(body)
        print(resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if passOfResponseCode:
            passed = True
        status['Requestmethods-APITest'] = passed
        return passed

    @assignOrder(52)
    def Request_methods_post_url_encoded(self):
        passed = False
        body = {
            "strange": "boom"
        }

        resp, body = self.test_client.post_urlencoded_data(body)
        print(resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if passOfResponseCode:
            passed = True
        status['Requestmethods-APITest'] = passed
        return passed

    @assignOrder(53)
    def Request_methods_put_data(self):
        passed = False
        body = "Test"

        resp, body = self.test_client.put_data(body)
        print(resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if passOfResponseCode:
            passed = True
        status['Requestmethods-APITest'] = passed
        return passed


    @assignOrder(54)
    def Request_methods_patch_data(self):
        passed = False
        body = "Test"

        resp, body = self.test_client.patch_data(body)
        print(resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if passOfResponseCode:
            passed = True
        status['Requestmethods-APITest'] = passed
        return passed


    @assignOrder(55)
    def Request_methods_delete_data(self):
        passed = False
        body = "Test"

        resp, body = self.test_client.delete_with_body(body)
        print(resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if passOfResponseCode:
            passed = True
        status['Requestmethods-APITest'] = passed
        return passed
