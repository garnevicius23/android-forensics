#!/bin/bash
DIRECTORY=$(cd '/mnt' && pwd)

echo find: 'mmssms.db' on $DIRECTORY
find $DIRECTORY . -type f -exec grep -sl "mmsms.db"  {} \;