#!/bin/env bash
#
# This file is part of 3l34n0r (Eleanor - A bot)
#
# Copyright (C) 2017 Chiayo Lin <chiayo.lin@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import the init functions
source /lib/lsb/init-functions

# General user-define configuration
DAEMON_USER="ubuntu"
DAEMON_NAME="eleanor"
SCRIPT_FILE="server.py"
SCRIPT_ARGS="--noauth_local_webserver"
SCRIPT_REPO="$HOME/3l34n0r/eleanor/"

# Path configuration
SCRIPT_PATH="$SCRIPT_REPO$SCRIPT_FILE"
PIDFLE_PATH="/var/run/$DAEMON_NAME.pid"

# Run $SCRIPT_PATH as a system daemon
_start_daemon () {
  log_daemon_msg "Starting $DAEMON_NAME daemon"
  start-stop-daemon --start                \
                    --background           \
                    --pidfile $PIDFLE_PATH \
                    --make-pidfile         \
                    --user    $DAEMON_USER \
                    --chuid   $DAEMON_USER \
                    --startas $SCRIPT_PATH \
                    --$ARGS                \

  log_end_msg $?
}

# Stop the daemon we started
_stop_daemon () {
  log_daemon_msg "Stopping $DAEMON_NAME daemon"
  start-stop-daemon --stop                 \
                    --pidfile $PIDFLE_PATH \
                    --retry 10             \

  log_end_msg $?
}

# Main
main () {
  case "$1" in
    start|stop)
      _${1}_daemon || exit $?
      ;;
    restart|reload|force-reload)
      _stop_daemon && _start_daemon || exit $?
      ;;
    status)
      status_of_proc "$DAEMON_NAME" "$SCRIPT_PATH" && exit 0 || exit $?
      ;;
    *)
      echo "Usage: $(pwd)/$DAEMON_NAME [start|stop|restart|status]"
  esac
}

# Run with the last argument
main "${@: -1}" || exit $?
