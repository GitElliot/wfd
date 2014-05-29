#!/usr/bin/python

import datetime
import time

oldticks =1400781270.24

print time.localtime(oldticks)

import datetime
import pymongo

ticks = time.time()

eventTime = ticks + 15

ss = str(ticks)
sf = float(ss)

while  (eventTime >= time.time()):
     print time.time()
     print str(sf)


print "DONE"