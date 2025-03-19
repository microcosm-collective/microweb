# Dokku server setup

## Create server

* make a server (on Linode)
  * needs at least 2GB RAM for the build step or it crashes out (with code 137 - OOM)

## Create users

Create all users as appropriate, e.g.

```bash
# create users
adduser madwort
# add sudo
usermod -aG sudo madwort
# add ssh key
sudo su - madwort
ssh-import-id gh:madwort
```

## Install Dokku

based on https://dokku.com/docs/getting-started/installation/

```bash
# for debian systems, installs Dokku via apt-get
wget -NP . https://dokku.com/install/v0.35.16/bootstrap.sh
sudo DOKKU_TAG=v0.35.16 bash bootstrap.sh

# add a key
cat id_rsa.pub | dokku ssh-keys:add admin

# install dokku-memcached plugin
sudo dokku plugin:install https://github.com/dokku/dokku-memcached.git --name memcached
dokku memcached:create microweb-memcached
```

## Create microweb app

Create the app on the server:

```bash
dokku apps:create microweb
```

Push to the app from your local git repository:

```bash
git remote add dokku dokku@lfgssdemo:microweb
git push dokku main
# nb. if you're pushing a wip branch!
git push dokku madwort/working-docker:main
```

Configure some things on the server:

```bash
dokku ports:add microweb http:80:5000
dokku domains:add microweb lfgss.com
dokku domains:add microweb www.lfgss.com
dokku domains:add microweb *.microcosm.app

dokku config:set --no-restart microweb DJANGO_SETTINGS_MODULE=microweb.settings
dokku config:set --no-restart microweb PYTHONPATH=.
dokku config:set --no-restart microweb MEMCACHE_HOST=dokku-memcached-microweb-memcached
dokku config:set --no-restart microweb CLIENT_SECRET=123456
dokku config:set --no-restart microweb SECRET_KEY=aoeui12345
```

Add some CloudFlare / nginx configuration for the app

```bash
mkdir /home/dokku/microweb/nginx.conf.d/
```

Copy this block into a file at `/home/dokku/microweb/nginx.conf.d/cloudflare.conf`:

```
  # Cloudflare
  set_real_ip_from 103.21.244.0/22;
  set_real_ip_from 103.22.200.0/22;
  set_real_ip_from 103.31.4.0/22;
  set_real_ip_from 104.16.0.0/12;
  set_real_ip_from 108.162.192.0/18;
  set_real_ip_from 141.101.64.0/18;
  set_real_ip_from 162.158.0.0/15;
  set_real_ip_from 172.64.0.0/13;
  set_real_ip_from 173.245.48.0/20;
  set_real_ip_from 188.114.96.0/20;
  set_real_ip_from 190.93.240.0/20;
  set_real_ip_from 197.234.240.0/22;
  set_real_ip_from 198.41.128.0/17;
  set_real_ip_from 199.27.128.0/21;
  set_real_ip_from 2400:cb00::/32;
  set_real_ip_from 2405:8100::/32;
  set_real_ip_from 2405:b500::/32;
  set_real_ip_from 2606:4700::/32;
  set_real_ip_from 2803:f800::/32;
  real_ip_header CF-Connecting-IP;
```

Then ensure file permissions are correct & reload nginx.

```bash
chown dokku:dokku /home/dokku/microweb/nginx.conf.d/cloudflare.conf
service nginx reload
```

Finally restart the app on the server to pick up all the changes:

```bash
# restart
dokku ps:restart microweb
```

And maybe check the logs for errors as the requests roll in!

```bash
# check the logs
dokku logs microweb
```

If you need to restart memcached, you can use:

```bash
dokku memcached:restart microcosm-memcached
```
