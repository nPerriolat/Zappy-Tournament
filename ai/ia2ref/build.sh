#!/bin/bash

if [ -z "$1" ]; then
    echo "Error: The first parameter must be 'ai', 'gui', or 'server'."
    exit 1
fi

if [[ "$1" != "ai" && "$1" != "gui" && "$1" != "server" ]]; then
    echo "Error: The first parameter must be 'ai', 'gui', or 'server'."
    exit 1
fi

TARGET=$1
MAKE_RULE=${2:-}

case $TARGET in
    ai)
        cd zappy_ai
        make "$MAKE_RULE"
        ;;
    gui)
        cd zappy_gui
        make "$MAKE_RULE"
        ;;
    server)
        cd zappy_server
        make "$MAKE_RULE"
        ;;
    *)
        echo "Error: The first parameter must be 'ai', 'gui', or 'server'."
        exit 1
        ;;
esac
