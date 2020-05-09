#!/bin/bash

# Ask for root permissions
if [ $EUID != 0 ]; then
            sudo "$0" "$@"
            exit $?
fi

# Attach image to loop device
#echo "Please, specify working directory where image is stored: "

working_dir="$1"

if [ -z "$working_dir" ]
then
    read -p  "Please, specify working directory where image is stored: "  working_dir
fi

if [ -d $working_dir ]
then
    cd $working_dir
    losetup -f -P "$working_dir/img/blk0.img"
else
    echo "Please, make sure that such directory exists."
    exit 1
fi

# Timeout till image will be fully attached
sleep 2

# List of valid 'loops'
mapfile -t loops_list < <( lsblk -f | grep -v "NAME" | awk '{print $1, $2}' | grep loop | sed s'/[├─└─]//g')

for (( i = 0; i<${#loops_list[@]}; i++))
do
    if [[ ${loops_list[$i]} == *"ext"* ]]; then

        IFS=' ' read -r -a loop_details <<< "${loops_list[$i]}"

        loop_name=${loop_details[0]}
        loop_fs=${loop_details[1]}

        mkdir /mnt/$loop_name

        mount -t $loop_fs /dev/$loop_name /mnt/$loop_name

        echo $loop_name - " was mounted successfuly."
    fi
done