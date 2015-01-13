#!/usr/bin/env python
import sys, subprocess, time, os, datetime, signal, json
from pprint import pprint

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
    
    req_json = open('/tmp/'+interestFilename)
    req_data = json.load(req_json)
    pprint(req_data)
    req_json.close()

    f = open('/home/htor/Documents/fireant/rsStatus','r')
    isAvailable = int(f.readline().strip())
    if isAvailable == 1:
      isResponse = True
      print "Resources is available!!!"
    else:
      isResponse = False
      print "No available resources found!!!"


    if isResponse == True:
      servicebin = str(req_data['request']['bin_name'])

      if os.path.isfile('/home/htor/rsrepo/bin/'+servicebin):
        print "The binary " + servicebin + " already exists!"
      else:
        print "The binary " + servicebin + " does not exist! \
              Need to get this bin!"
        subprocess.call("ccngetfile -v ccnx:/rsrepo/" + servicebin \
                        + " /home/htor/rsrepo/bin/" + servicebin,shell=True)
      print "Got the binary " + servicebin + "... Checking resource..."

      print "Launching vms..."
      cmd = "nohup sudo /home/htor/Documents/fireant/vxlan_recv.py "+\
            req_data['request']['vm_alias'] + " " +\
            req_data['request']['vm_ip'] + " " +\
            req_data['request']['vm_mac'] + " &"
      subprocess.Popen(cmd,shell=True)
      time.sleep(2)     
      
      print "Configuring vxlan tunnel..."
      cmd = "~/Documents/fireant/tunnel_recv.py " + \
            req_data['request']['host_ip']
      subprocess.call(cmd,shell=True)
      
      print "Configuring flows..."
      cmd = "~/Documents/fireant/addflows_recv.py " + \
            req_data['request']['vm_ip'] + " " + \
            req_data['request']['vm_mac']
      subprocess.call(cmd,shell=True)
      
      print "Create resource spec json..."
      res_json = open('./rsresponse.json')
      res_data = json.load(res_json)
      #pprint(res_data)
      res_json.close()
      res_data['response']['ID'] = req_data['request']['ID']
      # hardcode, later we need to add more code here
      if res_data['response']['ID'] == 'red':
        res_data['response']['vxlan'] = 100
      else:
        res_data['response']['vxlan'] = 200
      res_json = open('./rsresponse_mod.json','w')
      print >> res_json, json.dumps(res_data,indent=2)
      res_json.close()

      print "\nResponding the interest..."
      #subprocess.call("echo '" + resFilename + "' | ccnpoke -v " + interestURL + " &",\
      #                shell=True)
      cmd = "cat rsresponse_mod.json | ccnpoke -v " + interestURL + " &"
      os.system(cmd)
      subprocess.call("sleep 2; killall ccnpoke",shell=True)
      
      responseList.append(interestFilename)
      #print responseList

  else:
    print str(time.time()) + ": No active interest"
