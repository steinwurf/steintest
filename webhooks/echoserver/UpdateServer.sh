#!/bin/sh
tmux
git pull 
kill $(lsof -t -i:8080)
sh genstartServer.sh
tmux detach
