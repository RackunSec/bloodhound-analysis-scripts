#!/usr/bin/env python3
# 2021 Douglas Berdeaux
# This script reads BloodHound-Collector users.json file and prints list of Domain Admins
# 
# Usage: python3 da-users.py groups.json users.json
#
import json
import sys
import re
if len(sys.argv) < 3:
        print("[i] You must pass \"groups.json\" and \"users.json\" files as an arguments.")
else:
        with open(sys.argv[1]) as json_file:
                full_json = json_file.read()
                json_dict = json.loads(full_json)
                for node in json_dict['groups']:
                        if re.match("^(DOMAIN|ENTERPRISE)(\s+)?ADMINS",node['Properties']['name']):
                                print(f"\n[i] {node['Properties']['name']} members: ")
                                for sid in node['Members']:
                                        with open(sys.argv[2]) as users_json_file:
                                                json_users = users_json_file.read()
                                                user_json_dict = json.loads(json_users)
                                                for user in user_json_dict['users']:
                                                        if user['ObjectIdentifier'] == sid['MemberId']:
                                                                print(user['Properties']['name'])
