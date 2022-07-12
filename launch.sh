#!/bin/bash

script_path=$(dirname $(readlink -f $0))
cd $script_path

conda init bash
conda activate pealcan

python3 sniff.py --canbus
