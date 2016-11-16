#! /bin/bash
#
#  optipng's all the characters to see if it shrinks them
#
##################################################

dirs=$(ls -d */)
 for dir in $dirs ; do
  cd $dir
  pngFiles=$(ls *hi-rez.png)
  for file in $pngFiles ; do
    optipng -o1 $file 
  done
  cd ..
done
