# Author: Abid H. Mujtaba
# Date: 2014-12-15
#
# This Makefile contains the commands for installing, starting and stopping the watcher service.

DIR="/home/abid/scripts/python/watcher"

.PHONY: install, start, stop

install:
#			Installation involves creating a symbolic link for the upstart (initd) configuration file.
#			Then we reload the initd configuration
#
	sudo ln -s $(DIR)/watcher.conf /etc/init/watcher.conf
	sudo initctl reload-configuration

start:
#			upstart command for launching the watcher service defined by /etc/init/watcher.conf
	sudo start watcher

stop:
	sudo stop watcher
