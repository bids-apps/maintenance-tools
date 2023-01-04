#! /bin/bash

# Get ds114_test2 from OSF
# 
# USAGE:
# 
# - run:
#     name: Get test data ds114_test2
#     command: |
#       wget https://raw.githubusercontent.com/bids-apps/maintenance-tools/main/circleci/get_ds114_test2.sh
#       bash get_ds114_test2.sh 
# 

if [[ ! -d "${HOME}/data/ds114_test2" ]]; then
  wget -c -O "${HOME}/ds114_test2.tar" "https://osf.io/download/eg4ma/" && \
  mkdir -p "${HOME}/data" && \
  tar xf "${HOME}/ds114_test2.tar" -C "${HOME}/data"
fi
