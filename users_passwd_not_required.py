#!/usr/bin/env python3
# 2021 Douglas Berdeaux
# This script reads BloodHound-Collector users.json file and prints list of users.
import json
print("[i] Checking for users who don't require a password ... ")
with open('users.json') as file_contents:
	json_users = file_contents.read()
	json_dict = json.loads(json_users)
	for obj in json_dict['users']:
		if str(obj['Properties']['passwordnotreqd']) != "False":
			print(obj['Properties']['name']+":"+str(obj['Properties']['passwordnotreqd']))
	
