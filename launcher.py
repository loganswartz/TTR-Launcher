#!/usr/bin/env python3

import os
import time
import json
import platform

import requests
import sys

system = platform.system()
snap = False

if system == "Darwin":
    GAME = f"/Users/{os.getlogin()}/Library/Application Support/Toontown Rewritten/Toontown Rewritten"
    DYLD_LIBRARY_PATH = f"/Users/{os.getlogin()}/Library/Application Support/Toontown Rewritten/Libraries.bundle"
    DYLD_FRAMEWORK_PATH = f"/Users/{os.getlogin()}/Library/Application Support/Toontown Rewritten/Frameworks"
    CONFIG_DIRECTORY = os.path.expanduser("~/.config/ttrlauncher/")
elif system == "Linux":
    if snap == True:
        GAME = f"/home/{os.getlogin()}/snap/toontown/common/toontown-rewritten/TTREngine"
    else:
        GAME = "/usr/share/toontown-rewritten/TTREngine"
    DYLD_LIBRARY_PATH = ""
    DYLD_FRAMEWORK_PATH = ""
    CONFIG_DIRECTORY = os.path.expanduser("~/.config/ttrlauncher/")

URL = "https://www.toontownrewritten.com/api/login?format=json"

if not os.path.exists(CONFIG_DIRECTORY):
    os.makedirs(CONFIG_DIRECTORY)

if not os.path.exists(CONFIG_DIRECTORY + 'config.json'):
    with open(CONFIG_DIRECTORY + 'config.json', 'w') as f:
        f.write(json.dumps([]))
    with open(CONFIG_DIRECTORY + 'config.json.example', 'w') as f:
        f.write(json.dumps([['username', 'password', 'nickname']]))

ACCOUNTS = json.load(open(CONFIG_DIRECTORY + 'config.json', 'r'))


def die(reason):
    print(reason)
    exit(1)

def get_nickname(account):
    if len(account) < 3:
        return account[0]
    else:
        return account[2]

def select_account():
    if not len(ACCOUNTS):
        die(f'Error: You need to open {CONFIG_DIRECTORY + "config.json"} and add some accounts! See config.json.example for examples.')

    if len(sys.argv) > 1 and sys.argv[1] in ACCOUNTS.keys():
        return ACCOUNTS[sys.argv[1]]

    while True:
        if len(ACCOUNTS) == 1:
            print(f"Only 1 account found; Using {get_nickname(ACCOUNTS[0])}")
            account = 0
        else:
            print("Available accounts:")
            for index, acc in enumerate(ACCOUNTS):
                print(f"    [ {index} ] {get_nickname(acc)}")

            account = int(input('Which account? '))

        if account <= len(ACCOUNTS):
            return ACCOUNTS[account]
        else:
            print("Invalid account, try again.")


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
        os.system('cd "{}" && DYLD_LIBRARY_PATH="{}" DYLD_FRAMEWORK_PATH="{}" "{}"'.format(
            os.path.dirname(GAME), DYLD_LIBRARY_PATH, DYLD_FRAMEWORK_PATH, GAME
        ))
        exit(0)
    else:
        die('Somehow we got here, not sure how ...')


login(select_account())

