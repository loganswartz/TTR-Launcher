#!/usr/bin/env python3

# builtins
import time

# 3rd party modules
import json
import requests
from launcher import LOGIN_URL

def login(credentials):
    r = requests.post(LOGIN_URL, data={'username': credentials['username'], 'password': credentials['password']}).json()

    if r['success'] == "false":
        die(f"Unable to login: {r['banner']}")
    elif r['success'] == "partial":
        r = finish_partial_auth(r)

    if r['success'] == "delayed":
        r = finish_queue(r)

    if r['success'] == "true":
        #print(json.dumps(r, indent=4))
        return r
    else:
        print('Somehow we got here, not sure how ...')
        exit(1)


def finish_partial_auth(r):
    while True:
        print(r['banner'])
        code = input("Code: ")
        r = requests.post(LOGIN_URL, data={'appToken': code, 'responseToken': r['responseToken']}).json()

        if r['success']:
            return r


def finish_queue(r):
    queueToken = r['queueToken']
    while True:
        print(f"Currently waiting in queue... Position: {r['position']}, ETA: {r['eta']} seconds")
        time.sleep(1)
        r = requests.post(LOGIN_URL, data={'queueToken': queueToken}).json()
        if r['success'] == "true":
            return r
        time.sleep(29)

