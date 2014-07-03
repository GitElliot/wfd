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
    
print "Today is"

mmddyyyy = datetime.datetime.now().strftime("%m/%d/%Y")

print mmddyyyy

w1 = "xxxxxxxxxxxxxxxxxxxxxRemainingWFD<0,4>bbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

w2 = GetNextTagValue("RemainingWFD<", w1)

print w2

w3 = w2.split(",")

print w3

w4 = w3[0]

w5 = w3[1]

print "w4  ="  + w4 + "    w5 = " + w5

w6 = int(w5)  - 1

print "w6" + str(w6)







