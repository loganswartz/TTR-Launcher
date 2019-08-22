#!/usr/bin/env python3

# builtins
from pathlib import Path
import json
from getpass import getpass


class Config_Handler(object):

    def __init__(self, config_dir: lambda config_dir: Path(config_dir)):  # convert incoming variable to pathlib Path object
        self.config_dir = config_dir
        self.config_file = config_dir / 'config.json'
        self.config_ex = config_dir / 'config.json.example'

        if not self.config_dir.exists():
            create_config()
        self.account_list = json.load(self.config_file.open())


    def create_config(self):
        self.config_dir.mkdir()
        json.dump([], self.config_file.open(mode='w'))
        json.dump([{'username': '', 'password':'', 'nickname':''}], self.config_ex.open(mode='w'))


    def save_config(self):
        json.dump(self.account_list, self.config_file.open(mode='w+'))


    def get_nickname(self, account):
        if 'nickname' in account:
            return f"{account['nickname']} ({account['username']})"
        else:
            return account['username']


    def get_account_index(self, name: str):
        indexed_accounts = []
        for index, account in enumerate(self.account_list):
            if 'nickname' in account:
                indexed_accounts.append({'names': [account['username'], account['nickname']], 'index': index})
            else:
                indexed_accounts.append({'names': [account['username']], 'index': index})

        # find the first account with the given username/nickname
        for account in indexed_accounts:
            if name in account['names']:
                return account['index']

        # if we can't find the account, return False
        return False


    def add_account(self, account: dict):
        save_yn = input("Would you like to save this login? [y/n] ")
        if save_yn == "y" or save_yn == "Y":
            self.account_list.append(account)
        self.save_config()


    def select_account(self, cmd_args):
        # priority:
        #   1. use commandline arg
        #       --> prompt for password if account not found, offer to save
        #   2. use saved accounts

        # if there is a username/nickname specified via commandline argument, and account is in the config
        if len(cmd_args) > 1 and self.get_account_index(cmd_args[1], self.account_list) is not False:
            return self.account_list[self.get_account_index(cmd_args[1])]
        # if there is a username/nickname specified via commandline argument, and account is NOT in the config
        elif len(cmd_args) > 1 and self.get_account_index(cmd_args[1]) is False:
            new_account = {'username': cmd_args[1], 'password': getpass()}
            self.add_account(new_account)
            return new_account
        # if there is only 1 account in the config
        elif len(self.account_list) == 1:
            print(f"Only 1 account found; Using {self.get_nickname(self.account_list[0])}")
            return self.account_list[0]
        # else if there are no accounts in the config
        elif not len(self.account_list):
            print("No accounts found. Please specify an account.")
            new_account = {'username': input("Username: "), 'password': getpass()}
            self.add_account(new_account)
            return new_account
        else:
            # else, if no account was specified, prompt the user to pick:
            while True:
                print("Available accounts:")
                for index, acc in enumerate(self.account_list):
                    print(f"    [ {index} ] {self.get_nickname(acc)}")
                account_index = int(input('Which account? '))

                if account <= len(self.account_list) and account >= 0:
                    return self.account_list[account_index]
                else:
                    print("Invalid account, try again.")

