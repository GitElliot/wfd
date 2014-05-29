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


# These items need to be moved to a config file
dbHostName = "localhost"
dbPortNumber =  3001

connection = Connection(dbHostName, dbPortNumber)
print "Connecting to Campaign"
    
db = connection.meteor
print "Connected to Campaign"
    
collection = db.campaigns

print "Campaign List"
a = bool
    
        
for camp in db.campaigns.find().sort("campaign", pymongo.ASCENDING):
    print "->" + camp['campaign'] + "<-    "  + camp['_id'] + "   "  +  camp['cwordorder']
    
    try:
        a = camp['friactive']
        print "a is  " + str(a)
    except Exception, e:
        print  'Exception Error is: %s'  %e 
        
        
    
wordCollection = db.Words
for word in db.words.find().sort('seqnum'):
    print word['seqnum']  + "    "  + word['word']

