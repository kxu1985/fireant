#!/usr/bin/env python
import sys, subprocess, time, os, datetime, signal, json
from pprint import pprint

if sys.argv[1] == '172.16.10.67':
  vtepname = "vtep1"
  vtepport = "10"
else:
  vtepname = "vtep2"
  vtepport = "20"

cmd = "echo ctopassword | sudo -S ovs-vsctl add-port s1 " + vtepname +" -- \
      set interface " + vtepname + " type=vxlan option:remote_ip=" +\
      sys.argv[1] + " option:key=flow ofport_request=" + vtepport
os.system(cmd)
