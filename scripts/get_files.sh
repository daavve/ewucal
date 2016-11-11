#! /bin/bash
#
# Gets the files in file-list.txt
#
#####################################################################

BASE_URL="http://www.cadal.zju.edu.cn/CalliSources/images/characterimage/00000000/"
declare -i num
let "num = 0"

myFiles=$(cat file-list.txt)

for file in $myFiles; do
    let "num++"
    let "modulo = $num % 4"
    if [[ $modulo == 0 ]]; then
        filePath=$BASE_URL$file
        if [[ ! -a $file ]]; then
            wget -t 0 $filePath
        fi
    fi
done
