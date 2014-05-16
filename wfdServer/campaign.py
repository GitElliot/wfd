#!/usr/bin/python

import datetime
import pymongo
from pymongo import Connection
from pymongo import database


def activeToday(camp, dayNumber):   

    
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
    
    return false
    
    
    
    


def getActiveCampaigns(dbHostName, dbPortNumber):
    print "ACTIVE CAMPAIGN"
    
    today = datetime.date.today()
    dayNumber = today.weekday()
    print "Today is day number " + str(dayNumber)
    
    connection = Connection(dbHostName, dbPortNumber)
    print "Connecting to Campaign"
    
    db = connection.meteor
    print "Connected to Campaign"
    
    collection = db.campaigns
    
    print "Campaign List"
    
    for camp in db.campaigns.find().sort("campaign", pymongo.ASCENDING):
        
         print camp['campaign']  + "   "        
        
        if activeToday(camp, dayNumber):
            print "Active"
    
        
    
    connection.close();
    
    print "End of Campaigns"
    