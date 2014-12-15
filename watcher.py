#! /usr/bin/env python

# Author: Abid H. Mujtaba
# Date: 2014-12-15

# Source: http://www.saltycrane.com/blog/2010/04/monitoring-filesystem-python-and-pyinotify/

# This script uses the pyinotify library which in turn uses the Linux kernel's inotify facility to detect filesystem changes and take appropriate actions.

import pyinotify
import subprocess
import sys
import syslog

from daemon import Daemon


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

# Specify the pid file used to monitor and control the daemon/service.
PID_FILE = "/tmp/watcher.pid"


class MyEventHandler(pyinotify.ProcessEvent):

    def process_IN_CLOSE_NOWRITE(self, event):

        self.on_close("CLOSE_NOWRITE", event.pathname)

    def process_IN_CLOSE_WRITE(self, event):

        self.on_close("CLOSE_WRITE", event.pathname)

    def on_close(self, flag, pathname):

        syslog.syslog("{} - {}".format(flag, pathname))

        subprocess.call([TRIGGERED_SCRIPT])


class WatcherDaemon(Daemon):
    """
    Extends the Daemon class by overriding its run() method which provides the primary functionality provided by the
    service.

    NOTE the loop used in the end.
    """

    def run(self):
        # watch manager
        wm = pyinotify.WatchManager()

        for folder in MONITOR_FOLDERS:

            wm.add_watch(folder, MONITOR_FLAGS, rec=True)

        # event handler
        eh = MyEventHandler()

        # notifier
        notifier = pyinotify.Notifier(wm, eh)
        notifier.loop()


def main():
    """
    This method sets up the daemon and passes the command to it.

    Source: http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
    """

    daemon = WatcherDaemon(PID_FILE, start_msg="Watcher started", stop_msg="Watcher stopped")        # The pid file must be specified so that a running daemon can be accessed

    if len(sys.argv) == 2:

        if 'start' == sys.argv[1]:
                daemon.start()

        elif 'stop' == sys.argv[1]:
                daemon.stop()

        elif 'restart' == sys.argv[1]:
                daemon.restart()

        else:
                print "Unknown command"
                sys.exit(2)

        sys.exit(0)         # We have communicated with the daemon which runs asynchronously so we can exit this script

    else:
        print "Usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)


if __name__ == '__main__':
    main()