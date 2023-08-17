#!/bin/bash

keyword=$1
pids=$(ps -ef | grep $keyword | awk '{print $2}')

for pid in $pids; do
  if ps -p $pid > /dev/null; then
    kill -9 $pid
  fi
done