FROM python:2.7

ENV APP_HOME=/srv/www/django/microweb/

WORKDIR ${APP_HOME}

# The python:2.7 image is based on Debian Buster which is now EOL and its repositories have been moved to the archive, so we need to explicitly enable them:
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    sed -i '/buster-updates/d' /etc/apt/sources.list

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
# RUN ./dependencies.sh

RUN cp microweb/local_settings.py.sample microweb/local_settings.py

ENV PORT=80
EXPOSE ${PORT}
CMD python /usr/local/bin/gunicorn microweb.wsgi -b 0.0.0.0:${PORT}
