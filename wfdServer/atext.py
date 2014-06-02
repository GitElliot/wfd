#!/usr/bin/python

import datetime
import pymongo

import httplib2
from httplib2 import *

import urllib
import requests
import sys

atextURL = "http://api.atext.com"
atextPort = 80


message1 = "/v2/0fffc340-8b99-0131-2454-40404d31061b/program/variables"
message2 = "/v1/0fffc340-8b99-0131-2454-40404d31061b/notify"

message4 = "/v1/0fffc340-8b99-0131-2454-40404d31061b/broadcast"
message5 = "/v1/0fffc340-8b99-0131-2454-40404d31061b/kick"

message6 = "/v2/0fffc340-8b99-0131-2454-40404d31061b/program/subscribers"

key = "0fffc340-8b99-0131-2454-40404d31061b"




def getSubscribers():      
    m = atextURL + message6
    r = requests.get(m)
    print r.content  
    return r.content

def sendSMS(cell, message):
    cell = cell.replace("-","")
    m = atextURL + message2
    payload = {'number' : cell, 'message' : message}  
    r = requests.post(m, data=payload)
    return r.text
    
def sendTest():   
    payload = {'number' : '7329798073', 'message' : 'Testing 123 321 '}
    m = atextURL + message4
    r = requests.post(m, data=payload)
    return

cellNumber = sys.argv[1]

validNumbers = getSubscribers()
print validNumbers

if validNumbers.find(cellNumber):
    print "ATEXT TEST to " +  cellNumber
    
    retVal = sendSMS(cellNumber, "1 2 3 4 5")


print "DONE"




