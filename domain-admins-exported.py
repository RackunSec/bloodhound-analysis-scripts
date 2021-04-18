#!/usr/bin/env python3
# 2021 Douglas Berdeaux
# Export the domain admins with BloodHound as JSON and feed it to this script.
import json
import sys
if len(sys.argv) == 1:
	print("[i] You must pass an exported list of domain admins as JSON to me.")
else:
	with open(sys.argv[1]) as json_file:
		full_json = json_file.read()
		json_dict = json.loads(full_json)
		for node in json_dict['nodes']:
			if node['type'] == "User":
				print(node['props']['name'])
		
