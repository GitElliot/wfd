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
    
    
    
    
print "Start Here"

# Get Active Campaign List for today
activeCampaignList = []
activeCampaignList = getActiveCampaigns(dbHostName, dbPortNumber)

print "Active Campaign Count " + str(len(activeCampaignList))
for campaignIndex in range (0,  len(activeCampaignList)):
    
    print "Start Campaign " + activeCampaignList[campaignIndex]
 
    activeStudentList = getActiveStudents(dbHostName, dbPortNumber, activeCampaignList[campaignIndex])
    
    for studentIndex in range (0,  len(activeStudentList)):
        print "STUDENT CELL " + activeStudentList[studentIndex]
     
        activeWordList = []
        activeWordList = getActiveWordList(dbHostName, dbPortNumber, activeCampaignList[0])
        
        for wordIndex in range (0, len(activeWordList)):
            print "Word Tag " + activeWordList[wordIndex]
        
#
#i = 0
#wi = 0
#si = 0
#
            localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print localtime
            logLine =  localtime + " Send word  group <<" + activeWordList[wordIndex] + ">>  to student " + activeStudentList[studentIndex]
            print logLine
            studentAddLogLine(dbHostName, dbPortNumber, activeStudentList[studentIndex], logLine)

            sendSMS(activeStudentList[studentIndex], activeWordList[wordIndex])


            ## Get WordGroup from DB to send
            thisWordGroup = getActiveWord(dbHostName, dbPortNumber, activeWordList[wordIndex])
#
            print "Length " + str(len(thisWordGroup))

            if (len(thisWordGroup) > 0):
                retVal = sendSMS(activeStudentList[studentIndex], thisWordGroup[0])
                print retVal
                retVal = sendSMS(activeStudentList[studentIndex], thisWordGroup[1])
                print retVal
                retVal = sendSMS(activeStudentList[studentIndex], thisWordGroup[2])
                print retVal
                retVal = sendSMS(activeStudentList[studentIndex], thisWordGroup[3])
                print retVal


