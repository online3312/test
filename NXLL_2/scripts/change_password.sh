#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo Usage: $0 [username] [newpass]
    exit 2
fi
user=$1
pass=$2
hashpass="$(printf '%s' "$pass" | sha256sum | cut -f1 -d' ')"
awk -v user=$user -v pass=$hashpass -f ~/cnc/scripts/cpw.awk ~/cnc/db.txt > tmp && mv -f tmp ~/cnc/db.txt

