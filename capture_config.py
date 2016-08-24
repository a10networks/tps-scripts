#!/usr/bin/env python

# Eric Chou ericc@a10networks.com

"""

1. Configure caputre file onbox first

TH4435#confi t
TH4435(config)#capture-config TEST3
TH4435(config-capture-config)#?
  capture-limit  Method to end packet-capture
  clear          Clear or Reset Functions
  do             To run exec commands in config mode
  enable         Enable capture-config
  end            Exit from configure mode
  exit           Exit from configure mode or sub mode
  filter         Filter packets to save using Berkeley Packet Filter syntax
  length         Packet length Bytes to capture (Default 80)
  no             Negate a command or set its defaults
  show           Show Running System Information
  write          Write Configuration
TH4435(config-capture-config)#end
TH4435#

2. Use the script to enable / disable capture file

"""

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


clideploy_path = "/axapi/v3/capture-config/TEST3/"
url = base_url + clideploy_path
clideploy_payload = {
    "capture-config":{
        "name": "TEST3",
        "enable": "1"
    }
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


