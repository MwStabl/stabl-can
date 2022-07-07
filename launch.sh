#!/bin/bash

script_path=$(dirname $(readlink -f $0))
cd $script_path

source venv/bin/activate
jupyter lab
