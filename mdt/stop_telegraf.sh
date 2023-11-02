#!/bin/sh

[ -f /tmp/telegraf.pid ] && kill `cat /tmp/telegraf.pid`
