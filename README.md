# Rackfiles

A thin wrapper around Rackspace's `rack` cli, makes file operations much easier.

## Installation

    bash <(curl -s https://raw.githubusercontent.com/reorx/rackfiles/master/get-rackfiles.sh)

## Usage

1. List containers

        rackfiles -l

2. List files

        rackfiles -c CONTAINER -l

3. Upload a file

        rackfiles -c CONTAINER -u FILE

4. Download a file

        rackfiles -c CONTAINER -d FILE

5. Delete a file

        rackfiles -c CONTAINER -D FILE
