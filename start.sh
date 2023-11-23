#!/usr/bin/env bash
nginx -g 'daemon off;' &
uwsgi --ini uwsgi.ini