#!/bin/sh
/usr/bin/telegraf --config telegraf.conf --test
# check $?
/usr/bin/telegraf --config telegraf.conf --pidfile /tmp/telegraf.pid &
