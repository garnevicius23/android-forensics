#!/bin/bash

# List of valid 'loops'
mapfile -t loops_list < <( lsblk -f | grep -v "NAME" | awk '{print $1, $2}' | grep loop | sed s'/[├─└─]//g')

for (( i = 0; i<${#loops_list[@]}; i++))
do
    
    if [[ ${loops_list[$i]} == *"ext"* ]]; then

        IFS=' ' read -r -a loop_details <<< "${loops_list[$i]}"

        loop_name=${loop_details[0]}

        if [ $EUID != 0 ]; then
            sudo "$0" "$@"
            exit $?
        fi

        umount /dev/$loop_name
        rmdir /mnt/$loop_name

        echo $loop_name + " was unmounted successfuly."
    fi
done

losetup -d /dev/${loops_list[0]}