#!/bin/bash

# All Python dependencies are pure Python (no C extensions), so the only
# system requirement is Python 3.12+ (3.14 recommended) and a local memcached
# for the site/CNAME cache.

if [[ "$OSTYPE" == "linux-gnu" ]]; then
	sudo apt-get -y install python3 python3-venv memcached
elif [[ "$OSTYPE" == "darwin"* ]]; then
	brew install python memcached
else
	echo -e "${COL_RED}This script only works on Linux and OSX $COL_RESET"
	exit 1
fi

python3 -m venv ENV
source ENV/bin/activate
pip install -r requirements.txt
deactivate
