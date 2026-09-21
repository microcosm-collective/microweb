FROM python:3.14-slim

ENV APP_HOME=/srv/www/django/microweb/

WORKDIR ${APP_HOME}

COPY requirements.txt /${APP_HOME}

RUN python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /${APP_HOME}

RUN cp microweb/local_settings.py.sample microweb/local_settings.py

ENV PORT=80
EXPOSE ${PORT}
CMD python /usr/local/bin/gunicorn microweb.wsgi -b 0.0.0.0:${PORT} --worker-class gthread --threads 8
