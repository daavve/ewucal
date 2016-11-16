#! /bin/bash
#
#  shrinks all the new jpeg thumbs
#
##################################################

dirs=$(ls -d */)
 for dir in $dirs ; do
  cd $dir
  jpgFiles=$(ls *thumb.jpg)
  for file in $jpgFiles ; do
    echo $file
    jpegtran -o -outfile $file"-s" $file 
    mv -f $file"-s" $file
 done
  cd ..
done
