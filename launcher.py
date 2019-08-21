#!/usr/bin/env python3

# builtins
import os
import time
import json
from getpass import getpass
import subprocess
import sys

# 3rd party modules
import requests


system = sys.platform.toLower()

if system == "darwin":
    GAME = f"/Users/{os.getlogin()}/Library/Application Support/Toontown Rewritten/Toontown Rewritten"
    GAME = f"/Users/{os.getlogin()}/Library/Application Support/Toontown Rewritten/"
    DYLD_LIBRARY_PATH = f"/Users/{os.getlogin()}/Library/Application Support/Toontown Rewritten/Libraries.bundle"
    DYLD_FRAMEWORK_PATH = f"/Users/{os.getlogin()}/Library/Application Support/Toontown Rewritten/Frameworks"
    CONFIG_DIRECTORY = os.path.expanduser("~/.config/ttrlauncher/")
elif system == "linux":
    # if using the TTR snap package
    if os.path.isdir('/snap/toontown/current/'):
        GAME = f"/home/{os.getlogin()}/snap/toontown/common/toontown-rewritten/TTREngine"
        GAME_DIR = f"/home/{os.getlogin()}/snap/toontown/common/toontown-rewritten/"
    else:
        GAME = "/usr/share/toontown-rewritten/TTREngine"
        GAME_DIR = "/usr/share/toontown-rewritten/"
    DYLD_LIBRARY_PATH = "test"
    DYLD_FRAMEWORK_PATH = "test2"
    CONFIG_DIRECTORY = os.path.expanduser("~/.config/ttrlauncher/")

URL = "https://www.toontownrewritten.com/api/login?format=json"

if not os.path.exists(CONFIG_DIRECTORY):
    os.makedirs(CONFIG_DIRECTORY)

if not os.path.exists(CONFIG_DIRECTORY + 'config.json'):
    with open(CONFIG_DIRECTORY + 'config.json', 'w') as f:
        f.write(json.dumps([]))
    with open(CONFIG_DIRECTORY + 'config.json.example', 'w') as f:
        f.write(json.dumps([{'username': '', 'password':'', 'nickname':''}]))

ACCOUNTS = json.load(open(CONFIG_DIRECTORY + 'config.json', 'r'))


def die(reason):
    print(reason)
    exit(1)

def get_nickname(account):
    if 'nickname' in account:
        return f"{account['nickname']} ({account['username']})"
    else:
        return account['username']

def get_account_index(name: str):
    indexed_accounts = []
    for index, account in enumerate(ACCOUNTS):
        if 'nickname' in account:
            indexed_accounts.append({'names': [account['username'], account['nickname']], 'index': index})
        else:
            indexed_accounts.append({'names': [account['username']], 'index': index})

    # find the account with the given username/nickname
    for account in indexed_accounts:
        if name in account['names']:
            return account['index']

    # if we can't find the account, return False
    return False

def save_account(account: dict):
    save_yn = input("Would you like to save this login? [y/n] ")
    if save_yn == "y" or save_yn == "Y":
        ACCOUNTS.append(account)

def select_account():
    # priority:
    #   1. use commandline arg
    #       --> prompt for password if account not found, offer to save
    #   2. use saved accounts

    # if there is a username/nickname specified via commandline argument, and account is in the config
    if len(sys.argv) > 1 and get_account_index(sys.argv[1]) is not False:
        return ACCOUNTS[get_account_index(sys.argv[1])]
    # if there is a username/nickname specified via commandline argument, and account is NOT in the config
    elif len(sys.argv) > 1 and get_account_index(sys.argv[1]) is False:
        new_account = {'username': sys.argv[1], 'password': getpass()}
        save_account(new_account)
        return new_account
    # if there is only 1 account in the config
    elif len(ACCOUNTS) == 1:
        print(f"Only 1 account found; Using {get_nickname(ACCOUNTS[0])}")
        return ACCOUNTS[0]
    # else if there are no accounts in the config
    elif not len(ACCOUNTS):
        print("No accounts found. Please specify an account.")
        new_account = {'username': input("Username: "), 'password': getpass()}
        save_account(new_account)
        return new_account
    else:
        # else, if no account was specified, prompt the user to pick:
        while True:
            print("Available accounts:")
            for index, acc in enumerate(ACCOUNTS):
                print(f"    [ {index} ] {get_nickname(acc)}")
            account_index = int(input('Which account? '))

            if account <= len(ACCOUNTS) and account >= 0:
                return ACCOUNTS[account_index]
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
        print(f"Currently waiting in queue... Position: {r['position']}, ETA: {r['eta']} seconds")
        time.sleep(1)
        r = requests.post(URL, data={'queueToken': queueToken}).json()
        if r['success'] == "true":
            return r
        time.sleep(29)


def login(account):
    r = requests.post(URL, data={'username': account['username'], 'password': account['password']}).json()

    if r['success'] == "false":
        die("Unable to login: {}".format(r['banner']))
    elif r['success'] == "partial":
        r = finish_partial_auth(r)

    if r['success'] == "delayed":
        r = finish_queue(r)

    if r['success'] == "true":
        launch_game(r)
    else:
        die('Somehow we got here, not sure how ...')

def launch_game(tokens: dict):
    print("Putting you in the game....")
    os.environ['TTR_GAMESERVER'] = tokens['gameserver']
    os.environ['TTR_PLAYCOOKIE'] = tokens['cookie']
    os.environ['DYLD_LIBRARY_PATH'] = DYLD_LIBRARY_PATH
    os.environ['DYLD_FRAMEWORK_PATH'] = DYLD_FRAMEWORK_PATH
    subprocess.run([GAME], cwd=os.path.dirname(GAME), stdout=subprocess.PIPE)
    exit(0)

def get_updates():
    file_manifest = requests.get('https://cdn.toontownrewritten.com/content/patchmanifest.txt').json()

    for filename, file in file_manifest.items():
        # if the file is needed for your system and the hashes don't match
        if system in file['only'] && get_hash(GAME_DIR + filename) != file['hash']:
            print(f"Update found for {filename}. Downloading....")
            update_file(filename, file)
        else:
            print(f"{filename} is already up to date.")

    print("All updates finished.")


def update_file(filename: str, file: dict):
    archive = requests.get(f"https://cdn.toontownrewritten.com/content/{file['dl']}").content
    with open(GAME_DIR + filename, 'w+') as outfile:
        outfile.write(bz2.decompress(archive))
    if get_hash(GAME_DIR + filename) != file['hash']:
        print("Integrity check failed. Redownloading....")
        update_file(filename, file)
    else:
        print(f"{filename} was successfully updated.")
        return True



account = select_account()
# save config
json.dump(ACCOUNTS, open(CONFIG_DIRECTORY + 'config.json', 'w+'))
login(account)

