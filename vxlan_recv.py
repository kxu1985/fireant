#!/usr/bin/python
import mininet, sys, os, time
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Host

net = Mininet()

print "Adding Hosts..."
red2 = net.addHost('red2',ip='10.0.0.2',mac='00:00:00:00:00:02')
blue2 = net.addHost('blue2',ip='10.0.0.2',mac='00:00:00:00:00:02')

print "Adding switch..."
s1 = net.addSwitch('s1')

print "Adding controller..."
c0 = net.addController('c0')

print "Adding links..."
net.addLink(red2,s1)
net.addLink(blue2,s1)
net.start()

#print "Configuring hosts..."
#red2.setIP('10.0.0.2/8')
#blue2.setIP('10.0.0.2/8')
#red2.setMAC('00:00:00:00:00:02')
#blue2.setMAC('00:00:00:00:00:02')

while 1:
  time.sleep(1)

#CLI(net)
#net.stop()
