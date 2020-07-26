#!/usr/bin/env bash
#
# Commands:
# - build: Builds all the required images.
# - destroy: Stop instance and delete containers. This does not delete the image.
# - run: Run instance by replacing all running containers.
# - status: Check the status of the instance.
#
######################################################################

if [ $1 = "run" ]; then
   export IID=${2? app container ID not supplied}
   echo "Running scoring-service..."
fi

function apprm() {
    local container=$1

    echo "Removing container ${container}..."
    test $(docker ps -a | grep ${container} | wc -l) -ge 1 && docker rm -f ${container}
}

function app() {
    apprm "scoring-service"

    docker run -it \
        --rm \
        --name scoring-service \
        -p 443:443 \
        ${IID}

    echo "Started scoring-service listening to port 443..."
}

function build() {
    make local
}

function run() {
    app
}

function status() {
    docker ps | grep -E "scoring-service"
}

function destroy() {
    apprm "scoring-service"
}

function for_manifest() {
    fun_name=$1
    echo "Running ${fun_name}..."
    $fun_name
}

for_manifest ${1:-status}
