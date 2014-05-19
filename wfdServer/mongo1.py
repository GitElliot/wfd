#!/usr/bin/python

import datetime
import time
import pymongo
from pymongo import Connection
from pymongo import database

from campaign  import *
from Students  import *
from atext import *
from WordGroups import *


# These items need to be moved to a config file
dbHostName = "localhost"
dbPortNumber =  3001


       
        

def getWords():
    connection = Connection('localhost', 3001)
    print "Connecting"
    
    db = connection.meteor
    print "Connected"
    
    collection = db.words
    print "Collection"
    
    #for item in db.words.find().sort("seqnum", pymongo.ASCENDING):
    #    print item['word']
        
    
    print "end"
    
    connection.close()
    

print "HELLO WORLD"

# getWords()
activeCampaignList = []
activeCampaignList = getActiveCampaigns(dbHostName, dbPortNumber)
print activeCampaignList[0]

activeStudentList = getActiveStudents(dbHostName, dbPortNumber, activeCampaignList[0])

activeWordList = []
activeWordList = getActiveWordList(dbHostName, dbPortNumber, activeCampaignList[0])

i = 0
wi = 0
si = 0

localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#print localtime

logLine =  localtime + " Send word  group <<" + activeWordList[wi] + ">>  to student " + activeStudentList[si]
print logLine
studentAddLogLine(dbHostName, dbPortNumber, activeStudentList[si], logLine)

#sendSMS(activeStudentList[i], activeWordList[i])

#
# Get WordGroup from DB to send
thisWordGroup = getActiveWord(dbHostName, dbPortNumber, activeWordList[i])

print "Length " + str(len(thisWordGroup))

if (len(thisWordGroup) > 0):
    retVal = sendSMS(activeStudentList[i], thisWordGroup[0])
    print retVal
    retVal = sendSMS(activeStudentList[i], thisWordGroup[1])
    print retVal
    retVal = sendSMS(activeStudentList[i], thisWordGroup[2])
    print retVal
    retVal = sendSMS(activeStudentList[i], thisWordGroup[3])
    print retVal


