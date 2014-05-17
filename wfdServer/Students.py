#!/usr/bin/python

import datetime
import pymongo
from pymongo import Connection
from pymongo import database



def getActiveStudents(dbHostName, dbPortNumber, campaignID):
    print "ACTIVE Students"
    
    
    connection = Connection(dbHostName, dbPortNumber)
    print "Connecting to Students"
    
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