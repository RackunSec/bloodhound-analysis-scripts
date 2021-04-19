#!/usr/bin/env python3
# 2021 Douglas Berdeaux
# This script reads BloodHound-Collector users.json file and prints total number of users defined
#
# Usage: python3 users_count.py users.json
#
import json
import sys
if len(sys.argv) != 2:
        print("[i] Usage: python3 users_count.py users.json")
        sys.exit(1)
else:
        with open(sys.argv[1]) as file_contents:
                json_users = file_contents.read()
                json_dict = json.loads(json_users)
                print(json_dict['meta']['count'])

