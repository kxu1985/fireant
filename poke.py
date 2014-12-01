#!/usr/bin/env python
import sys, subprocess, time, os, datetime, signal

f = open('/home/htor/Documents/fireant/blockID','r')
blockID = f.readline().strip()
f.close()

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
  if proc[0] == '':
    print str(time.time()) + ': No fireant message.'
    continue

  recv_time = proc[0].split()[0]
  interestURL = proc[0].split()[5]
  interestFilename = interestURL.split('/')[2]
  #print "Interest URL", interestURL
  #print "Interest Filename", interestFilename
  #print recv_time
  #print time.time()

  if (time.time()-float(recv_time) < 30):
    print "\nActive request: " + interestFilename

    if interestFilename in responseList:
      print "Already responded."
      continue

    print "Reading the resource request..."
    subprocess.call("ccngetfile -v ccnx:/rsrepo/" + interestFilename \
                    + " /tmp/" + interestFilename,shell=True)

    print "\nAnalyzing available resources..."
    # Need to check OpenStack's plugin to decide
    f = open('/home/htor/Documents/fireant/rsStatus','r')
    isAvailable = int(f.readline().strip())
    if isAvailable == 1:
      isResponse = True
      print "Resources is available!!!"
    else:
      isResponse = False
      print "No available resources found!!!"

    if isResponse == True:
      print "Create resource spec json..."
      resFilename = 'res_' + str(blockID) + '_' + interestFilename
      subprocess.call("ccnputfile -v ccnx:/rsrepo/" + resFilename + \
                      " ~/Documents/fireant/rsresponse.json",shell=True)
      print "\nResponding the interest..."
      #subprocess.call("echo '" + resFilename + "' | ccnpoke -v " + interestURL \
      #                + " ; sleep 2; kill $!",shell=True)
      subprocess.call("echo '" + resFilename + "' | ccnpoke -v " + interestURL + " &",\
                      shell=True)
      subprocess.call("sleep 2; killall ccnpoke",shell=True)
      
      '''
      cmd = "echo '" + resFilename + "' | ccnpoke -v " + interestURL + ";"
      print cmd
      cmd = cmd.split(" ")
      print cmd
      start = datetime.datetime.now()
      process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
      
      timeout = 2;
      while process.poll() is None:
        print process.poll()
        time.sleep(1)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
          os.kill(process.pid, signal.SIGKILL)
          os.waitpid(-1, os.WNOHANG)
      '''

      responseList.append(interestFilename)
      #print responseList

  else:
    print str(time.time()) + ": No active interest"
