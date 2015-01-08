=======================
Configure fireant nodes
=======================
1. Configure ccnx environment variables
  vim ~/.bashrc
  Append the following three lines:
    export CCND_DEBUG=71
    export CCNR_DIRECTORY=/home/htor/rsrepo
    export CCND_LOG=/tmp/ccnd.log
  source ~/.bashrc

2. Create the repository 'rsrepo' locally
  cd ~
  mkdir rsrepo

3. Modify the topo in 'start' script

4. Change the 'blockID'

5. Change the 'rsStatus'
  1: have available resources
  0: no available resources

=========================
Clean ccn daemon and logs
=========================
./clean

=================
Start ccn daemons
=================
./start

==============
A demo example
==============
Assume a three-node linear topo:
Fireant1 <---> Fireant2 <---> Fireant3

If you would like reserve resources like the following:
Fireant1 <---> Fireant2 <---> Fireant3
 |                 |             |
red1 <------------------------> red2
 |                 |
blue1 <--------> blue2

[red1, red2, blue1, blue2] are hosts created in Mininet,
representing vms in OpenStack.

The link between red hosts and blue hosts are vxlan tunnels.

Here are the steps to run this demo:
1. Modify start script on all Fireants to creat the topology.

2. Modify the flow.txt on each Fireant for Mininet configuration.

3. Modify rsresponse.josn on Fireant2 and Fireant3.
  3.1 Modify the vxlan ID.
  3.2 Modify the host IP address for tunneling endpoints.

4. Clean up everything and start on all Fireants.
  4.1 On Fireant1, run "sudo mn -c; ./clean; ./start; ./putbin"
  4.2 On Fireant2 and Fireant3, run "sudo mn -c; ./clean; ./start"

5. Create red1 and blue1 on Fireant1.
  5.1 On Fireant1, open a second terminal, run "sudo ./vxlan.py"

6. Start Fireant listening daemon on Fireant2 and Fireant3.
  6.1 On Fireant2 and Fireant3, run "./poke.py"

7. First, let Fireant3 has available resources.
  7.1 On Fireant3, run "echo 1 > rsStatus"
  7.2 On Fireant2, run "echo 0 > rsStatus"

8. Start resource discovery on Fireant1 for red2.
  8.1 On Fireant1, modify rsreq.json.
    8.1.1 change the ID
    8.1.2 change the vm alias
  8.2 On Fireant1, run "./peek.py"

9. Test red network on Fireant1
  9.1 On Fireant1's second terminal (Mininet), run "red1 ping 10.0.0.2"

10. Second, let Fireant2 has available resources.
  10.1 On Fireant2, run "echo 1 > rsStatus"
  10.2 On Fireant3, run "echo 0 > rsStatus"

11. Start resource discovery on Fireant 1 for blue2.
  11.1 On Fireant1, modify rsreq.json.
    11.1.1 change the ID
    11.1.2 change the vm alias
  11.2 On Fireant1, run "./peek.py"

12. Test blue network on Fireant1
  12.1 On Fireant1's second terminal (Mininet), run "blue1 ping 10.0.0.2"

