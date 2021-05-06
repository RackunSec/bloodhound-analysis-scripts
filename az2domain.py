#!/usr/bin/env python3
# This script will "convert" azurehound collector output to domain-friendly output for queries within the BloodHound interface
# The idea for this script came out of raw testing in the wild - we were ghetting SID-like names for everything. We had
#   trouble querying that type of data, so I vuilt this script to run. It will update all nodes witin the labels defined below
#   (in the "whats" list) and add a "name" attribute with the same valueas the azname attrbiute. BlodHound will show the chnages
#   immediately when you query a device, user or group.
#
from neo4j import GraphDatabase # to query database
import sys # for argv and exit
import os # for error handling
# Color:
bcolors = {
	'OKGREEN' : '\033[3m\033[92m ✔ \033[0m',
	'GREEN' : '\033[92m',
	'FAIL' : '\033[3m\033[91m ✖ ',
	'ENDC' : '\033[0m',
	'WARN': '\033[33m  ',
}
## Versioning:
version="0.5.06.2"
## What's up? (These are the labels that we will SET with a working domain-friendly "name")
whats = ["Group","User","AZDevice","AZGroup","AZApp"] # <-- I need to fill this out more!
## UPDATE THE VALUES IN SECTION BELOW:
db_user = "neo4j" # Neo4J Username
db_passwd = "neo4jPassword" # Neo4J Password
db_server_address = "bolt://127.0.0.1:7687" # Neo4J URI
#############################
if db_user=="" or db_passwd=="":
    print(f"{bcolors['FAIL']}{bcolors['ENDC']} Please set your {bcolors['GREEN']}db_user{bcolors['ENDC']} and {bcolors['GREEN']}db_passwd{bcolors['ENDC']} in this file and try again.{bcolors['ENDC']}")
    sys.exit(1337)
else:
    print(f"\n{bcolors['WARN']} This script will query the Neo4J database located @ {db_server_address}")
    print(f"{bcolors['WARN']}   and will update every node to have a new attribute labeled \"name\"{bcolors['ENDC']}")
    ans=input("\n[?] Shall we continue (y/n)? ")
    if ans == "y":
        class Neo4JQuery:
            def __init__(self, uri, user, password):
            	self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

            def close(self):
            	self.driver.close()

            def query(self, what, db=None):
                assert self.driver is not None, "Driver not initialized!"
                session = None
                response = None
                full_query = "match n=(a:"+what+") foreach (m in nodes(n) | SET m.name = m.azname)" # debug
                try:
                    print(f"{bcolors['OKGREEN']}{bcolors['ENDC']} Querying: {full_query}") # DEBUG
                    session = self.driver.session(database=db) if db is not None else self.driver.session()
                    response = list(session.run(full_query))
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(f"{bcolors['FAIL']} Query failed: ", e)
                finally:
                    if session is not None:
                        session.close()
                return response
        print("")
        for what in whats:
            # Instatiate object:
            try:
                query_obj = Neo4JQuery(db_server_address, db_user, db_passwd)
                query_obj.query(what)
                query_obj.close()
            except Exception as e:
                print(f"{bcolors['WARN']} Issue with query: {what}: {e} {bcolors['ENDC']}")
                if "authentication details too many times in a row" in str(e):
                    print(f"{bcolors['FAIL']} Please ensure that you have set your password correctly. You may have been locked out.\n")
                    sys.exit(1)
                elif "authentication failure" in str(e):
                    print(f"{bcolors['FAIL']} Please ensure that you have set your password correctly.\n")
                    sys.exit(1)
                elif "ailed to establish connection" in str(e):
                    print(f"{bcolors['FAIL']} Cannot connect to Neo4J Server at {db_server_address}\n Ensure that the service is running on that host before continuing.{bcolors['ENDC']}")
                    sys.exit(1)
                else:
                    print(f"{bcolors['FAIL']}[?]{bcolors['ENDC']} What went wrong?")
                    sys.exit(1)
    else:
        sys.exit(1338)
print(f"{bcolors['OKGREEN']}{bcolors['ENDC']} Script completed.\n")
