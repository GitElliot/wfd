#!/usr/bin/python

import datetime
import pymongo
from pymongo import Connection
from pymongo import database
from DB import *

def getActiveWordList(campaignID):
#    print "ACTIVE Words"
      
    connection = Connection(getDBHost(), getDBPort())
    print "Connecting to Words"
    
    db = connection.meteor
#    print "Connected to Words"    
    
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

def getActiveWord(thisWord):

     connection = Connection(getDBHost(), getDBPort())     
     wordGroupList = []
     print "Find This Word " + thisWord
     
     
     try: 
        db = connection.meteor    
        collection = db.words
        word = db.words.find_one({'seqnum':thisWord})
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
 
def getWordBySeqNum(seqNum):

     connection = Connection(getDBHost(), getDBPort())     
     thisWord = ""
     print "Find This Word By Seq " + seqNum
         
     try: 
        db = connection.meteor    
        word = db.words.find_one({'seqnum':seqNum})
        print "FOUND WORD BY SEQ NUM"
        thisWord = word['word']
        
     except Exception, e:
        print "GET WORD BY SEQ NUM EXCEPT -- %s" % e

        thisWord = ""
        
     connection.close()
        
     return thisWord   
      
        
def getActiveWordQuestion(thisWord):

     connection = Connection(getDBHost(), getDBPort())     
     question = ""
     print "Find This Word Question For " + thisWord
        
     try: 
        db = connection.meteor    
        collection = db.words
        word = db.words.find_one({'seqnum':thisWord})
        question = word['question']
        
     except:
        print "EXCEPTON - WORD QUESTION"
        question = ""
        
     connection.close()
        
     return question   

def getActiveWordAnswer(thisWord, ansNumber):

     connection = Connection(getDBHost(), getDBPort())     
     question = ""
     print "Find This Word Answer  " + thisWord  +  "    Answer Number  " + str(ansNumber)
        
     try: 
        db = connection.meteor    
        collection = db.words
        word = db.words.find_one({'seqnum':thisWord})
        connection.close()
        
        print "FOUND ANSWER"
        answer = ""
        
        if ansNumber > 5:
            answer = "Answer Number Error 2"
            
        if ansNumber < 1:
            answer = "Answer Number Error 1"
            
        ansIndex = "ans" + str(ansNumber)
        
        print "  Answer index  " + ansIndex
        answer = word[ansIndex]
        
        
     except:
        print "EXCEPTION -  ANSWER QUESTION"
        answer = ""
        
        
     return answer
    
def getActiveWordAnswerTF(thisWord, ansNumber):

     connection = Connection(getDBHost(), getDBPort())     
     question = ""
     print "Find This Word Answer TF " + thisWord  +  "    Answer Number  " + str(ansNumber)
        
     try: 
        db = connection.meteor    
        word = db.words.find_one({'seqnum':thisWord})
        connection.close()
        
        print "FOUND ANSWER"
        
        answer = "F"
        
        if ansNumber > 5:
            answer = "Answer Number Error 2"
            
        if ansNumber < 1:
            answer = "Answer Number Error 1"
            
        ansIndex = "active" + str(ansNumber)
        
        
        if (word[ansIndex] == True):
            answer = "T"
                   
        
     except:
        print "EXCEPTION -  TF ANSWER QUESTION"
        
        
     return answer

    
def getActiveWordRemediation(thisWord, rightWrong):

     connection = Connection(getDBHost(), getDBPort())     
     question = ""
     print "Find Correct Remediation for word " + thisWord  +  "   Right/Wrong  " + rightWrong
        
     try: 
        db = connection.meteor    
        word = db.words.find_one({'seqnum':thisWord})
        connection.close()
        
        print "Found Word"
        
        if (rightWrong == "Correct"):
            remediation = word['remedifcorrect']
        else:
            remediation = word['remedifwrong']
            
        return remediation    
        
                   
        
     except:
        print "EXCEPTION -  In getActiveWordRemediation"
        
        
     return ""
