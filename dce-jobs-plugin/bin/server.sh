#!/bin/sh

cat <<EOF > /etc/supervisord.conf
[supervisord]
nodaemon=true

[program:nginx]
command=nginx -g "daemon off;" -c /etc/nginx/jobs/server-nginx.conf
autorestart=true
startsecs=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0

[program:jobs-server]
directory=/usr/src/app/jobs
command=gunicorn --preload -k sync -w 1 --max-requests 50000 --max-requests-jitter 8080 --access-logfile - --error-logfile - -b 0.0.0.0:8080 app:app
autorestart=true
startsecs=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
EOF

exec /usr/bin/supervisord
