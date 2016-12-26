#!/usr/bin/env bash
# sets up virtualenv and dependencies for SIS grade parser
# Zach Kirsch | December 2016

# exit if there are any errors
set -e

# create virtualenv
virtualenv venv

# install python dependencies
source venv/bin/activate
pip install -r requirements.txt
deactivate


# install phantomjs dependency
phantomjs_dist=phantomjs-2.1.1-linux-x86_64
phantomjs_zip=${phantomjs_dist}.tar.bz2

wget https://bitbucket.org/ariya/phantomjs/downloads/${phantomjs_zip}
tar -xjf $phantomjs_zip
rm $phantomjs_zip
mv $phantomjs_dist/bin/phantomjs .
rm -r $phantomjs_dist
