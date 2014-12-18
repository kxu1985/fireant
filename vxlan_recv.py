#!/usr/bin/python
import mininet, sys, os, time
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Host

net = Mininet()

vm_alias = sys.argv[1]
vm_ip = sys.argv[2]
vm_mac = sys.argv[3]

print "Adding Hosts..."
vm = net.addHost(vm_alias,ip=vm_ip,mac=vm_mac)

print "Adding switch..."
s1 = net.addSwitch('s1')

print "Adding controller..."
c0 = net.addController('c0')

print "Adding links..."
net.addLink(vm,s1)
net.start()

while 1:
  time.sleep(1)

#CLI(net)
#net.stop()
