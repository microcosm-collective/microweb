#!/bin/bash
set -e

# logfile and location
LOGFILE=/var/log/django/microweb.log
LOGDIR=$(dirname $LOGFILE)

# number of gunicorn workers
NUM_WORKERS=5
HOST='127.0.0.1:8000'

# user/group to run as
USER=django
GROUP=microcosm

# activate virtualenv
source /srv/www/django/microwebenv/bin/activate

cd /srv/www/django/microweb
test -d $LOGDIR || mkdir -p $LOGDIR

exec /srv/www/django/microwebenv/bin/gunicorn_django -b $HOST \
  -w $NUM_WORKERS -k gevent --user=$USER --group=$GROUP --log-level=info \
  --max-requests 1000 --log-file=$LOGFILE 2>>$LOGFILE
