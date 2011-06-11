#!/bin/sh

WORKON_HOME=/home/wilblack
PROJECT_ROOT=/home/wilblack/social

# activate virtual environment
. $WORKON_HOME/pinaxenv/bin/activate

cd $PROJECT_ROOT
#date >> $PROJECT_ROOT/logs/cron_pics.log
python manage.py send_mail >> $PROJECT_ROOT/logs/cron_mail.log 2>&1
python manage.py emit_notices >> $PROJECT_ROOT/logs/cron_mail.log 2>&1