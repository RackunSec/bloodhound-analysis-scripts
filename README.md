# Bloodhound Collector Analysis Scripts
Reads JSON files and Neo4J data from [BloodHound Collector](https://github.com/BloodHoundAD) and prints data to the terminal. This can be useful for quickly identifying high value targets. Use these lists for password spraying, phishing, or anything your imagination can come up with against your target client (if it's in scope!). This project is a work-in-progress but I will only push updates when I have tested each new update or script to ensure a deliverable. 
## Scripts
Below we will cover a few of the *most used* scripts in this library. If you'd like to see new functionality, please fee free to send me an email with your idea.

---
### SCRIPT: Bulk Update Owned Users
[This script](https://github.com/RackunSec/bloodhound-analysis-scripts/blob/main/bulk_update_owned_users.py) takes a file of users, [cmedb](https://github.com/byt3bl33d3r/CrackMapExec) export (CSV or line by line file from [Hashcat](https://hashcat.net/hashcat/) output, etc), and updates their record in the Neo4J BloodHound database as "owned." 

Let's say you got a lot of creds during the external phase of the penetration test from pihshing and password spraying. You get access to the internal network and use BloodHound collector(s) to pull data from the domain controller with the creds you have. Often times, your next step is to start doing research on those creds to find the quickest path to the domain admins group. Before I made this script, I had to search each one in BloodHound and right click and "Mark as owned". Well, this script makes this job quick and painless by doing that all at once and going straight to the source. The BloodHound UI will be updated immediately (well, you may have to re-search for the current user you have open).

Each username is verified in the users.json file using regexp before making the Neo4J database connection and query. 
***Usage:***

1. Edit the scripe to have your Neo4J username and password. Then set your Neo4J hostname. 
2. Run the script with the following arguments
   1. What type of file is it? CrackMapExec database export, or line by line list of usernames?
   2. What domain should the script filter on?
   3. The export file/file name
   4. The path to your users.json file that BloodHound collectors create.
```bash
root@demon:~# python3 bulk_update_owned_users.py ("cmedb"|"file") (filter domain) (export file) (path to users.json)
```
***CMEDB Dump Example:***
```bash
root@demon:~# python3 bulk_update_owned_users.py cmedb prison exported-creds.csv path/to/users.json

 ✔  Using export cmedb CSV file: exported-creds.csv.
 ✔  Importing pwn3d users from cmedb export.
 ✔  Filtering domain: prison.

 ✔  Updating user: username1@prison.local
   Could not find user: bad_username in file path/to/users.json 
 ✔  Updating user: username2@prison.local
 ✔  Updating user: username3@prison.local
 ✔  Updating user: username4@prison.local
 ✔  Updating user: username5@prison.local
 ✔  Updating user: username6@prison.local
 ✔  Updating user: username7@prison.local
 ✔  Updating user: username8@prison.local
 ✔  Updating user: username9@prison.local
 ✔  Updating user: username10@prison.local
 ✔  Updating user: username11@prison.local

 ✔  Completed. 11 records updated to "owned".
 
root@demon:~# 
```
***FILE Dump Example:***
```bash
root@demon:~# python3 bulk_update_owned_users.py file prison.local exported-creds.csv path/to/users.json

 ✔  Using export file: exported-creds.csv.
 ✔  Importing pwn3d users from file.
 ✔  Filtering domain: prison.local

 ✔  Updating user: username1@prison.local
   Could not find user: bad_username in file path/to/users.json 
 ✔  Updating user: username2@prison.local
 ✔  Updating user: username3@prison.local
 ✔  Updating user: username4@prison.local
 ✔  Updating user: username5@prison.local
 ✔  Updating user: username6@prison.local
 ✔  Updating user: username7@prison.local
 ✔  Updating user: username8@prison.local
 ✔  Updating user: username9@prison.local
 ✔  Updating user: username10@prison.local
 ✔  Updating user: username11@prison.local

 ✔  Completed. 11 records updated to "owned".
 
root@demon:~# 
```
***Troubleshooting:***

Sometimes the exported files will contain bad characters. When this happens, my script will tell you how to fix the file using Linux:
```bash
root@demon:~# python3 import_pwn3d.py cmedb prison exported-creds.csv path/to/users.json

 ✔  Using export cmedb CSV file: exported-creds-bad-chars.csv.
 ✔  Importing pwn3d users from cmedb export.
 ✔  Filtering domain: prison.

 ✔  Updating user: username1@prison.local
 ✔  Updating user: username2@prison.local
 ✔  Updating user: username3@prison.local
line contains NUL
 ✖  file contains invalid characters.  
Try cleaning the file with "cat exported-creds-bad-chars.csv|tr -cd '\11\12\15\40-\176' > exported-creds-bad-chars.csv-clean.csv " before running again.
 ✖  FAILED to read exported-creds-bad-chars.csv 
 
 ✔  Completed. 3 records updated to "owned".
 
 root@demon:~# 
```
---
### SCRIPT: Search All Users for "admin" in their Name
Ever wanted to quickly target any account that had say,
 * "-admin";
 * "admin"; or
 * "administrator"

In the name? Use [this script](https://github.com/RackunSec/bloodhound-analysis-scripts/blob/main/admin_usernames.py) to do just that. You simply pass it the users.json file that BloodHound Collectors create and it will parse out the JSON using Python magic.

***Usage:***
```bash
root@demon:~# python3 admin_usernames.py | tee -s admin-users.txt
```
---
### SCRIPT: Quickly List All Domain Admins
Use [this script](https://github.com/RackunSec/bloodhound-analysis-scripts/blob/main/domain_admins.py) to quickly list out all of the domain adminsdiscovered by the BloodHound Collector, from the command line.

***Usage:***
```bash
root@demon:~# python3 domain_admins.py | tee -a domain-admins.txt
```
