#!/bin/bash

working_dir="$1"
echo "$working_dir"

if [ -z "$working_dir" ]
then
    read -p  "Please, specify working directory where image is stored: "  working_dir
fi

if [ ! -d $working_dir ]
then
    echo "Please, make sure that such directory exists."
    exit 1
fi

mkdir -p "$working_dir/pictures" "$working_dir/telephony"

DIRECTORY=$(cd '/mnt' && pwd)

echo find: 'mmssms.db' on $DIRECTORY
sms_dest=$(find $DIRECTORY -name "mmssms.db")
calllog_dest=$(find $DIRECTORY -name "calllog.db")

cp "$sms_dest" "$working_dir/telephony"
cp "$calllog_dest" "$working_dir/telephony"

echo "Searching for pictures destination..."
pictures_dest=$(find $DIRECTORY -name "DCIM")

for pic in "$pictures_dest/"; do
    cp -r "$pic" "$working_dir/pictures"
done

mkdir -p "$working_dir/report"
python3 ../analyze/report.py $working_dir
