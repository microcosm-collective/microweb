FROM python:3.14-slim

ENV APP_HOME=/srv/www/django/microweb/

WORKDIR ${APP_HOME}

COPY requirements.txt /${APP_HOME}

RUN python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /${APP_HOME}

RUN cp microweb/local_settings.py.production microweb/local_settings.py

# add dummy user
RUN useradd -Ms /bin/bash -u1100 microweb

RUN mkdir -p /srv/www/django/static/ \
    && python manage.py collectstatic --noinput --settings=microweb.settings \
    && chown -R microweb:microweb /srv/www/django/static/

# switch to the unprivileged user to run gunicorn
USER microweb

ENV PORT=80
EXPOSE ${PORT}
# gthread workers: 4 processes x 8 threads = 32 concurrent requests per
# container. Each worker process owns one shared ThreadPoolExecutor
# (core/api/fetch.py) for concurrent API calls.
CMD python /usr/local/bin/gunicorn microweb.wsgi -b 0.0.0.0:${PORT} \
    --forwarded-allow-ips '*' \
    --worker-class gthread --workers 4 --threads 8 --max-requests 1000
