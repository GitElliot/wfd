#!/usr/bin/python

import datetime
import pymongo
import json

import httplib2
from httplib2 import *

import urllib
import requests
import sys

from campaign  import *
from Students  import *
from atext import *
from WordGroups import *
from DB import *

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
#    print r.text
    return r.text

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


#
#  Main Program Starts here
#
#  This routine is called from the php code sitting on the Web Server

mString = "message="
mStringLength = len(mString)
mStringIndex = 0

fString = ",from="
fStringLength =len(fString)
fStringIndex = 0

argv = sys.argv[1]           # expected input  program=WFD,message={1 - 5},from=7325551212

print argv


mStringIndex = argv.index(mString)
if mStringIndex < 1:
    print "message= not found"
    exit

fStringIndex = argv.index(fString)
if fStringIndex < 1:
    print "from= not found"
    exit

print "Message Index " + str(mStringIndex) + " from index " + str(fStringIndex)

message = argv[mStringIndex + mStringLength: fStringIndex]
print "message ->" + message + "<-"

cellNumber = argv[fStringIndex + fStringLength: fStringIndex + fStringLength + 11   ]

print "Cell Number ->" + cellNumber + "<-"

validNumbers = getSubscribers()
print validNumbers

try:
    if validNumbers.index(cellNumber):
        print "Valid Number"
        
except:
    print "Invalid Number"
    exit

if validNumbers.find(cellNumber, 11):
    print "Cell Number Found " +  cellNumber
    
    
#sendSMS(cellNumber, message)


localCellNumber = cellNumber[1:4] + "-" + cellNumber[4:7] + "-" + cellNumber[7:11]
print "Send Test Message  Local Cell Number " + localCellNumber

studentAddLogLine(localCellNumber, "<ANSWER >" + message + "</ANSWER>")


student = studentGetRecord(localCellNumber)

print student['studentStatus']
    


print "DONE"




