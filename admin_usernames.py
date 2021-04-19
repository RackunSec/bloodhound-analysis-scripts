#!/usr/bin/env python3
# 2021 Douglas Berdeaux
# This script reads BloodHound-Collector users.json file and prints list of users with "admin" in name
import json
import sys
if len(sys.argv)!=2:
        print(len(sys.argv))
        print("[i]) Usage: python3 admin_users.py users.json")
else:
        print("[i] Searching for admin usernames ... ")
        with open(sys.argv[1]) as file_contents:
                json_users = file_contents.read()
                json_dict = json.loads(json_users)
                for obj in json_dict['users']:
                        if "admin" in str(obj['Properties']['name']).lower():
                                print(obj['Properties']['name'])

