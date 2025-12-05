release: python manage.py migrate --noinput
web: gunicorn hrms.wsgi --log-file -
worker: python manage.py process_tasks