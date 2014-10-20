#!/bin/bash
cd /home/pi/notipi
git fetch origin
git checkout master
VAR=$(git log HEAD..origin/master --oneline)
if [[ $VAR ]]; then
    git pull origin master
    supervisorctl restart notipi
fi
