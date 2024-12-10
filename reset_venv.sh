#!/usb/bin/env bash

deactivate 2> /dev/null || echo "Non inside a venv"
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt
