#!/bin/bash

echo "Compiling..."
if [ `ls ./burp | grep ".class" | wc -l` -ne "0" ]
then
rm burp/*.class
fi

TEMP="`javac burp/* 2>&1`"
if [ `echo $TEMP | wc -c` -eq "1" ]
then
echo "Compile Successful"
else
echo "Compile Failed"
echo $TEMP
exit 1
fi

echo "Creating extension.jar..."
jar cf extension.jar burp/* assets/*
echo "Finished!"
