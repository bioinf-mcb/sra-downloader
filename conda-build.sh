#!/bin/bash

# change the package name to the existing PyPi package you would like to build and adjust the Python versions
pkg='sra-downloader'
array=( 3.7 3.8 )

echo "Building conda package ..."
# building conda packages
for i in "${array[@]}"
do
	conda-build --python $i $pkg
done

# convert package to other platforms
cd ~
platforms=( osx-arm64 osx-64 linux-32 linux-64 win-32 win-64 )
find $CONDA_PREFIX/conda-bld/linux-64/ -name *.tar.bz2 | while read file
do
    echo $file
    #conda convert --platform all $file  -o $CONDA_PREFIX/conda-bld/
    for platform in "${platforms[@]}"
    do
       conda convert --platform $platform $file  -o $CONDA_PREFIX/conda-bld/ --dependencies 'sra-tools >=2.9.6'
    done
    
done

# upload packages to conda
find $CONDA_PREFIX/conda-bld/ -name *.tar.bz2 | while read file
do
    echo $file
    anaconda upload --user bioinf-mcb $file
done

echo "Building conda package done!"