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

