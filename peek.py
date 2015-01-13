#!/usr/bin/env python
import sys,subprocess,time,pickle,os,json,base64
from xml.etree import ElementTree
from pprint import pprint

f = open('/home/htor/Documents/fireant/blockID','r')
blockID = f.readline().strip()
f.close()

#=========================
# Called by Plugin
# Input file: rsreq.json
#=========================
print '\nProcessing a request...'
out,err = subprocess.Popen("md5sum ~/Documents/fireant/rsreq.json",\
                            stdout=subprocess.PIPE,shell=True).communicate()
print out
reqfilename = 'req_profile_' + out.split()[0].strip() + '.json'
print reqfilename
subprocess.call("ccnputfile -v ccnx:/rsrepo/" + reqfilename + \
                " ~/Documents/fireant/rsreq.json",shell=True)

#=================
# Maintain request
#=================
pending_request = {}
res_json = open('./rsreq.json')
res_data = json.load(res_json)
print "\nRequest JSON File:"
pprint(res_data)
hostname = res_data['request']['ID']
# hardcode. Later we need to query mininet to get the info
if hostname == 'red':
  in_port = 1
else:
  in_port = 2
pending_request[hostname] = {'mac':'00:00:00:00:00:01', \
                              'ip':'10.0.0.1', 'in_port':in_port}
print "\nAdd pending request:"
print json.dumps(pending_request, indent=2)
res_json.close()

#===========================
# send out resource request
#===========================
lifetime = 20
waittime = lifetime
reqURL = 'ccnx:/fireant/' + reqfilename
print '\nSend out the request...'
proc = subprocess.Popen(['ccnpeek','-v','-l',str(lifetime),'-w',str(waittime),reqURL], \
                        stdout=subprocess.PIPE).communicate()
if proc[0] != '':
  print '\nGot a response...'
  #-------------------------------
  # Analyze the returned response
  #-------------------------------
  print 'Analyzing the response...'
  f = open('/tmp/recv_bin', 'w')
  f.write(proc[0])
  f.close()
  subprocess.call("ccn_ccnbtoxml -v /tmp/recv_bin | xmllint --format - \
                  > /tmp/recv_xml",shell=True)
  xmlorigin = ElementTree.parse('/tmp/recv_xml')
  #print xmlorigin
  xmlcontent = xmlorigin.find('Content')
  #print xmlcontent.tag
  #print xmlcontent.attrib
  print xmlcontent.text
  #print xmlcontent.tail
  responsefile = base64.b64decode(xmlcontent.text).strip()
  #print responsefile
  f = open('/tmp/rsresponse.json','w')
  f.write(responsefile)
  f.close()
  os.system('cat /tmp/rsresponse.json')
  #subprocess.call("ccngetfile -v ccnx:/rsrepo/" + responsefile + " /tmp/" + responsefile, \
  #                shell=True)
  #subprocess.call("cat /tmp/" + responsefile, shell=True)
  print '\nGOT RESOURCES!!!'

  res_json = open('/tmp/rsresponse.json')
  res_data = json.load(res_json)
  pprint(res_data)
  res_json.close()
  
  print "Configuring vxlan tunnel..."
  cmd = "/home/htor/Documents/fireant/tunnel_recv.py " + \
        res_data['response']['host_ip']
  subprocess.call(cmd,shell=True)

  print "Adding flows..."
  cmd = "/home/htor/Documents/fireant/addflows_sender.py " + \
        str(res_data['response']['vxlan'])
  subprocess.call(cmd,shell=True)

