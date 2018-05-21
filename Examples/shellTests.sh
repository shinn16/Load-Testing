#!/usr/bin/env bash
max=10
for (( i=$1; i > 0; --i ))
do
    echo "$i..."
    sleep 1
done