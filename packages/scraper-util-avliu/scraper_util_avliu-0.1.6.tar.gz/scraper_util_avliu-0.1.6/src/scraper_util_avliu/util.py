import json
import os
import re
import time

from selenium import webdriver
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.error

import mysql.connector

import boto3
import datetime


def get_selenium_driver(undetected=False):
    # adblock_filepath = '../lib/adblock.crx'

    if undetected:

        # The below code is extremely hacky, but accomplishes a few things:
        # (1) Makes default headless/executable to be the one we need in cloud
        # (2) Allows us to specify other options locally via env vars for testing
        # (3) Maintains everything in detected chromedriver because it doesn't need edecutable

        # Goal is to set custom env variable only if we're running locally
        headless = os.environ.get('HEADLESS')
        if not headless:
            headless = 'True'
        headless = False if headless == 'False' else True

        driver_executable_path = os.environ.get('DRIVER_EXECUTABLE_PATH')
        if not driver_executable_path:
            driver_executable_path = '/usr/bin/chromedriver'
        print(f'headless={headless}, path={driver_executable_path}')
        # See if we actually need this in cloud
        # use_subprocess = True

        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--mute-audio')
        # chrome_options.add_extension(adblock_filepath)
        driver = uc.Chrome(options=chrome_options,
                           headless=headless,
                           driver_executable_path=driver_executable_path)

    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--mute-audio')
        # chrome_options.add_extension(adblock_filepath)
        driver = webdriver.Chrome(options=chrome_options)

    return driver


def get_soup(url_or_driver):
    if type(url_or_driver) == uc.Chrome or type(url_or_driver) == webdriver.Chrome:
        return BeautifulSoup(url_or_driver.page_source, "html.parser")

    success = False
    sleep_time = 1
    max_sleep_time = 60 * 5

    req, html_page = None, None
    while not success:
        try:
            req = Request(url_or_driver)
            html_page = urlopen(req)
            success = True
        except urllib.error.HTTPError as e:
            print(f'error {e.code}')
            if 500 <= e.code <= 599 and sleep_time < max_sleep_time:
                print(f'server error; sleep {sleep_time} seconds')
                time.sleep(sleep_time)
                sleep_time *= 2
            else:
                raise e

    soup = BeautifulSoup(html_page, 'html.parser')
    return soup


# Get all the text within elements found using search_str
def get_soup_text(soup: BeautifulSoup, search_str: str, one=False):
    if one:
        return format_str(soup.select_one(search_str).text)
    else:
        return list(map(lambda x: format_str(x.text), soup.select(search_str)))


def append_to_json(json_file, new_data):
    if os.path.isfile(json_file):
        with open(json_file, 'r') as fp:
            all_data = json.load(fp)
    else:
        all_data = []

    all_data.append(new_data)

    with open(json_file, 'w') as fp:
        json.dump(all_data, fp, indent=4, separators=(',', ': '))


def append_to_file(file_name, new_data):
    with open(file_name, 'a') as f:
        for data in new_data:
            f.write(f'{data}\n')


def find_in_dict(my_dict: dict, key: str):
    # print(f'keys considered: {list(my_dict.keys())}')
    if key in my_dict.keys():
        return my_dict[key]
    ans = False
    for v in my_dict.values():
        if type(v) == dict:
            temp = find_in_dict(v, key)
            if temp != False:
                ans = temp
    return ans


# Replace newlines/tabs with the symbol |
def format_str(s):
    return re.sub("[\n\t\r]+", '|', s)


# Remove unnecessary symbols from a string
def remove_symbols_str(s):
    return re.sub("[|+:,.]", '', s)


def write_to_rds():
    # Make a mysql connection and create a table if it exists
    table_name = 'ebay_ev_sales'
    mydb = mysql.connector.connect(
        host="database-1.cchq0zbz9fej.us-east-1.rds.amazonaws.com",
        user="admin",
        password="12345678",
        database="ev-database-test"
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} "
        f"("
        f"vin VARCHAR(255), "
        f"date_accessed date, "
        f"make VARCHAR(255), "
        f"model VARCHAR(255), "
        f"price VARCHAR(255), "
        f"location VARCHAR(255), "
        f"fuel VARCHAR(255),"
        f"ebay_item_id VARCHAR(255),"
        f"PRIMARY KEY (vin, date_accessed)"
        f")"
    )


def get_log_time():
    dt = datetime.datetime.now()
    epoch = datetime.datetime.utcfromtimestamp(0)
    time = int((dt - epoch).total_seconds() * 1000.0)
    return time


def write_cloudwatch_log(log_group, log_stream, message):
    client = boto3.client('logs')
    response = client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[
            {
                'timestamp': get_log_time(),
                'message': message
            },
        ]
    )
    print(f'response: {response}')


def write_to_bucket(aws_bucket, source, dest):
    # Make sure to configure ~/.aws/configure file
    s3 = boto3.resource('s3')
    s3.Bucket(aws_bucket).upload_file(source, dest)


def main():
    bucket = 'test-youtube-audit-bucket'
    f = open("test_result_file.txt", "a")
    f.write("File content!")
    f.close()
    destination = 'test_folder/test_results_file.txt'

    write_to_bucket(bucket, "./test_result_file.txt", destination)


if __name__ == '__main__':
    main()
