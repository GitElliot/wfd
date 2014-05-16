#!/usr/bin/python

import datetime
import pymongo

import httplib
import urllib

atextURL = "api.atext.com"
atextPort = 80


message1 = "/v2/0fffc340-8b99-0131-2454-40404d31061b/program/variables"
message2 = "/v1/0fffc340-8b99-0131-2454-40404d31061b/notify"
message3 = "/v1/0fffc340-8b99-0131-2454-40404d31061b/notify"
message4 = "/v1/0fffc340-8b99-0131-2454-40404d31061b/broadcast"
message5 = "/v1/0fffc340-8b99-0131-2454-40404d31061b/kick"

message6 = "/v2/0fffc340-8b99-0131-2454-40404d31061b/program/subscribers"

key = "0fffc340-8b99-0131-2454-40404d31061b"

def getSubscribers():
    conn = httplib.HTTPConnection(atextURL)
    conn.request("GET", message6)
    r1 = conn.getresponse();
    
    print r1.status
    print r1.reason
    print r.content
    
    return



def atextSend():
    
    #conn = httplib.HTTPConnection(atextURL, atextPort)
    #conn.connect()
    #
    #request = conn.putrequest('POST', message1)
    #
    #headers = {}
    #conn.send()
    #
    #resp = conn.getresponse()
    #print resp.status
    #print resp.read()
    
    conn = httplib.HTTPConnection(atextURL)
    conn.request("GET", message1)
    r1 = conn.getresponse();
    
    print r1.status
    print r1.reason
    print r1
    
    return
    
def atextPost():

#    params = urllib.urlencode( {"We've got trouble!"})
#    parms2 = {'number' : '7329798073', 'message':'We got trouble'};
#   parms2 = {'7329798073','We got trouble'};
    
#    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
#    conn = httplib.HTTPConnection("api.atext.com:80")

#     conn.request("POST", message3 , params2, headers)
     
#    conn.request("POST", message3 , params2)

    parms2 = {'number' : '7329798073', 'message':'Friday Message'};
    parms = urllib.urlencode(parms2)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.atext.com:80")
    conn.request("POST", message5, param, headers);


    response = conn.getresponse()
    print response.status, response.reason

    data = response.read()
    conn.close()
    
    return
    
    
print "ATEXT TEST"
atextSend()

print "ATEXT TEST DONE"




