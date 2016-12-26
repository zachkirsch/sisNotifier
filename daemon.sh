#!/usr/bin/env bash

# runs a process every 10 minutes until an epoch
# Zach Kirsch | December 2016

# argument 1:  expiration (epoch time)
# argument 2+: command to run (plus any arguments)

# example: sh daemon.sh 1483574400 touch hi.txt

# check arguments
if [[ $# -lt 2 ]]; then
        echo "Wrong number of arguments."
        echo "Usage: $0 <expiration epoch> <command> [args]"
        exit 1
fi

# get expiration
expiration="$1"
shift

while [[ $(date +'%s') -lt $expiration ]]; do
        "${@}"
        sleep 600
done
