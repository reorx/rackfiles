#!/usr/bin/env bash

curl https://raw.githubusercontent.com/reorx/rackfiles/master/rackfiles.py -o /tmp/rackfiles.py && \
    chmod +x /tmp/rackfiles.py && \
    sudo mv /tmp/rackfiles.py /usr/local/bin/rackfiles
