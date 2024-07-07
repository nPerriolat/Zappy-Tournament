#!/bin/bash

tmux new-session -s "Server" -d "./start_server.sh"
tmux new-session -s "GUI" -d "./start_gui.sh"
# tmux new-session -s "AI" -d "./start_ai.sh"

./start_ai.sh
echo DEAD
sleep 5
