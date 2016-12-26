#!/usr/bin/env bash

# runs a process every 10 minutes until an epoch
# Zach Kirsch | December 2016

# argument 1:  expiration (epoch time)
# argument 2:  script to run
# argument 3+: arguments to be passed to script

# check arguments
if [[ $# -lt 2 ]]; then
        echo "Wrong number of arguments."
        echo "Usage: $0 <expiration epoch> <script> [args]"
        exit 1
fi

# get expiration
expiration="$1"
shift

while [[ $(date +'%s') -lt $expiration ]]; do
        "${@}"
        sleep 600
done
