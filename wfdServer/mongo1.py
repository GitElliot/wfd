#!/usr/bin/python

import datetime
import time
import pymongo
import sys
from pymongo import Connection
from pymongo import database

from campaign  import *
from Students  import *
from atext import *
from WordGroups import *
from DB import *



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

# Main Loop  (limited)
for i in range(0, 60):
    time.sleep(10)

    print "MAIN LOOP COUNT " + str(i)

    activeCampaignList = getActiveCampaigns()
    
    print "Active Campaign Count " + str(len(activeCampaignList))
    for campaignIndex in range (0,  len(activeCampaignList)):
        
        print "Start Campaign " + activeCampaignList[campaignIndex]
     
        activeStudentList = getActiveStudents(dbHostName, dbPortNumber, activeCampaignList[campaignIndex])
     
        wordIndex = 0
        for studentIndex in range (0,  len(activeStudentList)):
            print "STUDENT CELL " + activeStudentList[studentIndex]
            
            student = studentGetRecord(dbHostName, dbPortNumber, activeStudentList[studentIndex])
            
            if (studentReadyForNextMessage(student)):
                print "Send Message Now"
                
                nextWord = studentGetNextWord(student)
                
                print "Send Next Word <" + nextWord + ">"
                
                activeWordList = []
                activeWordList = getActiveWordList(dbHostName, dbPortNumber, activeCampaignList[campaignIndex])
                
                for activeWordIndex in range (0, len(activeWordList)):
                    
                    if ((nextWord == "") or (activeWordList[activeWordIndex]  == nextWord)):
                        
                        sendSMS(activeStudentList[studentIndex], activeWordList[activeWordIndex])                    
            
                        localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print localtime
                        logLine =  localtime + " Send word  group <<" + activeWordList[activeWordIndex] + ">>  to student " + activeStudentList[studentIndex]
                        print logLine
                        studentAddLogLine(dbHostName, dbPortNumber, activeStudentList[studentIndex], logLine)
                        
                        currentMessageTime = time.time()
                        nextMessageTime = currentMessageTime + (5 * 60)   # minutes * seconds
                        
                        
                        if (activeWordIndex + 1 < len(activeWordList)):                      
                            logLine = "Next Message Time <" + str(nextMessageTime) + ">"
                            logLine += "Next Word <" + activeWordList[activeWordIndex + 1] + ">"
                            print logLine
                            studentAddLogLine(dbHostName, dbPortNumber, activeStudentList[studentIndex], logLine)
                        else:
                            logLine = "<Campaign Done>"
                            print logLine
                            studentAddLogLine(dbHostName, dbPortNumber, activeStudentList[studentIndex], logLine)                        
                
        
                        ## Get WordGroup from DB to send
                        thisWordGroup = getActiveWord(dbHostName, dbPortNumber, activeWordList[activeWordIndex])
            
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
                        break
     
            else:
                print "Do Not Send Message"
            
           
           



