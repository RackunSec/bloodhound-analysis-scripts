#!/usr/bin/env python3
# 2021 Douglas Berdeaux
# This script reads BloodHound-Azure-Collector azusers.json file and prints list of users.
import json # for readinf JSON objects
import sys # for exit and argv
import os.path as path # for checking if file exists
import codecs # for Windows-specific BloodHound Collector's JSON files.
def usage(error):
    print(f"[!] Error: {error}")
    sys.exit(1)

if len(sys.argv)!=2:
    usage("Not enough arguments.")
else:
    users_file = sys.argv[1]
    if path.exists(users_file):
        with open(users_file) as file_contents:
            json_users = file_contents.read()
            decoded_users=codecs.decode(json_users.encode(), 'utf-8-sig')
            json_dict = json.loads(decoded_users)
            for obj in json_dict['data']:
                print(obj['UserPrincipalName'])
    else:
        usage(f"Could not find file {sys.argv[1]}")
