#!/usr/bin/env python3
# 2021 Douglas Berdeaux
# This script reads BloodHound-Collector users.json file and prints list of users.
import json
with open('users.json') as file_contents:
	json_users = file_contents.read()
	json_dict = json.loads(json_users)
	for obj in json_dict['users']:
		if len(obj['Aces']) > 0:
			print(obj['Properties']['name'])
	
