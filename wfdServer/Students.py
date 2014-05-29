#!/usr/bin/python

import datetime
import time
import pymongo
from pymongo import Connection
from pymongo import database

def getActiveStudents(dbHostName, dbPortNumber, campaignID):
#    print "ACTIVE Students"
    
    
    connection = Connection(dbHostName, dbPortNumber)
#    print "Connecting to Students"

    try: 
        db = connection.meteor
        print "Connected to Students"
    
        collection = db.students
    
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


def studentAddLogLine(dbHostName, dbPortNumber, thisCellNumber, logLine):
    
    connection = Connection(dbHostName, dbPortNumber)   
    db = connection.meteor
    print "Connected to Students (for status log)" 	
    
    collection = db.students    

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
 

def studentGetRecord(dbHostName, dbPortNumber, thisCellNumber):
    
    connection = Connection(dbHostName, dbPortNumber)   
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
        
    connection.close()
    return  "" 
    
def studentReadyForNextMessage(student):
    nmt = "Next Message Time <"
    
    if (student == ""):
        return True
    
    s1 = student['studentStatus']
    
    if (s1.find("<Campaign Done>") > 0):
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

#    print "Time Now " + str(now)
    print "Time Difference " + str(delta)
    
    if (delta < 0.0):
        return True
    else:
        return False
    
    return True
    
#
# Next Word is stored in Student Record
def studentGetNextWord(student):
    nmt = "Next Word <"
    
    if (student == ""):
        return ""
    
    s1 = student['studentStatus'];
    
    i1  = s1.rfind(nmt)                           ####  .....Next Word <WWWWWWWWWW>
    
#    print "Index of next message   "  + str(i1)
    
    if (i1 < 0):
        return ""
    
    i1 += len(nmt)   #Get to start of tick count
    
    s2 = s1[i1:]                                 #### WWWWWWWWWWWW>
    
    i2 = s2.find(">")
    if (i2 < 0):
        return ""
    
    s3 = s2[:i2]                                ####  WWWWWWWWWWWWW
      
    return s3
