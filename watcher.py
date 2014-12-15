#! /usr/bin/env python

# Author: Abid H. Mujtaba
# Date: 2014-12-15

# Source: http://www.saltycrane.com/blog/2010/04/monitoring-filesystem-python-and-pyinotify/

# This script uses the pyinotify library which in turn uses the Linux kernel's inotify facility to detect filesystem changes and take appropriate actions.

import pyinotify
import signal
import subprocess
import sys
import syslog


# Import the flags that we will use to monitor events in the specified folder
IN_CLOSE_WRITE = pyinotify.EventsCodes.FLAG_COLLECTIONS['OP_FLAGS']['IN_CLOSE_WRITE']
IN_CLOSE_NOWRITE = pyinotify.EventsCodes.FLAG_COLLECTIONS['OP_FLAGS']['IN_CLOSE_NOWRITE']

# Perform a bitwise OR operation to construct a combined set of flags
MONITOR_FLAGS = IN_CLOSE_WRITE | IN_CLOSE_NOWRITE

# We specify the folders that need to be monitored
MONITOR_FOLDERS = ['/home/abid/Documents/workspace/.misc',
                   '/home/abid/Pictures/.Personal']

# We specify the shell script that has to be run when the specified flags are triggered in the specified folders
TRIGGERED_SCRIPT = "/home/abid/bin/sanitize_recent_docs"


class MyEventHandler(pyinotify.ProcessEvent):

    def process_IN_CLOSE_NOWRITE(self, event):

        self.on_close("CLOSE_NOWRITE", event.pathname)

    def process_IN_CLOSE_WRITE(self, event):

        self.on_close("CLOSE_WRITE", event.pathname)

    def on_close(self, flag, pathname):

        subprocess.call([TRIGGERED_SCRIPT])


def signal_term_handler(signal, frame):

    syslog.syslog("Watcher Terminated")
    sys.exit(0)


def main():

    syslog.syslog("Watcher Started")
    signal.signal(signal.SIGTERM, signal_term_handler)      # Attach handler for SIGTERM so we can log the shutdown

    # watch manager
    wm = pyinotify.WatchManager()

    for folder in MONITOR_FOLDERS:

        wm.add_watch(folder, MONITOR_FLAGS, rec=True)

    # event handler
    eh = MyEventHandler()

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()


if __name__ == '__main__':
    main()