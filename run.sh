#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <docker_image_name> [optional_commands]"
    exit 1
fi

image_name="$1"
optional_arg="${@:2}"

# Check if the Docker image exists
if ! docker image inspect "$image_name" &> /dev/null; then
    echo Docker "$image_name" not found. Building...
    docker build -t "$image_name" .
fi

# Run the Docker container
echo run -t -v $PWD/automation:/app/automation --rm $image_name $optional_arg

docker run -t -v $PWD/automation:/app/automation --rm $image_name $optional_arg