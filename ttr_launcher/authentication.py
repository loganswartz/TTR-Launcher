#!/usr/bin/env python3

# Imports {{{
# builtins
import logging
import sys
import time

# 3rd party modules
import requests

# local modules
from ttr_launcher.constants import LOGIN_URL

# }}}


log = logging.getLogger(__name__)


def login(credentials):
    resp = requests.post(
        LOGIN_URL,
        data={"username": credentials["username"], "password": credentials["password"]},
    ).json()

    if resp["success"] == "false":
        log.error(f"Unable to login: {resp['banner']}")
        sys.exit(1)
    elif resp["success"] == "partial":
        resp = finish_partial_auth(resp)

    if resp["success"] == "delayed":
        resp = finish_queue(resp)

    if resp["success"] == "true":
        # print(json.dumps(r, indent=4))
        return resp
    else:
        print("Somehow we got here, not sure how....")
        sys.exit(1)


def finish_partial_auth(resp):
    while True:
        print(resp["banner"])
        code = input("Code: ")
        resp = requests.post(
            LOGIN_URL, data={"appToken": code, "responseToken": resp["responseToken"]}
        ).json()

        if resp["success"]:
            return resp


def finish_queue(resp):
    queueToken = resp["queueToken"]
    while True:
        print(
            f"Currently waiting in queue... Position: {resp['position']}, ETA: {resp['eta']} seconds"
        )
        time.sleep(1)
        resp = requests.post(LOGIN_URL, data={"queueToken": queueToken}).json()
        if resp["success"] == "true":
            return resp
        time.sleep(29)
