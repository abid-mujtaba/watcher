# Watcher

This utility consists of a script that uses pyinotify to detect CLOSE events in the specified folders and responds by running the specified script.

The configuration for the utility must reside in a script named *config.py* in the same folder as *watcher.py* (since it is fetched using *from config impot ...*.

In *config.py* you need only two variables:

```python
MONITOR_FOLDERS = [<list of full paths of folders (as strings) which are to be watched for the CLOSE event>]

TRIGGERED_SCRIPT = "<full path of script to run when event is detected>"
```

If you want to detect events other than CLOSE simply modify the MONITOR_FLAGS variable in *watcher.py*.


## Installation

A Makefile has been provided to allow you to install, start and stop the service. This implementation uses *upstart* to turn the script in to service. The service runs as a user job so root access is not needed.

To install the service :

```bash
make install
```

Once installed one can use standard *upstart* commands to control the service such as:

```bash
start watcher
stop watcher
restart watcher
```


## Logs

When the service is started a log is added to syslog. All other output from both the watcher script and the triggered script appears in the *upstart* logging location which is usuall *$HOME/.cache/upstart/watcher.log*

## Debug

To debug the utility simply run the *watcher.py* script from the terminal (like a normal python script). All output and error messages will be shown on the terminal. To exit the script simply press *Ctrl+C*.
