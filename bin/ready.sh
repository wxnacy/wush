#!/usr/bin/env bash
# Author: wxnacy(wxnacy@gmail.com)
# Description:

pyenv virtualenv 3.6.10 wush
pyenv local wush
cp data/pip.conf $VIRTUAL_ENV/pip.conf
pip install -r requirements.txt
