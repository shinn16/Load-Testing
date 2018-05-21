#!/usr/bin/env bash
NEWEST=$( ls -Art ../Output | tail -n 1 )  # gets the newest file in the dire
echo $NEWEST