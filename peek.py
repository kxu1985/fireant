#!/usr/bin/env python
import sys
import subprocess
import time
import pickle
from xml.etree import ElementTree
import base64

f = open('/home/htor/Documents/fireant/blockID','r')
blockID = f.readline().strip()
f.close()

#=========================
# Called by Plugin
# Input file: rsreq.json
#=========================
reqfilename = 'req_' + str(blockID) + '_' + str(time.time()) + '.json'
subprocess.call("ccnputfile -v ccnx:/rsrepo/" + reqfilename + \
                " ~/Documents/fireant/rsreq.json",shell=True)

#===========================
# send out resource request
#===========================
lifetime = 10
waittime = lifetime
reqURL = 'ccnx:/fireant/' + reqfilename
proc = subprocess.Popen(['ccnpeek','-v','-l',str(lifetime),'-w',str(waittime),reqURL], \
                        stdout=subprocess.PIPE).communicate()
if proc[0] != '':
  #-------------------------------
  # Analyze the returned response
  #-------------------------------
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
  print responsefile
  subprocess.call("ccngetfile -v ccnx:/rsrepo/" + responsefile + " /tmp/" + responsefile, \
                  shell=True) 
