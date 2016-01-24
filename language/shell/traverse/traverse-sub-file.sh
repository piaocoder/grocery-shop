#!/bin/sh
# åè½:
#       éåå½åç®å½ä¸é¢çææå­ç®å½
#       å¹¶æ§è¡ç¸åºçæä½

# éå½å½æ°
lsDir()
{
    for i in `ls`;do
        if [ -d $i ];then
            echo "ç®å½:$i"
            cd ./$i
            # ./clean.shè°ç¨shellæä»¶
            lsDir
            cd ..
        else
            echo $i
        fi
    done
}

# find éå
findRecursive()
{
    find . -type d |while read dir
    do
        echo "è¿å¥å­ç®å½:$dir"
        cd $dir
        ls
        echo "---------quit---------------"
        echo
        cd -
    done
}

#lsDir
findRecursive
