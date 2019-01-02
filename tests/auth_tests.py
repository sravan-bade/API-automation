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


class auth_APITest(object):
    def __init__(self, client):
        self.test_client = client

    @assignOrder(0)
    def auth_test_data(self):
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
    def UnAuthorised_digestauth_get_request(self):
        passed = False
        username = ""
        password = ""
        resp, body = self.test_client.get_basic_auth(username, password)
        print(resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if passOfResponseCode:
            passed = True
        status['auth-APITest'] = passed
        return passed

    @assignOrder(51)
    def Authorised_digestauth_get_request(self):
        passed = False
        username = "postman"
        password = "password"
        resp, body = self.test_client.get_basic_auth(username, password)
        print(resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if passOfResponseCode:
            passed = True
        status['auth-APITest'] = passed
        return passed

    @assignOrder(52)
    def Authorised_basicauth_get_request(self):
        passed = False
        username = "postman"
        password = "password"
        resp, body = self.test_client.get_basic_auth(username, password)
        print(resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if passOfResponseCode:
            passed = True
        status['auth-APITest'] = passed
        return passed

    @assignOrder(53)
    def Authorised_oauth1_get_request(self):
        passed = False
        client_key = "RKCGzna7bv9YD57c"
        client_secret = "D+EdQ-gs$-%@2Nu7"
        signature_method = "HMAC-SHA1"
        resp, body = self.test_client.get_oauth1(client_key, client_secret, signature_method)
        print(resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if passOfResponseCode:
            passed = True
        status['auth-APITest'] = passed
        return passed


    @assignOrder(54)
    def Authorised_hawkauth_get_request(self):
        passed = False
        hawk_id = "dh37fgj492je"
        hawk_key = "werxhqb98rpaxn39848xrunpaw3489ruxnpa98w4rxn"
        resp, body = self.test_client.get_hawk_auth(hawk_id, hawk_key)
        print(resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if passOfResponseCode:
            passed = True
        status['auth-APITest'] = passed
        return passed
