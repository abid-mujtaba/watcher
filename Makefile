# Author: Abid H. Mujtaba
# Date: 2014-12-15
#
# This Makefile contains the commands for installing, starting and stopping the watcher service.

.PHONY: install, start, stop

install:
#			Installation involves copying the the upstart configuration file to the location for user session upstart jobs.
#			Then we reload the initd configuration
#
	cp watcher.conf ~/.config/upstart/watcher.conf

start:
#			upstart command for launching the watcher service defined by ~/.config/upstart/watcher.conf
	start watcher

stop:
	stop watcher
