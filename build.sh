#!/bin/bash -xe
pipenv install --dev
pipenv run pyinstaller -n standup-notes --add-data 'standup.template:standup.template' -F standup_notes/__main__.py
sudo cp -i dist/standup-notes /usr/local/bin
