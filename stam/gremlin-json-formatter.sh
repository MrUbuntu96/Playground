#!/bin/bash

filename=$1
if [ -z $1 ]; then
    printf "\n\tError: missing filename\n\n"
    exit 1
fi

nlines="$(wc -l $filename | cut -f 1 -d ' ')"

awk -v nlines=$nlines '
    NR == 1      { print "[" $0 "," }
    NR > 1 && NR < nlines  { print $0 "," }
    NR == nlines { print $0 "]" }
' $filename

# Another way
#r=`wc -l $filename`  # run the command
#a=(${r})             # split into an array
#nlines=${a[0]}       # extract first element
