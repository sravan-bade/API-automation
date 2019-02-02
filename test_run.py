import utils
import test_client
import tests.request_methods_tests
import tests.auth_tests
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import time
import sys
import requests
requests.packages.urllib3.disable_warnings()
import configparser


def run_api_tests():
    config = configparser.ConfigParser()
    config.read('settings.conf')

    logger = logging.getLogger("Test Run")
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler("test_run.log", when="m", interval=10, backupCount=2)
    logger.addHandler(handler)
    logger.info("-----------------------------------------------")
    logger.info("Test started: "+datetime.now().strftime('%Y-%m-%d-%H%M%S'))
    start_time = time.time()

    username = config.get('params', 'username')
    apikey = config.get('params', 'apikey')

    botclient = test_client.BotClient()

    if len(sys.argv) != 3:
        print("\nError : Required arguments missing!!\n")
        print("Usage : python3 test_run.py <env> <build_version/release_name>\n")
        print("ex : python3 test_run.py postman-echo.com release_name\n")
        exit(1)

    hosturl = "https://"+sys.argv[1]+""
    build_version = sys.argv[2]
    # build version is only using here for reference in slack
    client = test_client.APIClient(hosturl, username, apikey)
    # username and apikey are kept as additional parameters and will nowhere be used in our testing
    print("\nHost Name :"+sys.argv[1])
    print("Release :"+sys.argv[2])

    tname = config.get('params', 'test_case')
    requestmethods = config.get('tests', 'requestmethods')
    auth = config.get('tests', 'auth')

    # testcase = tname.split(",")
    func_stat = {}

    if (tname == 'all') and (requestmethods == 'true'):
        func_stat.update(utils.run_test_cases(tests.request_methods_tests.requestmethods_APITest(client)))

    if (tname == 'all') and (auth == 'true'):
        func_stat.update(utils.run_test_cases(tests.auth_tests.auth_APITest(client)))

    execution_time = "*Total Time Taken for Execution : %s seconds *" % (time.time() - start_time)

    logger.info("------------End of Tests------------")

    utils.get_error_logs_test_run()

    # Slack Integration
    run_test = config.get('params', 'post_to_bot')
    slack_result_channel = config.get('params', 'slack_result_channel')
    text = "*Sample APIs validation:*\n"
    if run_test == 'true':
        botclient.post_result_to_slack(func_stat, slack_result_channel, text, hosturl, build_version, execution_time)
    else:
        logger.info("Skipping posting the result to Slack!")

    # Testrail Integration
    # My TestRail got expired, so made the update status to false
    post_to_testrail = config.get('testrail', 'post_to_testrail')
    run_id = config.get('testrail', 'run_id')
    username = config.get('testrail', 'username')
    password = config.get('testrail', 'password')

    if post_to_testrail == 'true':
        print("TestRail Updating")
        botclient.post_result_to_testrail(func_stat, run_id, username, password)
    else:
        logger.info("Skipping posting the result to TestRail!")
    logger.info("------------End of TestRail Update------------")


if __name__ == '__main__':
    run_api_tests()
