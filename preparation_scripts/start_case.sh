#!/bin/bash

read -p "Enter case id: " -r case_no

if [ -z "$case_no" ]
then
    echo "Case id cannot be empty."
    exit 1
fi

read -p "Specify path where case should be created: " -r working_dir

if [ -d $working_dir ]
then

    if [ -d "$working_dir/case-$case_no" ]
    then
        echo "Such case already exists in specified path."
        exit 1
    else
        mkdir "$working_dir/case-$case_no"
        ./create_image.sh $working_dir/case-$case_no
    fi
    
else
    echo "Please, make sure that such directory exists."
    exit 1
fi