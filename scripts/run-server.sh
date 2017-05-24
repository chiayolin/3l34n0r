#!/bin/bash

BINDIR="$HOME/3l34n0r/eleanor/"
SERVER="$BINDIR/server.py"
S_ARGS="--noauth_local_webserver"
S_NAME="Eleanor"
S_USER="ubuntu"
PIDFLE="/var/run/$S_NAME.pid"

. /lib/lsb/init-functions

_start () {
  log_daemon_msg "Starting $S_NAME daemon"
  start-stop-daemon --start --background --pidfile $PIDFLE        \
                    --make-pidfile --user $S_USER --chuid $S_USER \
                    --startas $SERVER -- $ARGS
  log_end_msg $?
}

_stop () {
  log_daemon_msg "Stopping system $S_NAME daemon"
  start-stop-daemon --stop --pidfile $PIDFLE --retry 10
  log_end_msg $?
}

case "$1" in
  start|stop)
    _${1}
    ;;

  restart|reload|force-reload)
    _stop
    _start
    ;;

  status)
    status_of_proc "$S_NAME" "$SERVER" && exit 0 || exit $?
    ;;
  
  *)
    echo "Usage: /etc/init.d/$S_NAME {start|stop|restart|status}"
    exit 1
    ;;
esac

exit 0
