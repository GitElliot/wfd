#!/usr/bin/python

import datetime
import time
import pymongo
import DB
import myLog
from pymongo import Connection
from pymongo import database


def getActiveStudents(campaignID):
#    print "ACTIVE Students"
    
    
    connection = Connection(getDBHost(), getDBPort())
#    print "Connecting to Students"

    try: 
        db = connection.meteor
        print "Connected to Students"
    
        activeStudentList = []
    
        print "Active Student List for Campaign " + campaignID
    
        for students in db.students.find({'campaign':campaignID}):         
#            print students['cell']  + "   "  + students['campaign']              
#            print " IS Active"
            activeStudentList.append(students['cell'])
             
        connection.close()
        
#        print "ACTIVE Students List EXIT"

        return activeStudentList
    
    except:
        print "GET ACTIVE STUDENT EXCEPTION"


def studentAddLogLine(thisCellNumber, logLine):
    
    connection = Connection(getDBHost(), getDBPort())   
    db = connection.meteor
    print "Connected to Students (for status log)" 	
    
    try: 
        student = db.students.find_one({'cell':thisCellNumber})
        
        if (student):
            thisLine = student['studentStatus'] + "\r\n" + logLine
            student['studentStatus'] = thisLine
                        
            db.students.update({'_id': student['_id']},  {'cell': student['cell'], 'name': student['name'],
                            'login':student['login'], 'pword':student['pword'], 'tzoffset': student['tzoffset'],
                            'allowaudio':student['allowaudio'], 'campaign':student['campaign'], 'studentStatus': thisLine}) 
           
            connection.close()
            return
            
    
    except Exception, e:
        print "Student Add Log Line EXCEPTION -- %s" % e
        
    connection.close()
    return
 

def studentGetRecord(thisCellNumber):
    
    connection = Connection(getDBHost(), getDBPort())   
    db = connection.meteor
    print "Connected to Students (for Get Record)" 	
    
    collection = db.students    

    try: 
        student = db.students.find_one({'cell':thisCellNumber})
        
        if (student):       
            connection.close()
            return student
            
    
    except Exception, e:
        print "Student Get Record EXCEPTION -- %s" % e
        return ""
        
    connection.close()
    return  "" 
 
   
def studentReadyForNextMessage(student, wordsPerDay):
    nmt = "Next Message Time <"
    rwfd = "RemainingWFD <"
    
    if (student == ""):
        return True
    
    s1 = student['studentStatus']
    
    print "STUDENT STRUCTURE CHECK     cell " + student['cell']
    
    if (s1.find("<Words Done>") > 0):
        return False
           
    i1  = s1.rfind(nmt)                           ####  .....Next Message Time <NNNNNNNNNN.NN>
    
#    print "Index of next message   "  + str(i1)
    
    if (i1 < 0):
        return True                              #### String not found, must be okay to send message
    
    i1 += len(nmt)   #Get to start of tick count
    
    s2 = s1[i1:]                                 #### NNNNNNNNNN.NN>
    
    i2 = s2.find(">")
    if (i2 < 0):
        myLog.Log("Data Error - studentReadyForNextMessage '>' tag missing")
        myLog.log(s1)
        return True                             #### Something not right,  send message anyway
    
    s3 = s2[:i2]                                #### NNNNNNNNNN.NN
    
    now = time.time()
    
    delta = float(s3) - now

#    print "Time Now " + str(now)
#    print "Time Difference " + str(delta)


    if (delta > 0):
        return False                           #### Not enough time has passed
    
    try:       # Catch possible exceptions for dealing with multiple words per day
        
        remainingWordTag = studentGetNextTagValue(rwfd, s1)    # Remaining Word For Day Count
    
        if (remainingWordTag == ""):
            return True
        
        rwc = remainingWordTag.split(",")     #### (day of week 0 - 6, remaining words for count)
        dayOfWeek = int(rwc[0])
        count = int(rwc[1])
        
        today = datetime.date.today()
        dayNumber = today.weekday()
        
        # If today is differernt from day last messsage was sent,  then send meessage today
        newrwdString = rfwd + str(dayNumber) + "," + str(wordsPerDay - 1) + ">"
        
        
        # If last message was sent today, determine if we can send another
        
    except:
        myLog.Log("Data Exception - studentReadyForNextMessage (multiple words per day)")
        myLog.log(s1)
        return True
    
    
    
    if (delta < 0.0):
        return True
    else:
        return False
    
    return True
    
#
    
def studentReadyForNextQuestion(student):
    
    print "Student Ready For Next Question?"
    nmt = "Next Message Time <"
    
    if (student == ""):
        return True
    
    s1 = student['studentStatus']
    
    
    if ((s1.find("<Words Done>")) < 0):         # Not ready for to send questions
#        print "<Words Done>"
        return False    
    
    if (s1.find("<Start Questions>") > 0):      # Questions in Progress
 #       print "<Start Questions>"
        return False
           
    i1  = s1.rfind(nmt)                           ####  .....Next Message Time <NNNNNNNNNN.NN>
    
#    print "Index of next message   "  + str(i1)
    
    if (i1 < 0):
        return True
    
    i1 += len(nmt)   #Get to start of tick count
    
    s2 = s1[i1:]                                 #### NNNNNNNNNN.NN>
    
    i2 = s2.find(">")
    if (i2 < 0):
        return True
    
    s3 = s2[:i2]                                #### NNNNNNNNNN.NN
    
    now = time.time()
    
    delta = float(s3) - now
    
    if (delta > 0.0):
        return False
    
    return True                                 # Okay to send out first series of questions


# Next Word is stored in Student Record    Check from the bottom up
def studentGetNextWord(student):
    nmt = "Next Word <"
    
    if (student == ""):
        return ""
    
    s1 = student['studentStatus'];
    
    i1  = s1.rfind(nmt)                           ####  .....Next Word <WWWWWWWWWW>
    
    print "Index of next message   "  + str(i1)
    
    if (i1 < 0):
        return ""
    
    i1 += len(nmt)   #Get to start of tick count
    
    s2 = s1[i1:]                                 #### WWWWWWWWWWWW>
    
    i2 = s2.find(">")
    if (i2 < 0):
        return ""
    
    s3 = s2[:i2]                                ####  WWWWWWWWWWWWW
      
    return s3



# Next Tag Value   stored in Student Record from the Bottom up
def studentGetNextTagValue(tag, student):
    nmt = tag
    
    if (student == ""):
        return ""
    
    s1 = student['studentStatus'];
    
    i1  = s1.rfind(nmt)                           ####  .....Next Word <WWWWWWWWWW>
    
    print "Index of next message   "  + str(i1)
    
    if (i1 < 0):
        return ""
    
    i1 += len(nmt)   
    
    s2 = s1[i1:]                                 #### WWWWWWWWWWWW>
    
    i2 = s2.find(">")
    if (i2 < 0):
        return ""
    
    s3 = s2[:i2]                                ####  WWWWWWWWWWWWW
      
    return s3