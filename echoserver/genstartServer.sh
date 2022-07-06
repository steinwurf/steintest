#!/bin/bash
LOGFILE="server_file.log"
LAUNCH="main.go"

while :
do
    echo "New launch at `date`" >> "${LOGFILE}"
    go run main.go
    wait
done