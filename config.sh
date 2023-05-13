#!/bin/zsh
if [ ! -d 'venv' ]
then
    echo 'creating venv'
    python -m venv venv
fi

echo 'activating venv'
source venv/bin/activate

echo 'update latest pip'
pip install --upgrade pip