#!/usr/bin/env python
import sys
import subprocess
import time

#========================
# Check incoming interest
#========================
subprocess.call("cat /tmp/ccnd.log | grep interest_from | grep fireant > /tmp/fireant.interest",shell=True)
proc = subprocess.Popen(['tail','-n','1','/tmp/fireant.interest'],stdout=subprocess.PIPE).communicate()
#print proc[0]
recv_time = proc[0].split()[0]
interestID = proc[0].split()[5]
#print interestID
#print recv_time
#print time.time()

if (time.time()-float(recv_time) < 30):
  print "Reading the resource request..."
  subprocess.call("ccngetfile -v ccnx:/rsrepo/rsreq.json /tmp/rsreq.json",shell=True)

  print "\nAnalyzing available resources...\n"
  isResponse = True
  if isResponse == True:
    print "Responding the interest...\n"
    subprocess.call("echo 'rsresponse.json' | ccnpoke -v " + interestID,shell=True)
else:
  print "No active interest"
