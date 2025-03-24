FROM python:2.7

ENV APP_HOME=/srv/www/django/microweb/


WORKDIR ${APP_HOME}

RUN apt-get -qq update && \
    apt-get -yq install --no-install-recommends \
    build-essential \
    libevent-dev \
    libmemcached-dev \
    zlib1g-dev && \
    apt-get -yq --purge autoremove && \
    apt-get -q clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /${APP_HOME}

RUN python -m pip install --upgrade pip \
    && pip install virtualenv \
    && pip install -r requirements.txt

COPY . /${APP_HOME}

RUN cp microweb/local_settings.py.production microweb/local_settings.py

# add dummy user
RUN useradd -Ms /bin/bash -u1100 microweb
USER microweb

ENV PORT=80
EXPOSE ${PORT}
CMD python /usr/local/bin/gunicorn microweb.wsgi -b 0.0.0.0:${PORT}
