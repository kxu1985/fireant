#!/usr/bin/env python
import sys
import subprocess
import time

blockID = 2
responseList = []

while 1:
  time.sleep(1)
  #========================
  # Check incoming interest
  #========================
  subprocess.call("cat /tmp/ccnd.log | grep interest_from | grep fireant \
                  > /tmp/fireant.interest",shell=True)
  proc = subprocess.Popen(['tail','-n','1','/tmp/fireant.interest'], \
                          stdout=subprocess.PIPE).communicate()
  #print proc[0]
  recv_time = proc[0].split()[0]
  interestURL = proc[0].split()[5]
  interestFilename = interestURL.split('/')[2]
  print "Interest URL", interestURL
  print "Interest Filename", interestFilename
  #print recv_time
  #print time.time()

  if (time.time()-float(recv_time) < 30):
    if interestFilename in responseList:
      print "Already responded."
      continue

    print "Reading the resource request..."
    subprocess.call("ccngetfile -v ccnx:/rsrepo/" + interestFilename \
                    + " /tmp/" + interestFilename,shell=True)

    print "\nAnalyzing available resources...\n"
    # Need to check OpenStack's plugin to decide
    isResponse = True

    if isResponse == True:
      print "Create resource spec json...\n"
      resFilename = 'res_' + str(blockID) + '_' + interestFilename
      subprocess.call("ccnputfile -v ccnx:/rsrepo/" + resFilename + \
                      " ~/Documents/fireant/rsresponse.json",shell=True)
      print "Responding the interest...\n"
      subprocess.call("echo '" + resFilename + "' | ccnpoke -v " + interestURL,shell=True)

      responseList.append(interestFilename)
      print responseList

  else:
    print "No active interest"
