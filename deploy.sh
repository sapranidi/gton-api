#!/usr/bin/bash

docker build -t gton-api .
docker run -itd --name gton-api -p 6000:8001 gton-api