#!/bin/bash

# CREATE CONFIG FILE
echo "Please enter your last.fm API KEY:"
read apikey
echo "api_key: \"${apikey}\"" > config.yml

# SETUP VIRTUAL ENVIRONMENT
cd virtualenv
virtualenv songcollection
source songcollection/bin/activate
cd ..

# INSTALL DEPENDENCIES
pip install -r REQUIREMENTS
