SERVER="../eleanor/server.py"
ARGS="--noauth_local_webserver"
RUN="python3"


PROCESS="$RUN $SERVER $ARGS"


function find_process

PROCESSCOUNT=$(ps -ef |grep -v grep |grep -cw <daemon process name>

if [$PROCESSCOUNT -eq 0]
then
  mailx -s "daemon process not running" myaddress@mydomain <msg body

fi

# double fork to detach from the current TTY
($RUN $SERVER $ARGS </dev/null >/dev/null 2>/dev/null &) &
exit 0
