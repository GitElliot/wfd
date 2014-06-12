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

pauseBetweenWords = 5           # 5 minutes
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
myLog("WFD Server Start")

# Get Active Campaign List for today
activeCampaignList = []

# Main Loop  (limited)
for i in range(0, 320):
    time.sleep(10)

    print "MAIN LOOP COUNT " + str(i)

    activeCampaignList = getActiveCampaigns()
    
    print "Active Campaign Count " + str(len(activeCampaignList))
    for campaignIndex in range (0,  len(activeCampaignList)):
        
        print "Start Campaign " + activeCampaignList[campaignIndex]
     
        activeStudentList = getActiveStudents(activeCampaignList[campaignIndex])
     
        wordIndex = 0
        for studentIndex in range (0,  len(activeStudentList)):
            print "STUDENT CELL " + activeStudentList[studentIndex]
            
            student = studentGetRecord(activeStudentList[studentIndex])
            
            if (studentReadyForNextMessage(student)):                        # Word Groups 

#               Time to send next message to student.  It could be the                 
                                              
                print "Send Message Now"
                
                nextWord = studentGetNextWord(student)
                
                print "Send Next Word <" + nextWord + ">"
                
                activeWordList = []
                activeWordList = getActiveWordList(activeCampaignList[campaignIndex])
                
                for activeWordIndex in range (0, len(activeWordList)):
                    print "ACTIVE WORD LIST ElEMENTS " + activeWordList[activeWordIndex]
                                    
                
                for activeWordIndex in range (0, len(activeWordList)):
                    
                    activeWord = getWordBySeqNum(activeWordList[activeWordIndex])
                    print "activeWord -> " + activeWord
                    
                    if ((nextWord == "") or (activeWordList[activeWordIndex]  == nextWord)):
                                         
                        localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print localtime
                        logLine =  localtime + "Word Tag (" + activeWord + ")   <<" + activeWordList[activeWordIndex] + ">>  to student " + activeStudentList[studentIndex]
                        print logLine
                        studentAddLogLine(activeStudentList[studentIndex], logLine)
                        
                        currentMessageTime = time.time()
                        nextMessageTime = currentMessageTime + (pauseBetweenWords * 60)   # minutes * seconds
                                              
                        if (activeWordIndex + 1 < len(activeWordList)):                      
                            logLine = "Next Message Time <" + str(nextMessageTime) + ">"
                            logLine += "Next Word <" + activeWordList[activeWordIndex + 1] + ">"
                            print logLine
                            studentAddLogLine(activeStudentList[studentIndex], logLine)
                        else:
                            logLine = "<Words Done>"
                            print logLine
                            studentAddLogLine(activeStudentList[studentIndex], logLine)
                            logLine = "<Start Questions>"
                            print logLine
                            studentAddLogLine(activeStudentList[studentIndex], logLine)                                   
                            logLine = "Next Message Time <" + str(nextMessageTime) + ">"                
                            print logLine
                            studentAddLogLine(activeStudentList[studentIndex], logLine)        
                        ## Get WordGroup from DB to send
                        thisWordGroup = getActiveWord(activeWordList[activeWordIndex])
            
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
            
            elif (studentReadyForNextQuestion(student)):
                   print "Send Question with first answers"
                   
                   
                   logLine = "<Start Questions>"
                   print logLine
                   studentAddLogLine(activeStudentList[studentIndex], logLine)                   
                            
                   activeWordIndex = 0
                   activeWordList = []
                   activeWordList = getActiveWordList(activeCampaignList[campaignIndex])                   
                   thisQuestion = getActiveWordQuestion(activeWordList[activeWordIndex])
                   
                   logLine = "Next Word <" + activeWordList[activeWordIndex] + ">"
                   print logLine
                   studentAddLogLine(activeStudentList[studentIndex], logLine)
                   
                   logLine = "Question -> " + thisQuestion
                   print logLine
                   studentAddLogLine(activeStudentList[studentIndex], logLine)
                   retVal = sendSMS(activeStudentList[studentIndex], thisQuestion)
                   
                   
                   #Ans 1 
                   thisAnswer = getActiveWordAnswer(activeWordList[activeWordIndex], 1).strip()
                   if len(thisAnswer) > 0:                   
                       logLine = "ANS 1 -> " + thisAnswer                
                       print logLine
                       retVal = sendSMS(activeStudentList[studentIndex], thisAnswer)
                       studentAddLogLine(activeStudentList[studentIndex], logLine)
                       
                   #Ans 2 
                   thisAnswer = getActiveWordAnswer(activeWordList[activeWordIndex], 2).strip()
                   if len(thisAnswer) > 0:                   
                       logLine = "ANS 2 -> " + thisAnswer                
                       print logLine
                       retVal = sendSMS(activeStudentList[studentIndex], thisAnswer)
                       studentAddLogLine(activeStudentList[studentIndex], logLine)
                       
                   #Ans 3 
                   thisAnswer = getActiveWordAnswer(activeWordList[activeWordIndex], 3).strip()
                   if len(thisAnswer) > 0:                   
                       logLine = "ANS 3 -> " + thisAnswer                
                       print logLine
                       retVal = sendSMS(activeStudentList[studentIndex], thisAnswer)
                       studentAddLogLine(activeStudentList[studentIndex], logLine)                       
                      
                   #Ans 4 
                   thisAnswer = getActiveWordAnswer(activeWordList[activeWordIndex], 4).strip()
                   if len(thisAnswer) > 0:                   
                       logLine = "ANS 4 -> " + thisAnswer                
                       print logLine
                       retVal = sendSMS(activeStudentList[studentIndex], thisAnswer)
                       studentAddLogLine(activeStudentList[studentIndex], logLine)                          
                      
                   #Ans 5 
                   thisAnswer = getActiveWordAnswer(activeWordList[activeWordIndex], 5).strip()
                   if len(thisAnswer) > 0:                   
                       logLine = "ANS 5 -> " + thisAnswer                
                       print logLine
                       retVal = sendSMS(activeStudentList[studentIndex], thisAnswer)
                       studentAddLogLine(activeStudentList[studentIndex], logLine)
                       
                       
                   currentMessageTime = time.time()
                   nextMessageTime = currentMessageTime + (pauseBetweenQuestions * 60)   # minutes * seconds
                   
                   logLine = "Next Message Time <" + str(nextMessageTime) + ">"
                   print logLine
                   studentAddLogLine(activeStudentList[studentIndex], logLine)
                   
                   logLine = "Wait For Answer <" + activeWordList[activeWordIndex] + ">"
                   print logLine
                   studentAddLogLine(activeStudentList[studentIndex], logLine)
                   
                   
            else:    
                   print "Do Not Send Message"

           
           



