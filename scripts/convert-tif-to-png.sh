#! /bin/bash
#
#  converts all tiffs to pngs and optimizes them
#
##################################################

declare -i length

dirs=$(ls -d */)
 for dir in $dirs ; do
  cd $dir
  tifFiles=$(ls *.tif)
  for file in $tifFiles ; do
    length=${#file}-3
    pngFile=${file:0:$length}"png"
    convert $file $pngFile
    optipng -o1 $pngFile
    rm -f $file 
  done
  cd ..
done
