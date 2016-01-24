#!/bin/sh

for i in `ls`;do
    if [ -f $i ]; then
        echo "æ®éæä»¶:$i"
    else
        echo "å¶ä»æä»¶:$i"
    fi
done


