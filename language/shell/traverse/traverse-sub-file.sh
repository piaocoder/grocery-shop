#!/bin/sh

lsDir()
{
    for i in `ls`;do
        if [ -d $i ];then
            echo "____________$i"
            cd ./$i
            lsDir
            cd ..
        else
            echo $i
        fi
    done
}

findRecursive()
{
    find . -type d |while read dir
    do
        echo "+++++++++++++++++++++++:$dir"
        cd $dir
        ls
        echo "---------quit---------------"
        echo
        cd -
    done
}

#lsDir
findRecursive
