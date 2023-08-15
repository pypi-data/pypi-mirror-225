#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import logging
import argparse
import json
import subprocess
import concurrent.futures
import smtplib
import shutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib import request

# ---- Argument parser ----
def GetVersion() -> str:
    return "0.8.3"

def GetArgParser() -> argparse.ArgumentParser:
    tArgParser = argparse.ArgumentParser(usage="%(prog)s [OPTIONS]",
                                         description="Run scripts/commands and send notifications.")

    tArgParser.add_argument("-v", "--version", action="version", version = f"{tArgParser.prog} version {GetVersion()}")
    tArgParser.add_argument("-o", "--only_tasks", nargs='+', default = [], help="Run only these tasks")
    tArgParser.add_argument("-t", "--only_tags", nargs='+', default = [], help="Run only tasks which have this tag")
    tArgParser.add_argument("-c", "--config", help="Path to configuration file", type=str, default="./config.json", required=False)
    tArgParser.add_argument("-p", "--pretend",  help="Do not run any tasks, just output what would be run.", action="store_true")
    tArgParser.add_argument("-f", "--get_default_config", help="Copy a sample configuration file to the current directory and exit", action="store_true")
    tArgParser.add_argument("-s", "--show", help="Show actual output of executed tasks", action="store_true")
    tArgParser.add_argument("-l", "--list", help="Do not run any tasks, just show a list of available tasks.", action="store_true")
    return tArgParser

# -- Logger setup ---
def setuplogging():
    # Set application wide debug level and format
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S',
                        level=logging.INFO)

# -- Configuration file --
class cAppConfig:
    cmdtemplate = { "name": "",
                    "cmd": "",
                    "args": [],
                    "cwd": ".",
                    "expected_return_val": [0],
                    "force_notify": False,
                    "notify_on_return_val": [],
                    "tags": [],
                    "timeout_s": None}
    def __init__(self, a_sFilename = ""):
        self.http_post = {}
        self.mail = {}
        self.tasks = []
        self.hostname = ""
        if a_sFilename: self.Read(a_sFilename)

    def GetFileList(self,
                    a_tDirList):
        files = []
        for current_dir in a_tDirList:
            if os.path.isdir(current_dir):
                for entry in os.scandir(current_dir):
                    if entry.is_file(): files.append(entry.path)
        return files

    def ReadTasks(self,
                  a_tConfigfile,
                  a_tOnlyTasks,
                  a_tOnlyTags):

        for i in a_tConfigfile["tasks"]:
            if not "name" in i: raise KeyError("Missing 'name' in task definition")
            if not "cmd"  in i: raise KeyError("Missing 'cmd' in task definition")
            newcmd = {}
            newcmd.update(cAppConfig.cmdtemplate)
            newcmd.update(i)
            # names must be unique
            for j in self.tasks:
                if j["name"] == newcmd["name"]: raise KeyError(f'Duplicate command names are not allowed (\"{j["name"]}\")')
            # check whether to really include the task based on name and tags
            bKeepTask = False
            bKeepTag = False
            if (a_tOnlyTasks and (newcmd["name"] in a_tOnlyTasks)) or (not a_tOnlyTasks): bKeepTask = True
            if a_tOnlyTags:
                for i in newcmd["tags"]:
                    if i in a_tOnlyTags:
                        bKeepTag = True
                        break
            else: bKeepTag = True
            if (bKeepTask and bKeepTag): self.tasks.append(newcmd)

    def Read(self,
             a_sFilename: str,
             a_tOnlyTasks = None,
             a_tOnlyTags = None):
        self.mail = { "active": False, "host": "", "port": 465, "starttls": False, "user": "", "password" : "", "mail_from": "", "mail_to": ""}
        self.http_post = {"active": False, "webhook_url": "blah" }
        self.tasks = []
        try:
            with open(a_sFilename, "r") as f:
                configfile = json.load(f)

            if "hostname" in configfile:
                self.hostname = configfile["hostname"]
            else: raise KeyError(f"\"hostname\" key not found in {a_sFilename}")

            if not "notify_methods" in configfile: raise KeyError(f"\"notify_methods\" key not found in {a_sFilename}")

            if "http_post" in configfile["notify_methods"]:
                self.http_post.update(configfile["notify_methods"]["http_post"])
            else: raise KeyError(f"\"http_post\" key not found in {a_sFilename}")

            if "mail" in configfile["notify_methods"]:
                self.mail.update(configfile["notify_methods"]["mail"])
            else: raise KeyError(f"\"mail\" key not found in {a_sFilename}")

            if "tasks_include_dirs" in configfile:
                dirs = configfile["tasks_include_dirs"]
                if not type(dirs) is list:
                    raise ValueError(f"\"tasks_include_dirs\" in {a_sFilename} should be a list")
                else:
                    files = self.GetFileList(dirs)
                    for i in files:
                        try:
                            with open (i, "r") as tf:
                                tasksfile = json.load(tf)
                                if "tasks" in tasksfile:
                                    self.ReadTasks(tasksfile, a_tOnlyTasks, a_tOnlyTags)
                        except Exception as e:
                            self.mail = {}
                            self.tasks = []
                            raise Exception(f"While reading included tasks file {i}: " + str(e)) from e

            if "tasks" in configfile:
                self.ReadTasks(configfile, a_tOnlyTasks, a_tOnlyTags)
            else: raise KeyError(f"\"tasks\" key not found in {a_sFilename}")

        except Exception as e:
            self.mail = {}
            self.tasks = []
            raise

# --- List tasks ---
def list_tasks(a_tConfig):
    print('   List of tasks follows:')
    for i in a_tConfig.tasks:
        print(f'   {i["name"]} (Tags: {i["tags"]})')
    return True

# --- Http post with json payload ----

class http_post:
    def __init__(self, a_sURL):
        self.sURL = a_sURL
    def send(self, a_sMsg):
        post = request.Request(url=self.sURL, method="POST")
        post.add_header(key="Content-Type", val="application/json")
        with request.urlopen(url = post, data = json.dumps({"text": a_sMsg}).encode() ) as response:
            if response.status != 200:
                raise Exception(response.reason)

# --- Simple Email sender ----
class mail:
    def __init__(self,
                 a_sServer,
                 a_sUser,
                 a_sPassword,
                 a_nPort,
                 a_bStarttls = False):
        self.sServer = a_sServer
        self.sUser = a_sUser
        self.sPassword = a_sPassword
        self.nPort = a_nPort
        self.bStarttls = a_bStarttls
        self.sHtmlFormatStart = '<html><body><pre>'
        self.sHtmlFormatEnd = '</pre></body></html>'

    def formatmessage(self, a_sMailAddrFrom, a_sMailAddrTo, a_sMsg, a_sSubject):
        message = MIMEMultipart("alternative")
        message["Subject"] = a_sSubject
        message["From"] = a_sMailAddrFrom
        message["To"] = a_sMailAddrTo
        message.attach(MIMEText(a_sMsg, "plain"))
        message.attach(MIMEText(f'{self.sHtmlFormatStart}{a_sMsg}{self.sHtmlFormatEnd}', "html"))
        return message.as_string()

    def send(self, a_sMailAddrFrom, a_sMailAddrTo, a_sMsg, a_sSubject):
        try:
            if self.bStarttls:
                with smtplib.SMTP(host = self.sServer, port = self.nPort) as mailer:
                    mailer.starttls()
                    mailer.login(user = self.sUser, password = self.sPassword)
                    mailer.sendmail(from_addr = a_sMailAddrFrom,
                                    to_addrs = a_sMailAddrTo,
                                    msg = self.formatmessage(a_sMailAddrFrom, a_sMailAddrTo, a_sMsg, a_sSubject))
            else:
                with smtplib.SMTP_SSL(host = self.sServer, port = self.nPort) as mailer:
                    mailer.login(user = self.sUser, password = self.sPassword)
                    mailer.sendmail(from_addr = a_sMailAddrFrom,
                                    to_addrs = a_sMailAddrTo,
                                    msg = self.formatmessage(a_sMailAddrFrom, a_sMailAddrTo, a_sMsg, a_sSubject))
        except Exception as e:
            raise

# --- Notifications ---
def notify(a_tConfig, a_tReturnValues = None):
    numfailed = 0
    notifications = []

    for i in a_tReturnValues:
        if i["failed"]:
            numfailed+=1
            logging.warning(f'The command {i["name"]} failed')
        if i["failed"] or i["force_notify"] or (i["return_value"] in i["notify_on_return_val"]): notifications.append(i)

    # send email notifications
    if a_tConfig.mail["active"] and notifications:
        try:
            mailer = mail(a_tConfig.mail["host"],
                          a_tConfig.mail["user"],
                          a_tConfig.mail["password"],
                          a_tConfig.mail["port"],
                          a_tConfig.mail["starttls"])
            for i in notifications:
                logging.info(f'Sending email for task: {i["name"]}')
                if i["failed"]: subject = f'Failed task \"{i["name"]}\" on host {a_tConfig.hostname}'
                else          : subject = f'Completed task \"{i["name"]}\" on host {a_tConfig.hostname}'
                message = f'Task: {i["name"]}\nReturn value: {i["return_value"]} (expected values: {i["expected_return_val"]})'
                if i['stdout']: message += f'\n\nOutput:\n{i["stdout"]}'
                if i['stderr']: message += f'\n\nError output:\n{i["stderr"]}'
                mailer.send(a_tConfig.mail["mail_from"], a_tConfig.mail["mail_to"], message, subject)
        except Exception as e:
            logging.error(f'Mail failed: {e}')
            raise

    # send http_post notifications to server, e.g. teams webhook
    if a_tConfig.http_post["active"] and notifications:
        try:
            poster = http_post(a_tConfig.http_post["webhook_url"])
            for i in notifications:
                logging.info(f'Sending http post for task: {i["name"]}')
                if i["failed"]: subject = f'<h1>Failed task \"{i["name"]}\" on host {a_tConfig.hostname}</h1>'
                else          : subject = f'<h1>Completed task \"{i["name"]}\" on host {a_tConfig.hostname}</h1>'
                message = f'Task: {i["name"]}<br>Return value: {i["return_value"]} (expected values: {i["expected_return_val"]})'
                if i['stdout']: message += f'<br><br>Output:<br><pre>{i["stdout"]}</pre>'
                if i['stderr']: message += f'<br><br>Error output:<br><pre>{i["stderr"]}</pre>'
                poster.send(subject + message)
        except Exception as e:
            logging.error(f'Http post failed: {e}')
            raise

    logging.info(f'{numfailed} command(s) failed')

# --- Sample configuration ---
def deploy_sample_config():
    # If requested: deploy sample configuration file to the current working directory and exit
    config_src = os.path.dirname(os.path.realpath(__file__)) + "/config.json"
    try:
        shutil.copy(config_src, os.getcwd())
    except Exception as e:
        logging.error(f"Error deploying sample configuration: {str(e)}")
        return 1
    logging.info(f"Deployed sample configuration file to {os.getcwd()}")
    return 0

# --- Command executor function ---
def run_cmd(a_tCmdParams, a_bPretend = False):
    # TODO: add timeout
    ret = {"failed": True, "return_value": 0, "stdout": "", "stderr": "" }
    ret.update(a_tCmdParams) # Add original parameters to return a complete dataset
    try:
        cmdstring = ' '.join([a_tCmdParams["cmd"]] + a_tCmdParams["args"])
        if a_bPretend:
            ret["failed"] = False
            logging.info(f"   Pretending to run command: \"{cmdstring}\" in \"{a_tCmdParams['cwd']}\"")
        else:
            completed = subprocess.run(cmdstring,
                                       cwd = a_tCmdParams["cwd"],
                                       timeout = a_tCmdParams["timeout_s"],
                                       capture_output = True,
                                       shell = True)
            ret["return_value"] = completed.returncode
            ret["stdout"]       = completed.stdout.decode('utf-8', errors = "replace")
            ret["stderr"]       = completed.stderr.decode('utf-8', errors = "replace")
            if completed.returncode in a_tCmdParams["expected_return_val"]: ret["failed"] = False
            else:                                                           ret["failed"] = True
    except Exception as e:
        ret["failed"] = True
        ret["return_value"] = 1
        ret["stdout"] = ""
        ret["stderr"] = str(e)
    return ret

# --- Show output ---
def show_output(taskinfo: list = None):
    logging.info("Task output follows")
    for i in taskinfo:
        print(f"---\nTask: {i['name']} (return value: {i['return_value']})\nstdout:\n{i['stdout']}\nstderr:\n{i['stderr']}\n")

# --- main routine ----
def run_program():
    # setup logging
    setuplogging()
    logging.info(f"task-notify {GetVersion()}")

    # read in command line arguments
    parser = GetArgParser()
    targs = parser.parse_args()

    # If requested: deploy sample configuration file to the current working directory and exit
    if targs.get_default_config:
        return deploy_sample_config()

    # read in configuration
    try:
        tAppConfig = cAppConfig()
        tAppConfig.Read(targs.config,
                        targs.only_tasks,
                        targs.only_tags)
    except Exception as e:
        logging.error(f"Could not read configuration: {e}")
        return 1

    # If requested: show list of tasks and exit
    if targs.list:
        return list_tasks(tAppConfig)

    # run commands in worker threads
    returnfutures = []
    returnvalues = []
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in tAppConfig.tasks:
                logging.info (f"Queueing worker thread for command: {i['name']}")
                returnfutures.append(executor.submit(run_cmd, i, targs.pretend))
    except Exception as e:
        logging.error (f"Worker thread failed: {e}")
        return 1
    # collect return values
    for i in returnfutures: returnvalues.append(i.result())

    # Send notifications for all failed commands or commands with force_notify = True
    try:
        notify(tAppConfig, returnvalues)
    except Exception as e:
        logging.error (f"Sending notification failed: {e}")
        return 1

    # Print task output to console, useful for local testing
    if targs.show:
        show_output(returnvalues)

if __name__ == '__main__':
    sys.exit(run_program())
