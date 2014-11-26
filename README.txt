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
