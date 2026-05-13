#!/bin/bash

cd ~/docker-status || exit

git pull origin main

docker compose down
docker compose up -d --build

