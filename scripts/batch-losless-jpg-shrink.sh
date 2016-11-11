 #! /bin/bash
 #
 # Use jpegtran to loslessly compress jpeg files by optimizing entropy
 #
 #########################################################################################################################################
 
 
 dirs=$(ls -d */)
 for dir in $dirs ; do
  cd $dir
  jpgFiles=$(ls *.jpg)
  for file in $jpgFiles ; do
    echo $file
    jpegtran -o -outfile $file"-s" $file 
    mv -f $file"-s" $file
 done
 cd ../
 
 done
