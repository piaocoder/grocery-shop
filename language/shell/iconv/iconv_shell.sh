#!/bin/bash

echo "$#"
if [ "$#" != "2" ];then
    echo "Usage: `basename $0` dir filter"
    exit
fi

show_file() {
    dir = $1
    filter = $2
    echo "$1"
    for file in `find $dir -name "$2"`; do
        echo "$file"
        if [ -d $dif/$file ];then
            show_file $file $2
        else
            iconv -f latin1 -t utf8 -o $file $file
        fi
    done
}

show_file $1 $2
