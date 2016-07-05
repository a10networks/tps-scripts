#!/usr/bin/env python

# This script was tested under 2.7.11 and 3.5.1
# Steps below are purposely sequential and repeated 
# for illustration purposes

import requests, json

# Basic infomation
host = '192.168.199.152'
base_url = 'https://'+host


# Acquire athorization token
auth_headers = {'content-type': 'application/json'}
auth_payload = {"credentials": {"username": "admin", "password": "a10"}}
auth_endpoint = '/axapi/v3/auth' 
url = base_url + auth_endpoint
r = requests.post(url, data=json.dumps(auth_payload), headers=auth_headers, verify=False)
signature =  r.json()['authresponse']['signature']
print("This is the signature token: " + signature)

# Headers beyond this point should include the authorization token
common_headers = {'Content-type' : 'application/json', 'Authorization' : 'A10 {}'.format(signature)}


# Simple GET 'show version' example
version_endpoint = '/axapi/v3/version/oper'
url = base_url + version_endpoint
r = requests.get(url, headers=common_headers, verify=False)
print(r.content)


# Simple POST example to change hostname
hostname_endpoint = '/axapi/v3/hostname'
url = base_url + hostname_endpoint
hostname_payload = {"hostname": {"value": "TH4435-new"}}
r = requests.post(url, data=json.dumps(hostname_payload), headers=common_headers, verify=False)
print(r.content)

# Commit changes
hostname_endpoint = '/axapi/v3/write/memory'
url = base_url + hostname_endpoint
r = requests.post(url, headers=common_headers, verify=False)
print(r.content)

# Log off
logoff_endpoing = '/axapi/v3/logoff'
url = base_url + logoff_endpoing
print("Log off")
r = requests.post(url, headers=common_headers, verify=False)


