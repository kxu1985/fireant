#!/usr/bin/env python
import sys, subprocess, time, os, datetime, signal, json
from pprint import pprint

vxlan = sys.argv[1]
if vxlan == '100':
  in_port = '1'
  vtep_port = '10'
elif vxlan == '200':
  in_port = '2'
  vtep_port = '20'

cmd = "echo 'table=0,in_port=" + in_port + ",actions=set_field:" + \
      vxlan + "->tun_id,resubmit(,1)' > flows.txt;" + \
      "echo 'table=0,actions=resubmit(,1)' >> flows.txt;" + \
      "echo 'table=1,tun_id=" + vxlan + ",dl_dst=00:00:00:00:00:01" + \
      ",actions=output:" + in_port + "' >> flows.txt;" + \
      "echo 'table=1,tun_id=" + vxlan + ",dl_dst=00:00:00:00:00:02" + \
      ",actions=output:" + vtep_port + "' >> flows.txt;" + \
      "echo 'table=1,tun_id=" + vxlan + ",arp,nw_dst=10.0.0.1" + \
      ",actions=output:" + in_port + "' >> flows.txt;" + \
      "echo 'table=1,tun_id=" + vxlan + ",arp,nw_dst=10.0.0.2" + \
      ",actions=output:" + vtep_port + "' >> flows.txt;"
os.system(cmd)

cmd = "echo ctopassword | sudo -S ovs-ofctl add-flows s1 flows.txt"
os.system(cmd)
