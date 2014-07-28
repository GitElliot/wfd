#!/usr/bin/python

import datetime
import time
import os
import os.path


LogRoot = "/tmp"


def Log(line):
    logFileName  = LogRoot + "/" + "WFD_" + time.strftime('%Y%m%d') + ".txt"
    
    try:
        os.stat(LogRoot)
    except:
        print "LogRoot Directory Did Not Exist " + LogRoot
        os.mkdir(LogRoot)
        print "EXCEPT log"
    try:
        f = open(logFileName, "a")
        now = time.strftime('%Y%m%d %H:%M ')
        f.write(now + line + "\n")
        f.close()
    except:
        print "Log File Write Exception"