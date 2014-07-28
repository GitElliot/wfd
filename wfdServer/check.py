#!/usr/bin/python

import datetime
import time
import pymongo
import sys
import json
from pymongo import Connection
from pymongo import database

from campaign  import *
from Students  import *
from atext import *
from WordGroups import *
from DB import *

def getNextListItem(list, currentItem):
    l = len(list)
    for i in range(0, l):
        
        if (currentItem == list[i] and ((i + 1) >= l)):
            return "00000"
            
        if (currentItem == list[i]):
            return list[i + 1] 
    return "00000"


def ActiveWordCheck(): 
    print "Check Active Word Answer TF"
    
    student = studentGetRecord('732-979-8073')
    
    if (student == ""):
        print "student blank"
        exit()
    
    print student['studentStatus']
    
    thisWord = nextWord = studentGetNextWord(student)
    
    print "nextWord " + nextWord
    
    campaign = "RHzD8va7JfxEmru3h"
    
    activeWordList = []    
    activeWordList = getActiveWordList(campaign)
    
    print activeWordList
    
    print "Length " + str(len(activeWordList))
    
    current = "10017"
    next = ""
    
    next = getNextListItem(activeWordList, current)
        
    print "next " + next
    
# Next Tag Value   stored in Student Record from the Bottom up
def GetNextTagValue(tag, strng):
    nmt = tag
    
    s1 = strng
    
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

def secondsPastMidnight(hhmmString):
    
    print "Input String " + hhmmString
    
    ampmFlag = "AM"
    if (hhmmString.find("PM") > 0):
        ampmFlag = "PM"
    
    hhmm1 = hhmmString.replace(ampmFlag, "").strip()
    
    hhmmArray = hhmm1.split(':')
    
    hh = hhmmArray[0]
    mm = hhmmArray[1]
    
    print "hh " + hh + "  mm " + mm
    
    

    
#  print "Today is"

#  mmddyyyy = datetime.datetime.now().strftime("%m/%d/%Y")

#  print mmddyy

#   Return True if time is right to send message
def sendTimeCheck(hhmm):
    
    hhmmNow = time.strftime('%I:%M %p')
    
    if (hhmmNow.find("PM") > 0):
        hhmmNowFlag = "PM"
    else:
        hhmmNowFlag = "AM"
        
    if (hhmm.find("PM") > 0):
        hhmmFlag = "PM"
    else:
        hhmmFlag = "AM"
        
    if (hhmmFlag == hhmmNowFlag):
        hhmmNow = hhmmNow.replace("12:", "00:")    # Change 12:00 hours to 00:00 hours
        hhmm = hhmm.replace("12:", "00:")          # Change 12:00 hours to 00:00 hours
        if (hhmmNow  < hhmm):
            return False
        else:
            return True
        
    if (hhmmFlag == "PM"):
        return False
    
    return True
                

#timeCheck = "09:49 PM"
#
#if (sendTimeCheck(timeCheck) == True):
#    print " Time is " + timeCheck + " Time To Send"
#else:
#    print "Time is "  + timeCheck + " Do Not Send"
    
    
timeNow = time.strftime("%Y-%m-%d %H:%M:%S")
print timeNow

studentUpdateLastMessageSent("732-979-8073")

studentUpdateLastMessageReceived("732-979-8073")







