#! /bin/bash

# used to build the Docker image for a project in circle CI
#
#  assumes that the docker has been cached in ${HOME}/docker/image.tar
#
# - save_cache:
#     key: my_cache
#     paths:
#     - ~/docker
#     - ~/data
#

if [[ -e "${HOME}/docker/image.tar" ]]; then
    docker load -i "${HOME}/docker/image.tar"
fi
git describe --tags --always > version
docker build -t "bids/${CIRCLE_PROJECT_REPONAME,,}" .
mkdir -p "${HOME}/docker"
docker save "bids/${CIRCLE_PROJECT_REPONAME,,}" > "${HOME}/docker/image.tar"
