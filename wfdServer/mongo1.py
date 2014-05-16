#!/usr/bin/python

import datetime
import pymongo
from pymongo import Connection
from pymongo import database

from campaign  import *


# These items need to be moved to a config file
dbHostName = "localhost"
dbPortNumber =  3001


def fib(n):
    a, b = 0, 1
    while b < n :
        print b,
        a, b = b, a+b
        
        

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
    

print "HELLO WORLD"

# getWords()
getActiveCampaigns(dbHostName, dbPortNumber)
print "Done"

