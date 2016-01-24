#!/bin/sh
 
function scandir() {
    local cur_dir parent_dir workdir
    workdir=$1
    cd ${workdir}
    if [ ${workdir} = "/" ];then
        cur_dir=""
    else
        cur_dir=`pwd`
    fi
 
    for dirlist in `ls ${cur_dir}`
    do
        if test -d ${dirlist};then
            cd ${dirlist}
            scandir ${cur_dir}/${dirlist} $2
            cd ..
        else
            #echo ${cur_dir}/${dirlist}
            #åèªå·±çå·¥ä½
            local filename=$dirlist
            echo "å½åæä»¶æ¯ï¼"$filename
            #echo ${#2} #.zip 4
            #echo ${filename:(-${#2})}

        	if [[ ${filename:(-${#2})} = $2 ]] 
        	then
        		echo "å é¤æä»¶"$filename
 				rm -f $filename
                echo 
                echo 
 			fi
        fi
    done
}
 
function delete_specified ()
{
    #éåæä»¶å¤¹ãå é¤æå®åç¼åçæä»¶
    #é®é¢ï¼åä¿æ¤çæä»¶å é¤ä¸äº
    #æ³¨é:$1æ¯æå®çæä»¶å¤¹ï¼$2æ¯æå®çåç¼å
    if test -d $1;then
        scandir $1 $2
    elif test -f $1;then
        echo "you input a file but not a directory,pls reinput and try again"
        exit 1
    else
        echo "the Directory isn't exist which you input,pls input a new one!!"
        exit 1
    fi
}

# éåæå®ç®å½ä¸çæå®æ ¼å¼çæä»¶
# ç¸æ¯
function traverse_specified()
{
    for dir in `find $1 -name '$2'`
    do 
        # æåç¶ç®å½
        path=`dirname $dir`
        if [ $path != . ];then
            echo $path
            cd $path
            . clean.sh
            cd -
        fi
    done
}


case "$1" in
    delete)
        delete_specified $2 $3
        ;;
    traverse)
        traverse_specified
        ;;
    *)
        echo "Usage: $0 {delete|traverse}"
        exit 1;
esac
