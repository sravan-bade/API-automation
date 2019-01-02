import requests
import json
import requests.auth
from requests_oauthlib import OAuth1
from requests_hawk import HawkAuth

import logging

global app_host_url
app_host_url=''

logger = logging.getLogger("Test Run")


class RestClient(object):

    def post(self, url, body, headers=None):
        resp = requests.post(url, body, headers=headers, verify=False)
        try:
            output = json.loads(resp.text)
            #resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def put(self, url, body, headers=None):
        resp = requests.put(url, body, headers=headers, verify=False)
        try:
            output = json.loads(resp.text)
            #resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def patch(self, url, body, headers=None):
        resp = requests.patch(url, data=body, headers=headers, verify=False)
        try:
            output = json.loads(resp.text)
            #resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def get(self, url, headers=None):
        resp = requests.get(url, headers=headers, verify=False)
        try:
            output = json.loads(resp.text)
            #resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def getContent(self, url, headers=None):
        resp = requests.get(url, headers=headers, verify=False)
        type(resp)
        type(resp.content)
        try:
            output = resp.content
            #resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def get_with_auth(self, url, username, password, headers=None):
        resp = requests.get(url, auth=(username, password), headers=headers, verify=False)
        try:
            output = json.loads(resp.text)
            #resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def get_with_digest_auth(self, url, username, password, headers=None):
        resp = requests.get(url, auth=HTTPDigestAuth(username, password), headers=headers, verify=False)
        try:
            output = json.loads(resp.text)
            #resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def get_with_oauth1(self, url, client_key, client_secret, signature_method, headers=None):
        auth = OAuth1(client_key, client_secret, signature_method=signature_method)
        resp = requests.get(url, auth=auth, headers=headers, verify=False)
        try:
            output = json.loads(resp.text)
            #resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def get_with_hawk(self, url, hawk_id, hawk_key, headers=None):
        auth = HawkAuth(id=hawk_id, key=hawk_key)
        resp = requests.get(url, auth=auth, headers=headers, verify=False)
        try:
            output = json.loads(resp.text)
            #resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def delete(self, url, headers=None):
        resp = requests.delete(url, headers=headers, verify=False)
        #return resp.status_code
        try:
            output = json.loads(resp.text)
            #resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def deletetag(self, url, body, headers=None):
        resp = requests.delete(url, data=body, headers=headers, verify=False)
        try:
            output = json.loads(resp.text)
            # resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None


class BotClient(RestClient):

    def __init__(self):
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json' }

    def post_result_to_slack(self, status, channel,text_message, hosturl, build_version, execution_time):
        url = 'https://hooks.slack.com/services/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'

        text = text_message + "URL: " + hosturl + " Build Version: " + build_version + "\n"

        for key in sorted(status):
            if status[key][1] == True:
                text = text + status[key][0] + " : Passed\n"
            else:
                text = text + status[key][0] + " : *Failed*\n"
        print(text)

        # Request methods TC's
        textrm = ''
        testrmp = 0
        testrmf = 0
        for key in sorted(status):
            if 'Request_methods' in status[key][0]:
                if status[key][1] == True:
                    textrm = textrm + status[key][0] + " : Passed\n"
                    testrmp = testrmp + 1
                else:
                    textrm = textrm + status[key][0] + " : *Failed*\n"
                    testrmf = testrmf + 1

        # Auth TC's
        texth = ''
        testhp = 0
        testhf = 0
        for key in sorted(status):
            if 'Authorised' in status[key][0]:
                if status[key][1] == True:
                    texth = texth + status[key][0] + " : Passed\n"
                    testhp = testhp + 1
                else:
                    texth = texth + status[key][0] + " : *Failed*\n"
                    testhf = testhf + 1
        #print execution_time
        logger.info(text)

        TotalFailed = testrmf+testhf
        TestStatus = "\n" + "*Test Execution Summary*\n" + "Total Tests: "+str(testrmf+testrmp+testhf+testhp)+"; Passed: "\
                     +str(testrmp+testhp)+"; Failed: "\
                     +str(testrmf+testhf) +"\n" + execution_time
        TestStatus1 = "\n" +  "Total Tests: "+str(testrmf+testrmp+testhf+testhp)+"; Passed: "\
                     +str(testrmp+testhp)+"; Failed: "\
                     +str(testrmf+testhf) +"\n" + execution_time
        OpenDefects = ""
        #OpenDefects = "\n" + "*Open Defects : -\n"
        print(TestStatus)
        logger.info(TestStatus)
        Test_Results = text+ TestStatus
        Test_Results_file = open("Test_Results.txt","w")
        Test_Results_file.write(Test_Results)
        Test_Results_file.close()

        #body = {"channel": channel, "username": "CBSCAMBot", "text": text + TestStatus + OpenDefects, "icon_emoji": ":mega:"}
        body = {
            "channel": channel,
            "username": "APIBot",
            "attachments": [
                {
                    "color": "#080888",
                    "title": "Request methods API's",
                    #"text": testrmp,
                    "fields": [
                        {
                            "title": "Request methods Execution Summary",
                            "value": "Total Tests: " + str(testrmp + testrmf) + ";Passed: " + str(
                                testrmp) + ";Failed: " + str(testrmf)
                        }
                    ]
                },
                {
                    "color": "#800000",
                    "title": "Auth API's",
                    #"text": texth,
                    "fields": [
                        {
                            "title": "Auth Execution Summary",
                            "value": "Total Tests: " + str(testhp + testhf) + ";Passed: " + str(
                                testhp) + ";Failed: " + str(testhf)
                        },
                    ]
                },
                {
                    "color": "#C1FF33",
                    "title": "Test Status\n",
                    "fields": [
                        {
                            "title": "Overall Execution Summary",
                            "value": TestStatus1+"\n"+OpenDefects
                        },
                    ]
                },
                {
                    "color": "#3FFF33",
                    "fallback": "",
                    "actions": [
                        {
                            "type": "button",
                            "text": "GitHub",
                            "url": "https://github.com/sravan-bade/API-automation",
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "text": "Travis",
                            "url": "https://travis-ci.org/sravan-bade/API-automation",
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "text": "TestRail",
                            "url": "https://sravanbade.testrail.io/index.php?/runs/view/2",
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "text": "Defects",
                            "url": "https://sravanbade.testrail.io/index.php?/runs/view/2",
                            "style": "danger"
                        }
                    ]
                }
            ]
       }
        print("Total TCs :"+str(testrmf+testrmp+testhf+testhp))
        resp, body = self.post(url, json.dumps(body), headers=self.headers)
        return resp, body

    def post_result_to_testrail(self, testStatus, runid, username, password):

        def __init__(self):
            self.headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

        # Test cases + Status in Test Result
        testresult={}
        count = 0
        for key, value in testStatus.items():
            # print value[0], value[1]
            tname = value[0]
            tstatus = value[1]
            testresult[tname] = tstatus
            # print tname
            count = count + 1
        print("Count of Test cases getting to testresult--------" + str(count))
        runid = str(runid)
        getTestsUrl = "https://sravanbade.testrail.io/index.php?/api/v2/get_tests/" + runid
        postTestUrl = "https://sravanbade.testrail.io/index.php?/api/v2/add_result_for_case/" + runid + "/"

        resp = requests.get(getTestsUrl, auth=(str(username), str(password)), headers=self.headers, verify=False)
        output = json.loads(resp.text)
        # print output
        print("Response Code-- " + str(resp))

        # TestRail Test case + ID
        testrail = {}
        for t in output:
            # print t["title"],t["case_id"]
            title = t["title"]
            caseid = t["case_id"]
            testrail[title] = caseid
        '''
        for key,val in testrail.items():
            print key,val
        '''
        count = 0
        for key, val in testresult.items():
            count = count + 1
            if val == True:
                body = '{"status_id":"1"}'
            else:
                body = '{"status_id":"5"}'

            try:
                caseid = testrail[key]
                postUrl = postTestUrl + str(caseid)
                resp = requests.post(postUrl, body, auth=(str(username), str(password)), headers=self.headers)
            except KeyError:
                print("Test case is not present in test rail: " + key)
        print("Count of Test cases posted to testrail--------" + str(count))


class APIClient(RestClient):

    def __init__(self, hosturl, username, apikey):
        #super(APIClient, self).__init__(output)
        global app_host_url
        app_host_url = hosturl
        self.endpoint = hosturl
        self.headers_urlencoded = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

# All Unique API's here

#**********************************************************************************************************************
#*****************             Postman Sample Requests             ************************
#**********************************************************************************************************************
    def post_raw_data(self, body):
        url = '%s/post' % (self.endpoint)
        print("Rest URL: "+url)
        logger.info("Rest URL:"+url)
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def post_urlencoded_data(self, body):
        url = '%s/post' % (self.endpoint)
        print("Rest URL: "+url)
        logger.info("Rest URL:"+url)
        status, resp = self.post(url, body, headers=self.headers_urlencoded)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_data(self):
        url = '%s/get?test=123' % (self.endpoint)
        print("Rest URL: "+url)
        logger.info("Rest URL:"+url)
        resp,body = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return resp,body

    def put_data(self, body):
        url = '%s/put' % (self.endpoint)
        print("Rest URL: "+url)
        logger.info("Rest URL:"+url)
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def patch_data(self, body):
        url = '%s/put' % (self.endpoint)
        print("Rest URL: "+url)
        logger.info("Rest URL:"+url)
        status, resp = self.patch(url, json.dumps(body), headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def delete_with_body(self, body):
        url = '%s/delete' % (self.endpoint)
        print("Rest URL: "+url)
        logger.info("Rest URL:"+url)
        status, resp = self.deletetag(url, body, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

#**********************************************************************************************************************
#*****************             Postman Auth Requests             ************************
#**********************************************************************************************************************
    def get_digest_auth(self, username, password):
        url = '%s/digest-auth' % (self.endpoint)
        print("Rest URL: "+url)
        logger.info("Rest URL:"+url)
        status, resp = self.get_with_digest_auth(url, username, password, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_basic_auth(self, username, password):
        url = '%s/basic-auth' % (self.endpoint)
        print("Rest URL: "+url)
        logger.info("Rest URL:"+url)
        status, resp = self.get_with_auth(url, username, password, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_oauth1(self, client_key, client_secret, signature_method):
        url = '%s/oauth1' % (self.endpoint)
        print("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get_with_oauth1(url, client_key, client_secret, signature_method, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_hawk_auth(self, hawk_id, hawk_key):
        url = '%s/auth/hawk' % (self.endpoint)
        print("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get_with_hawk(url, hawk_id, hawk_key, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp
