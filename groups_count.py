#!/usr/bin/env python3
# 2021 Douglas Berdeaux
# This script reads BloodHound-Collector users.json file and prints total number of groups defined
#
# Usage: python3 groups_count.py groups.json
#
import json
import sys
if len(sys.argv) != 2:
        print("[i] Usage: python3 groups_count.py groups.json")
        sys.exit(1)
else:
        with open(sys.argv[1]) as file_contents:
                json_groups = file_contents.read()
                json_dict = json.loads(json_groups)
                print(json_dict['meta']['count'])
