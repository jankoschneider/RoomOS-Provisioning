import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass
import csv
import os
from multiprocessing.pool import ThreadPool
from itertools import repeat


def get_credentials():
    ''' Prompts and return a username and password.'''
    username = input('Enter Username: ')
    password = None
    while not password:
        password = getpass()
        password_verify = getpass('Retype your password: ')
        if password != password_verify:
            print('Passwords do not match. Try again')
            password = None
    return username, password
    

def get_codec_ips():
    rows = []
    try:
        with open('vc-systems.csv', 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            # extracting field names through first row
            fields = next(csvreader)  # python3
            # extracting each data row one by one
            for row in csvreader:
                rows.append(row)
            # get total number of rows
            print("Total no. of rows: %d" % (csvreader.line_num-1))
    except FileNotFoundError:
        print(filename + " Input file not found in current directory")

    fieldindex = fields.index('IP Address')
    codec_ips = []
    for row in rows:
        codec_ips.append(row[fieldindex])
    
    return codec_ips


def do_upload(ip,username,password):
    for xml_file in os.listdir("xml"):
        if xml_file.endswith(".xml"):
            xml_content = open('xml/' + xml_file, "r").read()
            url = "https://{}/putxml".format(ip)
            headers={'content-type': 'text/xml; charset=UTF-8'}
            response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers, data=xml_content, verify=False)
            output = '-'*40+"\n"
            output += 'Sent XML-File {} to {}\n'.format(xml_file,ip)
            output += 'Status code: {}\n'.format(response.status_code)
            output += 'Response: {}'.format(response.text)
            print(output)


def main():
    requests.packages.urllib3.disable_warnings()
    codec_ips = get_codec_ips()
    print("Codec IPs are {}".format(codec_ips))
    print("")
    username, password = get_credentials()
    # Threading to speed things up:
    with ThreadPool(10) as pool:
        pool.starmap(do_upload, zip(codec_ips, repeat(username), repeat(password)))

if __name__ == "__main__":
    main()