#!/bin/bash

video=$1
fps=$2

reset="\033[0m"
magenta="\033[35m"
green="\033[0;32m"
red="\033[0;31m"

color_echo() {
    local color=$1
    local msg=$2
    echo -e "$color$2$reset"
}

execute_and_handle_error() {
    local start=$SECONDS
    "$@"
    local status=$?
    local duration=$((SECONDS - start))
    local minutes=$((duration / 60))
    local seconds=$((duration % 60))
    if [$status -ne 0]; then
        color_echo $red "Error - Execution failed - '$*'"
    else
        color_echo $magenta "Execution time: ${minutes} min ${seconds} sec."
    fi
}

v2i() {
    local vid=$1
    local fps=$2
    python src/v2i.py $vid --fps $fps
}

i2p() {
    vid=$1
    python src/i2p.py $vid 
}

p2g() {
    vid=$1
    python src/p2g.py $vid 
}

echo $PATH

color_echo $magenta "Turning video $video into frames"
execute_and_handle_error v2i $diveo $fps
color_echo $magenta "Turning frames into pixelated frames"
execute_and_handle_error i2p $video
color_echo $magenta "Turning pixelated frames into gif"
execute_and_handle_error p2g $video

color_echo $green "Success"