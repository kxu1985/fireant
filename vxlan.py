#!/usr/bin/python
import mininet, sys, os
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Host

net = Mininet()

print "Adding Hosts..."
red1 = net.addHost('red1')
blue1 = net.addHost('blue1')

print "Adding switch..."
s1 = net.addSwitch('s1')

print "Adding controller..."
c0 = net.addController('c0')

print "Adding links..."
net.addLink(red1,s1)
net.addLink(blue1,s1)
net.start()

print "Configuring hosts..."
red1.setIP('10.0.0.1/8')
blue1.setIP('10.0.0.1/8')
red1.setMAC('00:00:00:00:00:01')
blue1.setMAC('00:00:00:00:00:01')

CLI(net)
#net.stop()
