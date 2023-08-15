# Task-notify

Simple solution to run scripts/commands and send notifications via email or webhook (e.g. MS Teams) if it fails. Works great with cron to automate tasks.


Example:
```
$ tasknotify -c ./config.json --only_tasks "Free disk space" "System uptime"
29.01.2023 21:22:41 - INFO: tasknotify 0.8.0
29.01.2023 21:22:41 - INFO: Queueing worker thread for command: Free disk space
29.01.2023 21:22:41 - INFO: Queueing worker thread for command: System uptime
29.01.2023 21:22:41 - WARNING: The command Free disk space failed
29.01.2023 21:22:41 - INFO: Sending email for task: Free disk space
29.01.2023 21:22:41 - INFO: 1 command(s) failed
```

# Installation

  * Install from pypi: ```pip install task-notify```

# Command line arguments

## -v, --version
Show version

## -h, --help
Show help

## -o, --only_tasks
Only run these tasks, chosen by the "name" property.

Example
```
tasknotify --only_tasks "mytask1" "mytask2"
```

## -t, --only_tags
Only run tasks which have at least one of these tags.

Example
```
tasknotify --only_tags "diskcheck" "informational"
```

## -c, --config,
Path to the configuration file to use

Example
```
tasknotify --config ~/myconfig.json
```

## -p, --pretend
Do not run any tasks, only print what would be run.

## -f, --get_default_config

Place a sample configuration file (```config.json```) in the current working directory

## -s, --show

Show actual output of executed tasks in console log.

## -l, --list

Do not run any tasks, just show a list of available tasks.

# Configuration file

tasknotify uses one configuration file to keep all needed information. Optionally, task definitions can also be split into several files and included. Running task-notify with the ```-f``` command line switch places a default ```config.json``` into your current working directory to serve as a starting point.

## hostname

String describing the host where tasknotify runs. This gets included into notification messages to distinguish the messages origin if you run the script on more than one host.

## notify_methods

The methods of notification can be configured and activated here.

### http_post

HTTP POST message.

  * active: Use this notification method
  * webhook_url: URL to HTTP Post the message to. E.g. the MS Teams webhook url.

### mail

EMail message.

  * active: Use this notification method
  * host:     Mail server
  * port:     Port to use
  * starttls: Use StartTTLS
  * user:     Username
  * password: Password
  * mail_from: Sender Email address
  * mail_to:   Receiver EMail address


## tasks_include_dirs

Optional list of directories, which will be included. All files in these directories need to be json-files with task definitions, e.g.

```
{
    "tasks":
    [
        {
            "name:"                 "Get free disk space",
            "cmd":                  "df",
            "timeout_s:             10,
            "args":                 ["-h", "--exclude", "tmpfs"],
            "cwd":                  ".",
            "expected_return_val":  [0],
            "notify_on_return_val": [0],
            "force_notify":         False,
            "tags":                 []
        },
        {
            "name":  "Get host name",
            "cmd":   "uname",
            "args":  ["-a"]
        }
    ]
}

```
Note: Only "name" and "cmd" are mandatory, all other task attributes will be filled with default values if not supplied.


See also the following ```tasks``` section.

## tasks

Task definitions. Essentially, a task is a command with optional arguments which are run like on a local shell.

Every task can have the following properties:

### name:

*mandatory*

Name of the task. Used in notifications to identify the task, must be unique across all task definitions.
### cmd:

*mandatory*

Actual command to run.
### timeout_s:

*default*: None

Timeout in seconds. If the command does not finish/return within this time, the process will be killed and the task will be considered to have failed.
### args:

*default*: []

List of command line arguments.
### cwd:

*default*: "."

Working directory.
### expected_return_val:

*default*: [0]

List of expected return value(s) for this task. If the actual return value does not match one of these values, then the task will be considered failed and a notification will be send.
### force_notify:

*default*: False

ALWAYS send a notification about this task, regardless of the return value. The return value will still be used to check if the task has failed (thus resulting in another notification message).
### notify_on_return_val

*default*: []

List of return values which will lead to sending a notification about this task. The return value will still be used to check if the task has failed (thus resulting in another notification message).

### tags:

*default*: []

List of tags for this task.

# Licensing

Licensed under the MIT license, see also LICENSE.txt
