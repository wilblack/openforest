#!/bin/sh
chown -R www-data /home/wilblack/android/
chmod -R 775 /home/wilblack/android

WORKON_HOME=/home/wilblack
PROJECT_ROOT=/home/wilblack/social

# activate virtual environment
. $WORKON_HOME/pinaxenv/bin/activate


cd $PROJECT_ROOT
#date >> $PROJECT_ROOT/logs/cron_pics.log
python manage.py load_pics >> $PROJECT_ROOT/logs/cron_pics.log 2>&1