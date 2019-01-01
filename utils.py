import configparser as ConfigParser
import requests
import json
import time
import boto
#import paramiko
import select
#import yaml
import string
import random
import sys
import logging
import fnmatch
import os
import zipfile
import glob
import csv
import adal
from boto.exception import S3ResponseError
from requests.exceptions import ConnectionError, ChunkedEncodingError,ReadTimeout,ConnectTimeout

logger = logging.getLogger("Test Run")

DOWNLOAD_LOCATION_PATH = os.getcwd()+"/"
if not os.path.exists(DOWNLOAD_LOCATION_PATH):
	print ("Making download directory")
	os.mkdir(DOWNLOAD_LOCATION_PATH)


def unzipfiles(filePath):
    with zipfile.ZipFile(filePath,"r") as zip_ref:
        zip_ref.extractall(DOWNLOAD_LOCATION_PATH)


def get_error_logs_test_run():
    open('test_error.log', 'w').close()
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, 'test_run.log'):
            print(file)
            fpod = open(file, "r")
            lines = fpod.readlines()
            for i in range(0, len(lines)):
                if lines[i].__contains__(' Error'):
                    with open('test_error.log', 'a') as f:
                        # f.write(lines[i - 5])
                        f.write(lines[i - 4])
                        f.write(lines[i - 3])
                        f.write(lines[i - 2])
                        f.write(lines[i - 1])
                        f.write(lines[i])


def print_test_results(passed, test_name):
    if passed:
        print('**********************************')
        print('    %s TEST PASSED' % test_name)
        print('**********************************\n')
    else:
        print('**********************************')
        print('    %s TEST FAILED' % test_name)
        print('**********************************\n')


def assignOrder(order: object) -> object:
        """

        :rtype: object
        """
        def do_assignment(to_func):
            to_func.order = order
            return to_func
        return do_assignment


def run_test_cases(class_obj):
    config = ConfigParser.ConfigParser()
    config.read('settings.conf')
    global TotalTests
    global TotalPassed
    TotalTests = 0
    TotalPassed = 0

    functions = sorted(
        # get a list of fields that have the order set
        [
                getattr(class_obj, field) for field in dir(class_obj)
                if hasattr(getattr(class_obj, field), 'order')
        ],
        # sort them by their order
        key=(lambda field: field.order)
    )
    #print functions
    print("Running testcases of set " + class_obj.__class__.__name__ + " :")
    logger.info("Running testcases of set "+ class_obj.__class__.__name__ + " :")
    dict = {}
    dict2= {}



    #return dict2, dict
    for func in functions:
        # print TotalTests
        TotalTests = TotalTests + 1
        print("--------------------------------------")
        logger.info("--------------------------------------")
        status = func()
        # print "--------------------------------------"
        dict[time.time()] = [func.__name__, status]
        if status is True:
            print(func.__name__ + "............  OK")
            logger.info(func.__name__ + "............  OK")
            dict2[func.__name__] = [1, 1]
            TotalPassed = TotalPassed + 1
            print("--------------------------------------")
            logger.info("--------------------------------------")
            # print TotalPassed
        elif status is False:
            print(func.__name__ + "............  Error")
            logger.info(func.__name__ + "............  Error")
            dict2[func.__name__] = [1, 0]
            print("--------------------------------------")
            logger.info("--------------------------------------")
        else:
            print("Testcase did not return any status")
            logger.info("Testcase did not return any status")

    return dict


def assertEqual(a,b):
    if a == b:
        return True
    else:
        return False


def assertContains(a,b):
    # a: String
    # b: Substring
    if b in a:
        return True
    else:
        return False


def randomString(size=3, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def dbConnection(hostInstance,passwordDB,querySQL):
    mariadb_connection = mariadb.connect(host=hostInstance,user='cmuser', password=passwordDB, database='cam',port=3168)
    cursor = mariadb_connection.cursor()
    query = (querySQL)
    cursor.execute(query)
    resultSet=list(cursor.fetchall())
    print('resultSet--->', resultSet)
    mariadb_connection.close()
    return resultSet
