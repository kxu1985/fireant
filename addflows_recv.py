#!/usr/bin/env python
import sys, subprocess, time, os, datetime, signal, json
from pprint import pprint

vm_ip = sys.argv[1]
vm_mac = sys.argv[2]
vxlan = '100'

cmd = "echo 'table=0,in_port=1,actions=set_field:" + \
      vxlan + "->tun_id,resubmit(,1)' > flows.txt;" + \
      "echo 'table=0,actions=resubmit(,1)' >> flows.txt;" + \
      "echo 'table=1,tun_id=" + vxlan + ",dl_dst=" + vm_mac +\
      ",actions=output:1' >> flows.txt;" + \
      "echo 'table=1,tun_id=" + vxlan + ",dl_dst=" +\
      "00:00:00:00:00:01,actions=output:10' >> flows.txt;" + \
      "echo 'table=1,tun_id=" + vxlan + ",arp,nw_dst=" + vm_ip + \
      ",actions=output:1' >> flows.txt;" + \
      "echo 'table=1,tun_id=" + vxlan + ",arp,nw_dst=10.0.0.1" + \
      ",actions=output:10' >> flows.txt;"
os.system(cmd)

cmd = "echo ctopassword | sudo -S ovs-ofctl add-flows s1 flows.txt"
os.system(cmd)
