#!/usr/bin/python

#
# v0.1 created ban on ramp action for A10 TPS 
# Eric Chou (ericc@a10networks.com)
#

import smtplib
import sys
from sys import stdin
import optparse
import sys
import logging, json, urllib2

LOG_FILE = "/var/log/fastnetmon-notify.log"
MAIL_HOSTNAME="localhost"
MAIL_FROM="infra@example.com"
MAIL_TO="infra@example.com"


logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler(LOG_FILE)
handler.setFormatter(formatter)
logger.addHandler(handler)



client_ip_as_string=sys.argv[1]
data_direction=sys.argv[2]
pps_as_string=int(sys.argv[3])
action=sys.argv[4]

logger.info(" - " . join(sys.argv))



def mail(subject, body):
    fromaddr = MAIL_FROM
    toaddrs  = [MAIL_TO]

    # Add the From: and To: headers at the start!
    headers = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % (
                fromaddr,
                ", ".join(toaddrs), 
                subject
            )
    )

    msg = headers + body

    server = smtplib.SMTP(MAIL_HOSTNAME)
    #server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


# A10 AXAPIv3 Helper Functions

def axapi_auth(host, username, password):
    base_uri = 'https://'+host
    auth_payload = {"credentials": {"username": username, "password": password}}
    r = axapi_action(base_uri + '/axapi/v3/auth', payload=auth_payload)
    signature = json.loads(r)['authresponse']['signature']
    return base_uri, signature


def axapi_action(uri, payload='', signature='', method='POST'):
    try:
        if method == 'POST':
            req = urllib2.Request(uri)
            req.add_header('content-type', 'application/json')
            if signature:
                req.add_header('Authorization', 'A10 {0}'.format(signature))
            response = urllib2.urlopen(req, json.dumps(payload))
        elif method == 'GET':
            req = urllib2.Request(uri)
            req.add_header('content-type', 'application/json')
            if signature:
                req.add_header('Authorization', 'A10 {0}'.format(signature))
            response = urllib2.urlopen(req)
        return response.read()
    except Exception as e:
        print("Exception occured: " + str(e))

# A10 Mitigator Information
mitigator_ip = "192.168.199.152"

if action == "unban":
    subject = "Fastnetmon Guard: IP %(client_ip_as_string)s unblocked because %(data_direction)s attack with power %(pps_as_string)d pps" % {
        'client_ip_as_string': client_ip_as_string,
        'data_direction': data_direction,
        'pps_as_string' : pps_as_string,
        'action' : action
    }

    mail(subject, "unban")
    sys.exit(0)

elif action == "ban":
    subject = "Fastnetmon Guard: IP %(client_ip_as_string)s blocked because %(data_direction)s attack with power %(pps_as_string)d pps" % {
        'client_ip_as_string': client_ip_as_string,
        'data_direction': data_direction,
        'pps_as_string' : pps_as_string,
        'action' : action
    }

    body = "".join(sys.stdin.readlines())
    mail(subject, body)

    # A10 Mitigation On Ramp 
    mitigator_base_url, signature = axapi_auth(mitigator_ip, "admin", "a10")
    zone_name = client_ip_as_string + "_zone"
    ip_addr = client_ip_as_string
    port_num = 53
    port_protocol = 'udp'
    ddos_violation_action_payload = {
      "zone-list": [
        {
          "zone-name":zone_name,
          "ip": [
            {
              "ip-addr":ip_addr
            }
          ],
          "operational-mode":"monitor",
          "port": {
            "zone-service-list": [
              {
                "port-num":port_num,
                "protocol":port_protocol,
                "level-list": [
                  {
                    "level-num":"0",
                    "zone-escalation-score":1,
                    "indicator-list": [
                      {
                        "type":"pkt-rate",
                        "score":50,
                        "zone-threshold-num":1,
                        "zone-violation-actions":"bmf_a10_script",
                      }
                    ],
                  },
                  {
                    "level-num":"1",
                  }
                ],
              }
            ],
          },
        }
      ]
    }   
    r = axapi_action(mitigator_base_url+'/axapi/v3/ddos/dst/zone', signature=signature, payload=ddos_violation_action_payload)
    axapi_action(mitigator_base_url+'/axapi/v3/logoff', signature=signature)
    logger.info(r)
    
    sys.exit(0)


elif action == "attack_details":
    subject = "Fastnetmon Guard: IP %(client_ip_as_string)s blocked because %(data_direction)s attack with power %(pps_as_string)d pps" % {
        'client_ip_as_string': client_ip_as_string,
        'data_direction': data_direction,
        'pps_as_string' : pps_as_string,
        'action' : action
    }
    body = "".join(sys.stdin.readlines())


    mail(subject, body)
    sys.exit(0)

else:
    sys.exit(0)




