#!/usr/bin/env bash
# Author: wxnacy(wxnacy@gmail.com)
# Description:

pyenv virtualenv 3.6.10 wush
pyenv local wush
cp data/pip.conf $VIRTUAL_ENV/pip.conf
pip install pyflakes
pip install pytest
pip uninstall pycrypto
pip uninstall pycryptodome
pip install pycryptodome
pip install w3lib
pip install -r requirements.txt
