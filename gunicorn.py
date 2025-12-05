# Gunicorn Configuration for Django HRMS

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 5

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Load application code before the worker processes are forked
preload_app = True

# The granularity of Error log outputs
loglevel = "info"

# Logging
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
accesslog = "-"
errorlog = "-"

# Process naming
proc_name = "django_hrms"

# PID file
pidfile = "/tmp/gunicorn.pid"

# User and group to run as
user = "www-data"
group = "www-data"

# Temp directory
tmp_upload_dir = None

# SSL (if using HTTPS)
keyfile = None
certfile = None

# Environment variables
raw_env = [
    "DJANGO_SETTINGS_MODULE=hrms.settings",
]

# Django settings module
django_settings = os.environ.get("DJANGO_SETTINGS_MODULE", "hrms.settings")

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Python WSGI application path
wsgi_app = None

# Pass additional arguments to the WSGI application
args = None

# DAEMON configuration (uncomment to daemonize)
# daemon = True
# pidfile = "/tmp/gunicorn.pid"
# logfile = "/var/log/gunicorn.log"

# Redirect stdout/stderr to a log file
# capture_output = True

# Preload application
preload_app = True

# Worker temporary directory
worker_tmp_dir = "/dev/shm"

# Hooks
def on_starting(server):
    server.log.info("Starting Django HRMS server...")

def on_reload(server):
    server.log.info("Reloading Django HRMS server...")

def on_shutdown(server):
    server.log.info("Shutting down Django HRMS server...")

def on_exit(server):
    server.log.info("Django HRMS server has exited.")

def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Django HRMS server is ready. Spawning workers")

def worker_abort(worker):
    worker.log.info("Worker received SIGABRT signal")