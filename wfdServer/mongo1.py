#!/usr/bin/python

import datetime
import time
import pymongo
import sys
from pymongo import Connection
from pymongo import database

import myLog
import campaign
import Students
import WordGroups

from atext import *
from DB import *

pauseBetweenWords = 60          # 60 minutes
pauseBetweenQuestions = 10      # 10 minutes 


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
myLog.Log("WFD Server Start")

# Get Active Campaign List for today
activeCampaignList = []

# Main Loop  (limited)
#for i in range(0, 10000):
i = 0
while True:
    i = i + 1
    
    time.sleep(10)

    msg =  "MAIN LOOP Iteration COUNT " + str(i)
    print msg
#    myLog.Log(msg)

    activeCampaignList = campaign.getActiveCampaigns()
    
    msg = "Active Campaign Count " + str(len(activeCampaignList))
    print msg
#    myLog.Log(msg)
    for campaignIndex in range (0,  len(activeCampaignList)):
        
        msg = "Start Campaign " + campaign.getCampaignName(activeCampaignList[campaignIndex])
        print msg
#        myLog.Log(msg)
                
        campaignWordsPerDay = campaign.getCampaignWordsPerDay(activeCampaignList[campaignIndex])
        print "Campaign Words Per Day " + campaignWordsPerDay        
           
        activeStudentList = Students.getActiveStudents(activeCampaignList[campaignIndex])
     
        wordIndex = 0
        for studentIndex in range (0,  len(activeStudentList)):
            print "STUDENT CELL " + activeStudentList[studentIndex]
            
            student = Students.studentGetRecord(activeStudentList[studentIndex])
            
            if (Students.studentReadyForNextMessage(student, campaignWordsPerDay)): 

#               Time to send next message to student.                 
                                              
                print "Send Message Now"
                
                nextWord = Students.studentGetNextWord(student)
                
                msg =  "Send Next Word Group Now <" + nextWord + ">"
                print msg
                myLog.Log(msg)
                
                activeWordList = []
                activeWordList = campaign.getActiveWordList(activeCampaignList[campaignIndex])

                
                for activeWordIndex in range (0, len(activeWordList)):
                    print "ACTIVE WORD LIST ElEMENTS " + activeWordList[activeWordIndex]
                                    
                
                for activeWordIndex in range (0, len(activeWordList)):
                    
                    activeWord = WordGroups.getWordBySeqNum(activeWordList[activeWordIndex])
                    print "activeWord -> " + activeWord
                    
                    mesg = "Cell " + activeStudentList[studentIndex] +  "   Word  " + activeWord
                    myLog.Log(mesg)
                    
                    if ((nextWord == "") or (activeWordList[activeWordIndex]  == nextWord)):
                                         
                        localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print localtime
                        logLine =  localtime + "Word Tag (" + activeWord + ")   <<" + activeWordList[activeWordIndex] + ">>  to student " + activeStudentList[studentIndex]
                        print logLine
                        
                        Students.studentAddLogLine(activeStudentList[studentIndex], logLine)
                        
                        currentMessageTime = time.time()
                        nextMessageTime = currentMessageTime + (pauseBetweenWords * 60)   # minutes * seconds
                                              
                        if (activeWordIndex + 1 < len(activeWordList)):                      
                            logLine = "Next Message Time <" + str(nextMessageTime) + ">"
                            logLine += "Next Word <" + activeWordList[activeWordIndex + 1] + ">"
                            print logLine
                            Students.studentAddLogLine(activeStudentList[studentIndex], logLine)
                        else:
                            Students.studentAddLogLine(activeStudentList[studentIndex], logLine)
                            logLine = "<Words Done>"
                            print logLine
                            Students.studentAddLogLine(activeStudentList[studentIndex], logLine)                                   
                            logLine = "Next Message Time <" + str(nextMessageTime) + ">"                
                            print logLine
                            Students.studentAddLogLine(activeStudentList[studentIndex], logLine)        
                        ## Get WordGroup from DB to send
                        thisWordGroup = WordGroups.getActiveWord(activeWordList[activeWordIndex])
            
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
            
            elif (Students.studentReadyForNextQuestion(student)):
                   print "Send Question with first answers"
                                     
                   logLine = "<Start Questions>"
                   print logLine
                   Students.studentAddLogLine(activeStudentList[studentIndex], logLine)                   
                            
                   activeWordIndex = 0
                   activeWordList = []
                   activeWordList = WordGroups.getActiveWordList(activeCampaignList[campaignIndex])                   
                   thisQuestion = WordGroups.getActiveWordQuestion(activeWordList[activeWordIndex])
                   
                   logLine = "Next Word <" + activeWordList[activeWordIndex] + ">"
                   print logLine
                   Students.studentAddLogLine(activeStudentList[studentIndex], logLine)
                   
                   logLine = "Question -> " + thisQuestion
                   print logLine
                   Students.studentAddLogLine(activeStudentList[studentIndex], logLine)
                   retVal = sendSMS(activeStudentList[studentIndex], thisQuestion)
                   
                   msg = "Send Question   Cell: " + activeStudentList[studentIndex] + "   Question: " + thisQuestion
                   
                   
                   #Ans 1 
                   thisAnswer = WordGroups.getActiveWordAnswer(activeWordList[activeWordIndex], 1).strip()
                   if len(thisAnswer) > 0:                   
                       logLine = "ANS 1 -> " + thisAnswer                
                       print logLine
                       retVal = sendSMS(activeStudentList[studentIndex], thisAnswer)
                       Students.studentAddLogLine(activeStudentList[studentIndex], logLine)
                       
                   #Ans 2 
                   thisAnswer = WordGroups.getActiveWordAnswer(activeWordList[activeWordIndex], 2).strip()
                   if len(thisAnswer) > 0:                   
                       logLine = "ANS 2 -> " + thisAnswer                
                       print logLine
                       retVal = sendSMS(activeStudentList[studentIndex], thisAnswer)
                       Students.studentAddLogLine(activeStudentList[studentIndex], logLine)
                       
                   #Ans 3 
                   thisAnswer = WordGroups.getActiveWordAnswer(activeWordList[activeWordIndex], 3).strip()
                   if len(thisAnswer) > 0:                   
                       logLine = "ANS 3 -> " + thisAnswer                
                       print logLine
                       retVal = sendSMS(activeStudentList[studentIndex], thisAnswer)
                       Students.studentAddLogLine(activeStudentList[studentIndex], logLine)                       
                      
                   #Ans 4 
                   thisAnswer = WordGroups.getActiveWordAnswer(activeWordList[activeWordIndex], 4).strip()
                   if len(thisAnswer) > 0:                   
                       logLine = "ANS 4 -> " + thisAnswer                
                       print logLine
                       retVal = sendSMS(activeStudentList[studentIndex], thisAnswer)
                       Students.studentAddLogLine(activeStudentList[studentIndex], logLine)                          
                      
                   #Ans 5 
                   thisAnswer = WordGroups.getActiveWordAnswer(activeWordList[activeWordIndex], 5).strip()
                   if len(thisAnswer) > 0:                   
                       logLine = "ANS 5 -> " + thisAnswer                
                       print logLine
                       retVal = sendSMS(activeStudentList[studentIndex], thisAnswer)
                       studentAddLogLine(activeStudentList[studentIndex], logLine)
                       
                       
                   currentMessageTime = time.time()
                   nextMessageTime = currentMessageTime + (pauseBetweenQuestions * 60)   # minutes * seconds
                   
                   logLine = "Next Message Time <" + str(nextMessageTime) + ">"
                   print logLine
                   Students.studentAddLogLine(activeStudentList[studentIndex], logLine)
                   
                   logLine = "Wait For Answer <" + activeWordList[activeWordIndex] + ">"
                   print logLine
                   Students.studentAddLogLine(activeStudentList[studentIndex], logLine)
                   
                   
            else:    
                   print "Do Not Send Message"

           
           



