#!/bin/bash

X=30
Y=30
C=5
name="zappy_server_arthur"

if [[ $1 == "debug" ]]; then
    echo "Server debug mode"
    ./$name -p 4242 -x $X -y $Y -n test -c $C -v -f 2 -v
    exit 0
fi

if [[ $1 == "debugfast" ]]; then
    echo "Server debug mode"
    ./$name -p 4242 -x $X -y $Y -n test -c $C -v -f 6 -v
    exit 0
fi

if [[ $1 == "slow" ]]; then
    echo "Server slow mode"
    ./$name -p 4242 -x $X -y $Y -n test -c $C -v -f 42 -v
    exit 0
fi

if [[ $1 == "fast" ]]; then
    echo "Server fast mode"
    ./$name -p 4242 -x $X -y $Y -n test -c $C -v -f 1000 -v
    exit 0
fi

if [[ $1 == "maxfast" ]]; then
    echo "Server recommended fast mode"
    ./$name -p 4242 -x $X -y $Y -n test -c $C -v -f 2000 -v
    exit 0
fi

if [[ $1 == "hyperfast" ]]; then
    echo "Server max frequency mode"
    ./$name -p 4242 -x $X -y $Y -n test -c $C -v -f 10000 -v
    exit 0
fi

./$name -p 4242 -x $X -y $Y -n test -c $C -v
