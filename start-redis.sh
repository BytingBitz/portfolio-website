#!/bin/sh
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo 1 > /proc/sys/vm/overcommit_memory
exec docker-entrypoint.sh redis-server "$@"