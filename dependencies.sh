#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu" ]]; then
	sudo apt-get install python2
	curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
	sudo python2 get-pip.py
	rm get-pip.py
	sudo apt-get -y install build-essential fabric libevent-dev libmemcached-dev python2.7-dev python2-dev zlib1g-dev
	sudo pip install virtualenv
elif [[ "$OSTYPE" == "darwin"* ]]; then
	brew install libmemcached
	brew install python
	pip install fabric
	pip install virtualenv
else
	echo -e "${COL_RED}This script only works on Linux and OSX $COL_RESET"
	exit 1
fi

virtualenv ENV
source ENV/bin/activate
ORIGPATH=$PATH
export PATH=$PWD/ENV/bin:$PATH
pip install -r requirements.txt
deactivate
export PATH=$ORIGPATH
