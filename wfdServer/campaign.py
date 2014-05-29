#!/usr/bin/python

import datetime
import pymongo
from pymongo import Connection
from pymongo import database
from DB import *
from atext import *


def activeToday(camp, dayNumber):

    try:
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
            return false
      
    return false

def getActiveCampaigns():
    print "GET ACTIVE CAMPAIGN"
    
    today = datetime.date.today()
    dayNumber = today.weekday()
    print "Today is day number " + str(dayNumber)
    
    connection = Connection(getDBHost(), getDBPort())
    print "Connecting to Campaign"
    
    db = connection.meteor
    print "Connected to Campaign"
    
    collection = db.campaigns
    
    activeCampaignList = []
    print "Active Campaign List"
    
        
    for camp in db.campaigns.find().sort("campaign", pymongo.ASCENDING):

#        print "Campaign Loop " + camp['campaign']          
        try:
            if activeToday(camp, dayNumber):            
                print "Campaign " + camp['campaign']  + " is Active"
                activeCampaignList.append(camp['_id'])            
                       
        except Exception, e:
                print "getActiveCampaigns EXCEPTION -- %s" % e
                print "Exception in calling activeToday()"
                print "Campaign " + camp['campaign']               
            
            
    connection.close();            
    return activeCampaignList    

    
#    print "End of Campaigns"


print "Campaigns Now"


    