#!/usr/bin/env python

# This script was tested under 2.7.6 and 3.4.3
# Steps below are purposely sequential and repeated
# for illustration purposes

import requests, json

# Basic infomation
host = '192.168.199.150'
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


# Simple GET 'show version'
version_endpoint = '/axapi/v3/version/oper'
url = base_url + version_endpoint
r = requests.get(url, headers=common_headers, verify=False)
print(r.content)


# POST to create zone
zone_endpoint = '/axapi/v3/ddos/dst/zone/'
url = base_url + zone_endpoint
zone_payload = {
      "zone-list": [
      {
      "zone-name":"partner_test",
      "ip": [
        {
          "ip-addr":"1.1.1.1",
        }
      ],
      "operational-mode":"monitor",
      "advertised-enable":0,
      "uuid":"12345"
      },
      ]
    }
r = requests.post(url, data=json.dumps(zone_payload), headers=common_headers, verify=False)
print(r.content)

# Update to modify existing zone
zone_endpoint = '/axapi/v3/ddos/dst/zone/'
url = base_url + zone_endpoint
zone_payload = {
      "zone-list": [
      {
      "zone-name":"partner_test",
      "ip": [
        {
          "ip-addr":"10.10.10.10",
        }
      ],
      "operational-mode":"monitor",
      },
      ]
    }
r = requests.put(url, data=json.dumps(zone_payload), headers=common_headers, verify=False)
print(r.content)

# Delete existing zone
zone_endpoint = '/axapi/v3/ddos/dst/zone/partner_test'
url = base_url + zone_endpoint
zone_payload = {}
r = requests.delete(url, headers=common_headers, verify=False)
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

