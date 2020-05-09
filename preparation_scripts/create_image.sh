#!/bin/bash

echo "*** About to create disk image..."

working_dir="$1"

if [ -d $working_dir ]
then
    cd $working_dir
else
    echo "Please, make sure that such directory exists."
    exit 1
fi

# Attached device list
mapfile -t devices_list < <( adb devices | grep -v "List"  | awk '{print $1}' | grep -v -e '^$')

if [ ${#device_list[@]} -eq 0 ]
then 
    echo "Zero devices are connected."
    exit 1;
fi

echo "List of availabe devices: "

for (( i = 0; i<${#devices_list[@]}; i++))
do
    echo $i". " ${devices_list[$i]}
done

read -p "Enter device number of which you want to create image: " device_number

if [ "$device_number" -ge  "${#devices_list[@]}" ]
then
    echo "No such device."
    exit 1
fi

mkdir img
cd "$working_dir/img"

# Create image of device inside external storage
echo "Creating disk image..."
adb -s ${devices_list[$device_number]} shell 'su busybox dd if=/dev/block/mmcblk0 of=/storage/0123-4567/blk0.img bs=4096'

echo "Downloading image from phone to local storage... "
adb -s ${devices_list[$device_number]} pull /storage/0123-4567/blk0.img

./mount_image.sh $working_dir