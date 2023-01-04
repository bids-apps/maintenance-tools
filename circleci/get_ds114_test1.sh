#! /bin/bash

# Get ds114_test1 from OSF
#
# USAGE:
#
# - run:
#     name: Get test data ds114_test1
#     command: |
#       wget https://raw.githubusercontent.com/bids-apps/maintenance-tools/main/circleci/get_ds114_test1.sh
#       bash get_ds114_test1.sh
#

if [[ ! -d "${HOME}/data/ds114_test1" ]]; then
  wget -c -O "${HOME}/ds114_test1.tar" "https://osf.io/download/zerfq/" && \
  mkdir -p "${HOME}/data" && \
  tar xf "${HOME}/ds114_test1.tar" -C "${HOME}/data"
fi
