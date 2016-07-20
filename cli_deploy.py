#!/usr/bin/env python

# Eric Chou ericc@a10networks.com

import requests, json
#from json_config import hostname

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


clideploy_path = "/axapi/v3/clideploy/"
url = base_url + clideploy_path
clideploy_payload = {
    "commandList":["router bgp 64513", "no network 14.14.14.14/32", "end"]
}

r = requests.post(url, data=json.dumps(clideploy_payload), headers=common_headers, verify=False)
print(r.content)


# Commit changes
hostname_endpoint = '/axapi/v3/write/memory'
url = base_url + hostname_endpoint
print("write mem")
r = requests.post(url, headers=common_headers, verify=False)
print(r.content)

# Log off
logoff_endpoing = '/axapi/v3/logoff'
url = base_url + logoff_endpoing
print("Log off")
r = requests.post(url, headers=common_headers, verify=False)


