#!/usr/bin/bash
#
# Adds the stuff from usually changed folders.  Also performs a commit and push with message
#
#
#############################################################################################################


git add calligraphy/migrations/*.py
git add calligraphy/*.py
git add calligraphy/templates/calligraphy/*.html
git add static/css/*.css
git add static/js/*.js

git commit -m $2
git push -v
