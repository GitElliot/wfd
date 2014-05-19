#!/usr/bin/python

import datetime
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
    
        print "Active Student List"
    
        for students in db.students.find({'campaign':campaignID}):
            print students['cell']  + "   "                
            print " IS Active"
            activeStudentList.append(students['cell'])
             
        connection.close();
    
        print "ACTIVE Students List EXIT"

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
        print "AA + id " + student['_id']
        
        if (student):
            print "BB"
            thisLine = student['studentStatus'] + "\r\n" + logLine
            print "OLD + NEW " + thisLine
            student['studentStatus'] = thisLine
            print "CC"
            
#            db.students.update ({'cell': thisCellNumber}, {set: {        'studentStatus': logLine}})
            
            db.students.update({'_id': student['_id']},  {'cell': student['cell'], 'name': student['name'],
                            'login':student['login'], 'pword':student['pword'], 'tzoffset': student['tzoffset'],
                            'allowaudio':student['allowaudio'], 'campaign':student['campaign'], 'studentStatus': thisLine}) 
            
                       
#                Students.update(Session.get('editing_student'), {$set: {cell:cell, name:name, login:login, pword:pword,
#                    tzoffset:tzoffset, allowaudio:al lowaudio, campaign:campaign, studentStatus:studentStatus}}); 
            
            
            print "DD"
            connection.close()
            return
            
    
    except Exception, e:
        print "Student Add Log Line EXCEPTION -- %s" % e
        
    connection.close()
    return
    
    
