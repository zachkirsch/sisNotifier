#!/usr/bin/env bash

# Checks if grades have been updated on SIS and sends and email if so
# Zach Kirsch | December 2016

# Argument 1: SIS username
# Argument 2: file containing SIS password
# Argument 2: email to contact if the grades have been changed

username="$1"
password="$2"
email="$3"

# files for comparing old grades with new grades
old=".grades.txt"
new=".new_grades.txt"

if [[ -f "$old" ]] ; then
        already_exists=true
fi
touch $old $new

# run grade parser, put output in $new
source venv/bin/activate
python parseGrades.py "$username" "$password" > $new
python_exit=$?
deactivate
pkill -u $USER phantomjs

if [ $python_exit -ne 0 ]; then # python error
        exit 1
fi

# print grades to screen
cat $new

# check for updates
diff $old $new > /dev/null

if [ $? -ne 0 ]; then # if diff had ouptut
        if [[ "$already_exists" = true ]]; then
                mail -s "Grades updated" $email < $new
        fi
        echo "*** Grades updated ***"
fi

mv $new $old
