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
# RUN ./dependencies.sh

# These two files are necessary to render the site properly, but they are
# not included in the repo due to .gitignore exclusions:
ADD https://www.lfgss.com/static/js/bootstrap.min.js ${APP_HOME}core/static/js/
ADD https://www.lfgss.com/static/themes/1/css/bootstrap.min.css ${APP_HOME}core/static/themes/1/css

RUN [ ! -f microweb/local_settings.py ] && echo "Missing config. Using default. Should be fine." && cp microweb/local_settings.py.sample microweb/local_settings.py

ENV PORT=80
EXPOSE ${PORT}
CMD python /usr/local/bin/gunicorn_django -b 0.0.0.0:${PORT}
