wsgi_app = "sy_low_value.wsgi"
bind = ["0.0.0.0:8540"]
workers = 16
worker_class = "gevent"
# default 1000. The maximum number of simultaneous clients.
# This setting only affects the Eventlet and Gevent worker types.
# worker_connections = 1000
threads = 2

# logging
# accesslog = '-'  # '-' means log to stdout.
# errorlog = '-'
# Access log - records incoming HTTP requests
accesslog = "/var/log/sy-low-value/gunicorn.access.log"
# Error log - records Gunicorn server goings-on
errorlog = "/var/log/sy-low-value/gunicorn.error.log"
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
loglevel = "info"
capture_output = True  # Redirect stdout/stderr to specified file in errorlog.
