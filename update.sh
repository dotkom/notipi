#!/bin/bash
cd /home/pi/notipi
git fetch origin
git checkout production
VAR=$(git log HEAD..origin/production --oneline)
if [[ $VAR ]]; then
    git pull origin production
    supervisorctl restart notipi
fi
