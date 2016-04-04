#!/bin/bash - 
#===============================================================================
#
#          FILE: pktgen.sh
# 
#         USAGE: ./pktgen.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年04月01日 09:56
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

#!/bin/sh
# pktgen.conf -- Sample configuration for send on two devices on a UP system

#modprobe pktgen
#modprobe pktgen

function pgset() {
    local result

    echo $1 > $PGDEV
    result=`cat $PGDEV | fgrep "Result: OK:"`
    if [ "$result" = "" ]; then
         cat $PGDEV | fgrep Result:
    fi
}

function pg() {
    echo inject > $PGDEV
    cat $PGDEV
}

# On UP systems only one thread exists -- so just add devices
# We use eth0
echo "Adding devices to run".

PGDEV=/proc/net/pktgen/kpktgend_0
pgset "rem_device_all"
pgset "add_device eth0"
pgset "max_before_softirq 10000"

#pgset "add_device eth0"

# Configure the individual devices
echo "Configuring devices"

PGDEV=/proc/net/pktgen/eth0
#pgset "delay 0"
pgset "clone_skb 1000000"
pgset "pkt_size 60"
#pgset "min_pkt_size 60"
#pgset "max_pkt_size 60"
#pgset "min_pkt_size 92"
#pgset "max_pkt_size 92"


pgset "src_mac 70:71:BC:A8:5A:E8"
pgset "dst_mac 70:71:bc:dc:92:ab"

pgset "count 10000000"

# Time to run

PGDEV=/proc/net/pktgen/pgctrl

echo "Running... ctrl^C to stop"

pgset "start"

echo "Done"

cat /proc/net/pktgen/eth0

