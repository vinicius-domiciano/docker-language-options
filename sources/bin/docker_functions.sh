#!/bin/bash
__create_image_from_docker_file_function__() {
    docker build -t "$1" -f $2 .
}

__download_image_from_docker_file_function__() {
    docker pull $1
}