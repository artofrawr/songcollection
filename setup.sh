#!/bin/bash

# SETUP VIRTUAL ENVIRONMENT
cd virtualenv
virtualenv songcollection
source songcollection/bin/activate
cd ..

# INSTALL DEPENDENCIES
pip install -r REQUIREMENTS
