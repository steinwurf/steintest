#!/bin/sh
tmux
git pull 
kill $(lsof -t -i:8080)
go run main.go
tmux detach
