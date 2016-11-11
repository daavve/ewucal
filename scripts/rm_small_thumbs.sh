#! /bin/bash
#
#  Removes all the thumbnails.
#  Kosuke does not like the quality loss involved
#
##################################################

dirs=$(ls -d */)
 for dir in $dirs ; do
  cd $dir
  rm -f *.thumb.*
  cd ..
done
  