#!/usr/bin/env python
import sys
import subprocess
import time

blockID = 1

#=========================
# Called by Plugin
# Input file: rsreq.json
#=========================
reqfile = 'rsreq.json'
subprocess.call("ccnputfile -v ccnx:/rsrepo/rsreq.json ~/Documents/fireant/rsreq.json",shell=True)

#===========================
# send out resource request
#===========================
lifetime = 3
waittime = lifetime
reqID = 'ccnx:/fireant/req_' + str(blockID) + '_' + str(time.time())
proc = subprocess.Popen(['ccnpeek','-v','-l',str(lifetime),'-w',str(waittime),reqID], stdout=subprocess.PIPE).communicate()
print proc
