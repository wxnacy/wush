#!/usr/bin/env bash
# Author: wxnacy(wxnacy@gmail.com)
# Description:

# poetry shell

name=$1

nohup wush server --config tests/data/config/config.yml &

pytest $name -vs --cov --cov-report=html

