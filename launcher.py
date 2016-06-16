#!/usr/bin/env python3

import os
import time

import requests

GAME = "/Users/{}/Library/Application Support/Toontown Rewritten/Toontown Rewritten".format(os.getlogin())
DYLD_LIBRARY_PATH = "/Users/{}/Library/Application Support/Toontown Rewritten/Libraries.bundle".format(os.getlogin())
DYLD_FRAMEWORK_PATH = "/Users/{}/Library/Application Support/Toontown Rewritten/Frameworks".format(os.getlogin())


URL = "https://www.toontownrewritten.com/api/login?format=json"

ACCOUNTS = {}


def select_account():
    while True:
        print("Available accounts: {}".format(", ".join(ACCOUNTS.keys())))
        account = input('Which account? ')
        if account in ACCOUNTS.keys():
            return ACCOUNTS[account]
        print("Invalid account, try again.")


def die(reason):
    print(reason)
    exit(1)

def finish_partial_auth(r):
    while True:
        print(r['banner'])
        code = input("Code: ")
        r = requests.post(URL, data={'appToken': code, 'responseToken': r['responseToken']}).json()

        if r['success']:
            return r


def finish_queue(r):
    queueToken = r['queueToken']
    while True:
        print(r)
        print("Currently waiting in queue... Position: {}, ETA: {} seconds".format(r['position'], r['eta']))
        time.sleep(1)
        r = requests.post(URL, data={'queueToken': queueToken}).json()
        if r['success'] == "true":
            return r
        time.sleep(29)


def login(account):
    r = requests.post(URL, data={'username': account[0], 'password': account[1]}).json()

    if r['success'] == "false":
        die("Unable to login: {}".format(r['banner']))
    elif r['success'] == "partial":
        r = finish_partial_auth(r)

    if r['success'] == "delayed":
        r = finish_queue(r)
        print(r)

    if r['success'] == "true":
        os.environ['TTR_GAMESERVER'] = r['gameserver']
        os.environ['TTR_PLAYCOOKIE'] = r['cookie']
        os.system('DYLD_LIBRARY_PATH="{}" DYLD_FRAMEWORK_PATH="{}" "{}"'.format(DYLD_LIBRARY_PATH, DYLD_FRAMEWORK_PATH, GAME))
        exit(0)
    else:
        die('Somehow we got here, not sure how ...')


login(select_account())