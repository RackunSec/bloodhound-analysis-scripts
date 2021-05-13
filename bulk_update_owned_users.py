#!/usr/bin/env python3
# (c) GNU 2021 RackunSec
#
# Import exported creds from CME (as CSV) directly into Neo4j
#
# This will update the BloodHound UI immediately.
# It reads the CSV file, pulls out all users defined by your domain filter
#  And reads users.json file to get full name
#  Then, queries Neo4j to update that user as "owned"
#
import csv # for exported cmedb file
from neo4j import GraphDatabase # to query database
import sys # for argv and exit
import json # for users.json file
import re # for matching usernames from cmedb to actual DC data
import os # for errors
import codecs # for Windows-specific BloodHound Collector's JSON files.
#
# Color:
bcolors = {
    'YELL' : '\033[33m',
	'OKGREEN' : '\033[3m\033[92m ✔ \033[0m',
	'GREEN' : '\033[92m',
	'FAIL' : '\033[3m\033[91m ✖ ',
	'ENDC' : '\033[0m',
	'WARN': '\033[33m  ',
	'INFO': '[i]'
}
version="0.4.19.2"
query_count = 0 # stupid globals
db_user = "" # Neo4J Username
db_passwd = "" # Neo4J Password
db_server_address = "bolt://127.0.0.1:7687" # Neo4J URI
# Check arguments:
def usage(error):
	print(f"[i] Error: {error}")
	print("[i] Usage: python3 import_pwn3d.py (cmedb|file) (filter domain) (export file) (path to users.json)")
	sys.exit(1)
if len(sys.argv)!= 5:
	usage("Not enough arguments")
elif sys.argv[1] != "cmedb" and sys.argv[1] != "file":
	usage(f"Unknown file type: {sys.argv[1]}")
else:
    class BloodHoundUpdate:
    	def __init__(self, uri, user, password):
    		self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False) # fix for update to neo4j modules

    	def close(self):
    		self.driver.close()

    	def query(self, user, db=None):
    		print(f"{bcolors['OKGREEN']} Updating user: {user}")
    		assert self.driver is not None, "Driver not initialized!"
    		session = None
    		response = None
    		full_query = "MATCH (n) WHERE (n.name = \""+user+"\") SET n.owned = true" # debug
    		#print(f"full_query]: {full_query}") # debug
    		try:
    			session = self.driver.session(database=db)  if db is not None else self.driver.session()
    			response = list(session.run(full_query))
    		except Exception as e:
    			exc_type, exc_obj, exc_tb = sys.exc_info()
    			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    			print(exc_type, fname, exc_tb.tb_lineno)
    			print("{bcolors['FAIL']} Query failed: ", e)
    		finally:
    			if session is not None:
    				session.close()
    		return response

    if sys.argv[1] == "cmedb":
        print(f"\n{bcolors['OKGREEN']} Using export {bcolors['GREEN']}cmedb CSV file{bcolors['ENDC']}: {bcolors['GREEN']}{sys.argv[3]}{bcolors['ENDC']}.")
        print(f"{bcolors['OKGREEN']} Importing {bcolors['YELL']}pwn3d{bcolors['ENDC']} users from {bcolors['GREEN']}cmedb {bcolors['ENDC']}export.")
        print(f"{bcolors['OKGREEN']} Filtering domain: {bcolors['GREEN']}{sys.argv[2]}{bcolors['ENDC']}.\n")
        with open(sys.argv[3]) as cmedb_csv:
            csv_reader = csv.reader(cmedb_csv, delimiter=',')
            try:
                for row in csv_reader:
                    if row[2] == "":
                        continue
                    if (row[1].lower() == sys.argv[2].lower()) and not "$" in row[2]:
                    	# open users.json and get actual username for SID:
                        update_user = "" # define this.
                        with open(sys.argv[4]) as users_json:
                            json_users = users_json.read()
                            decoded_users=codecs.decode(json_users.encode(), 'utf-8-sig')
                            json_dict = json.loads(decoded_users)
                            for obj in json_dict['users']:
                                if re.match(f"^{row[2]}@".lower(),str(obj['Properties']['name']).lower()):
                                	update_user = obj['Properties']['name']
                                	break
                        if update_user == "":
                            print(f"{bcolors['WARN']} Could not find user: {row[2]} in file {sys.argv[4]} {bcolors['ENDC']}")
                            continue
                        else:
                            try:
                                query_obj = BloodHoundUpdate(db_server_address, db_user, db_passwd)
                                query_obj.query(update_user)
                                query_obj.close()
                                query_count += 1
                            except Exception as e:
                                print(f"{bcolors['WARN']} Issue with query: {update_user}: {e} {bcolors['ENDC']}")
                                if "authentication details too many times in a row" in str(e):
                                    print(f"{bcolors['FAIL']} Please ensure that you have set your password correctly. You may have been locked out.\n")
                                    sys.exit(1)
                                elif "authentication failure" in str(e):
                                    print(f"{bcolors['FAIL']} Please ensure that you have set your password correctly.\n")
                                    sys.exit(1)
                                elif "ailed to establish connection" in str(e):
                                    print(f"{bcolors['FAIL']} Cannot connect to Neo4J Server at {db_server_address}\n")
                                    sys.exit(1)
                                else:
                                    print(f"{bcolor['FAIL']} What happened?")
                                    sys.exit(1)
            #except Exception as e: # debug
            except Exception as e:
                print(e) # debug
                print(f"{bcolors['FAIL']} file contains invalid characters.  {bcolors['ENDC']}\nTry cleaning the file with \"cat {sys.argv[3]}|tr -cd '\\11\\12\\15\\40-\\176' > {sys.argv[3]}-clean.csv \" before running again.")
                print(f"{bcolors['FAIL']} FAILED to read {sys.argv[3]} {bcolors['ENDC']}\n")
    elif sys.argv[1] == "file":
        print(f"\n{bcolors['OKGREEN']} Using file {bcolors['GREEN']}line by line file{bcolors['ENDC']}: {bcolors['GREEN']}{sys.argv[3]}{bcolors['ENDC']}.")
        print(f"{bcolors['OKGREEN']} Using fqdn domain: {bcolors['GREEN']}{sys.argv[2]}{bcolors['ENDC']}.\n")
        with open(sys.argv[3]) as all_users:
            for user in all_users:
                if user == "": continue
                update_user = "" # define this
                try:
                    user = user.rstrip() # drop newline
                    with open(sys.argv[4]) as users_json:
                        json_users = users_json.read()
                        json_dict = json.loads(json_users)
                        for obj in json_dict['users']:
                            if re.match(f"^{user}@".lower(),str(obj['Properties']['name']).lower()):
                                update_user = obj['Properties']['name']
                                break
                    if update_user == "":
                        print(f"{bcolors['WARN']} Could not find user: {user} in file {sys.argv[4]} {bcolors['ENDC']}")
                        continue
                    query_obj = BloodHoundUpdate(db_server_address, db_user, db_passwd)
                    query_obj.query(update_user)
                    query_obj.close()
                    query_count += 1
                except Exception as e:
                    print(f"{bcolors['WARN']} Issue with query: {update_user}: {e} {bcolors['ENDC']}")
                    if "authentication details too many times in a row" in str(e):
                        print(f"{bcolors['FAIL']} Please ensure that you have set your password correctly. You may have been locked out.\n")
                        sys.exit(1)
                    elif "authentication failure" in str(e):
                        print(f"{bcolors['FAIL']} Please ensure that you have set your password correctly.\n")
                        sys.exit(1)
                    elif "ailed to establish connection":
                        print(f"{bcolors['FAIL']} Cannot connect to Neo4J Server at {db_server_address}\n Ensure that the service is running on that host before continuing.{bcolors['ENDC']}")
                        sys.exit(1)

print(f"\n{bcolors['OKGREEN']} Completed. {bcolors['GREEN']}{query_count}{bcolors['ENDC']} records updated to \"owned\".\n ")
