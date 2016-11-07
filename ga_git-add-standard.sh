#!/usr/bin/bash
#
# Adds the stuff from usually changed folders.  Also performs a commit and push with message
#
#
#############################################################################################################

j=true
message="'"

for i in "$@"; do
    if [[ j -eq 'true'  ]]; then
        message="$message$i"
        j=false
    else
        message="$message $i"
    fi

done

message="$message'"

echo $message

git add calligraphy/migrations/*.py
git add calligraphy/*.py
git add calligraphy/templates/calligraphy/*.html
git add static/css/*.css
git add static/js/*.js

git commit -m $message
git push -v
