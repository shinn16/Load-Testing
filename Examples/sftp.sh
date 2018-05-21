#!/usr/bin/env bash
cd ../
NEWEST=$( ls -Art Output | tail -n 2 )
echo "$NEWEST"
for i in $NEWEST
do
    echo "put ./Output/\"$i\""
done