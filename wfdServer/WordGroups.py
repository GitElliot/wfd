#!/usr/bin/python

import datetime
import pymongo
from pymongo import Connection
from pymongo import database

def getActiveWordList(dbHostName, dbPortNumber, campaignID):
#    print "ACTIVE Words"
      
    connection = Connection(dbHostName, dbPortNumber)
    print "Connecting to Words"
    
    db = connection.meteor
#    print "Connected to Words"
    
    collection = db.words
    
    activeWordList = []
#    print "Active Word List"
    
    for word in db.words.find().sort("seqnum", pymongo.ASCENDING):
        
        try:
            campaigns = word['campaign']
            if campaigns.index(campaignID) >= 0 :
                print "Word FOUND " + word['word']
                print campaigns
                activeWordList.append(word['word'])                
        except:
            campaigns = ""
                               
    connection.close();            
    return activeWordList    
  
#    print "End of Words"

def getActiveWord(dbHostName, dbPortNumber, thisWord):

     connection = Connection(dbHostName, dbPortNumber)     
     wordGroupList = []
     print "Find This Word " + thisWord
     
     
     try: 
        db = connection.meteor    
        collection = db.words
        word = db.words.find_one({'word':thisWord})
        print "FOUND WORD"
        wordGroupList.append(word['instruction'])
        wordGroupList.append(word['use1'])
        wordGroupList.append(word['use2'])
        wordGroupList.append(word['use3'])
        
     except:
        print "EXCEPT WORD"
        wordGroupList = []
        
     connection.close()
        
     return wordGroupList   
        

