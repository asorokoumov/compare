web: gunicorn compare.wsgi --log-file -
web: python compare/manage.py collectstatic --noinput; bin/gunicorn_django --workers=4 --bind=0.0.0.0:$PORT compare/settings.py