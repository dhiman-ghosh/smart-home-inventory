#!/bin/bash

PORT=80

if [ $# -ne 0 ]; then
  if [ $1 = "-h" ] || [ $1 = "--help" ]; then
    echo "Usage: ./start.sh [port]"
    exit 0
  else
    PORT=$1
  fi
fi

sudo service firewalld stop
sudo gunicorn sinventory.server:app -b 192.168.1.11:$PORT
