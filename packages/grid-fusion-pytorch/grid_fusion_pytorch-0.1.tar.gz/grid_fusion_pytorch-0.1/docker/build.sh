#!/usr/bin/env bash

# Check args
if [ "$#" -ne 0 ]; then
  echo "usage: ./build.sh"
  return 1
fi

# Build the docker image
docker build\
  --build-arg user=$USER\
  --build-arg uid=$UID\
  -t grid_fusion_pytorch\
  -f Dockerfile .
