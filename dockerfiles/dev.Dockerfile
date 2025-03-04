FROM python:3.4

ENV APP_HOME /srv/www/django/microweb/


WORKDIR ${APP_HOME}

COPY sources-stretch.list /etc/apt/sources.list

RUN apt-get update

RUN apt-get -qq update && \
    apt-get -yq install --no-install-recommends \
        build-essential \
        fabric \
        libevent-dev \
        libmemcached-dev \
        zlib1g-dev && \
    apt-get -yq --purge autoremove && \
    apt-get -q clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /${APP_HOME}

RUN pip install -r requirements.txt

COPY . /${APP_HOME}
# RUN ./dependencies.sh

# These two files are necessary to render the site properly, but they are
# not included in the repo due to .gitignore exclusions:
ADD https://www.lfgss.com/static/js/bootstrap.min.js ${APP_HOME}core/static/js/
ADD https://www.lfgss.com/static/themes/1/css/bootstrap.min.css ${APP_HOME}core/static/themes/1/css

RUN cp microweb/local_settings.py.sample microweb/local_settings.py

ENV PORT 80
EXPOSE ${PORT}
CMD python ./ENV/bin/gunicorn_django -b 0.0.0.0:${PORT}
