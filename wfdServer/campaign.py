#!/usr/bin/python

import datetime
import time
import pymongo
import DB
import myLog

from pymongo import Connection
from pymongo import database
from atext import *



def excludeToday(campName, xlist):
    
   print "Excluded date list " + xlist
           
   if (xlist == ""):
     return False

   mmddyyyy = datetime.datetime.now().strftime("%m/%d/%Y")
   
   if xlist.find(mmddyyyy):
      print "EXCLUDE DEBUG mmddyyyy " + mmddyyyy + "    xlist-> " + xlist
      return True
   
   return False
    

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

def activeToday(camp, dayNumber):
#    print "activeToday()"
    try:
               
        campaignTime  = camp['sendtime']        # Time has to be in correct format
        campaignTime = campaignTime.strip()
        if (sendTimeCheck(campaignTime) == False):
            return False
               
        if dayNumber == 0:
            return camp['monactive']
        
        if dayNumber == 1:
            return camp['tueactive']
        
        if dayNumber == 2:
            return camp['wedactive']
        
        if dayNumber == 3:
            return camp['thuactive']
        
        if dayNumber == 4:
            return camp['friactive']
        
        if dayNumber == 5:
            return camp['satactive']
        
        if dayNumber == 6:
            return camp['sunactive']
    
    except:
            msg = "Exception - activeToday() "
            print msg
            myLog.Log(msg)
            return False
      
    return False

def getActiveCampaigns():
    print "GET ACTIVE CAMPAIGN"
    
    today = datetime.date.today()
    dayNumber = today.weekday()
    print "Today is day number " + str(dayNumber)
    
    connection = Connection(DB.getDBHost(), DB.getDBPort())
#    print "Connecting to Campaign"
    
    db = connection.meteor
#    print "Connected to Campaign"
    
    collection = db.campaigns
    
    activeCampaignList = []
    print "Campaign List"
    
        
    for camp in db.campaigns.find().sort("campaign", pymongo.ASCENDING):

#        print "Campaign Loop " + camp['campaign']
#        print "Campaign Exclude Dates " + camp['xdatelist']
        try:
            if ((camp['campaign'], camp['xdatelist']) == True):
                print "Campaign Excluded Today - " + camp['campaign'] 
                continue
            
#            print "Campaign Not Excluded Today - " + camp['campaign']        
                      
            if activeToday(camp, dayNumber):            
                print "Campaign Active Today - " + camp['campaign']
                activeCampaignList.append(camp['_id'])
#            else:
#                print "Campaign Not Active Today - " + camp['campaign']
                       
        except Exception, e:
                msg = "Exception:  getActiveCampaigns EXCEPTION -- %s" % e
                print msg
                print "Exception in calling activeToday()"
                print "Campaign " + camp['campaign']
                myLog.Log(msg)
            
            
    connection.close();            
    return activeCampaignList    

    
#    print "End of Campaigns"


#   print "Campaigns Now"

def getActiveWordList(campaignID):
    print "ACTIVE Word List Order"
      
    connection = Connection(DB.getDBHost(), DB.getDBPort())
#    print "Connecting to Campaigns"
    
    db = connection.meteor
#    print "Connected to Words"    
    
    activeWordList = []
#    print "Active Word List Order"
    
    campaign = db.campaigns.find_one({"_id":campaignID})
    
    connection.close()
    
    if (campaign == ""):
        return ""
    
    wordOrder = campaign['cwordorder']
    
    if (wordOrder == ""):
        return ""
    
    wordOrderArray = wordOrder.split(",")
    
    for word in wordOrderArray:
        if (len(word) > 0):
            activeWordList.append(word)             
 #           print "activeWordList  add- > " + word
    
    return activeWordList    
#  
##    print "End of Words"




def getCampaignName(campaignID):
 #   print "Get Campaign Name"
      
    connection = Connection(DB.getDBHost(), DB.getDBPort())
    
    try:
        
        db = connection.meteor
         
        campaign = db.campaigns.find_one({"_id":campaignID})
        
        connection.close()
        
        if (campaign == ""):
            return "N/A"
        
        name  = campaign['campaign']
        
        if (name  == ""):
            return "N/A"
    
        return name
    
    except Exception, e:      
        msg = "Exception:  getCampaign Exception " + campaignID + "   -- %s "  % e
        print msg
        myLog.Log(msg)
        return "N/A"    

def getCampaignWordsPerDay(campaignID):
 #   print "Get Campaign Words Per Day"
      
    connection = Connection(DB.getDBHost(), DB.getDBPort())
    
    try:
        
        db = connection.meteor
         
        campaign = db.campaigns.find_one({"_id":campaignID})
        
        connection.close()
        
        if (campaign == ""):
            return "1"
        
        wordsPerDay = campaign['sendcount']
        
        if (wordsPerDay == ""):
            return "1"
    
        return wordsPerDay
    
    except Exception, e:      
        msg = "Exception:  getCampaignWordsPerDay " + campaignID + "   -- %s "  % e
        print msg
        myLog.Log(msg)
        
        return "1"


