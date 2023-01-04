#! /bin/bash

# used to push the Docker image for a project in circle CI
#
# USAGE:
#
# - run:
#     name: push docker image
#     command: |
#       wget https://raw.githubusercontent.com/bids-apps/maintenance-tools/main/circleci/push_docker.sh
#       bash push_docker.sh
#

if [[ -n "$DOCKER_PASS" ]]; then

    # make sure we have a lowercase repo name
    repo_name=$(echo "${CIRCLE_PROJECT_REPONAME}" | tr '[:upper:]' '[:lower:]')

    echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin

    echo "Pushing to DockerHub bids/${repo_name}:unstable"
    docker tag "bids/${repo_name}" "bids/${repo_name}:unstable"
    docker push "bids/${repo_name}:unstable"

    if [[ -n "${CIRCLE_TAG}" ]]; then
        echo "Pushing to DockerHub bids/${repo_name}:${CIRCLE_TAG}"
        docker push "bids/${repo_name}:latest"
        docker tag "bids/${repo_name}" "bids/${repo_name}:${CIRCLE_TAG}"
        docker push "bids/${repo_name}:${CIRCLE_TAG}"
    fi

else
    echo "No DOCKER_PASS, skipping push to DockerHub"

fi
