# Bloodhound Collector Analysis Scripts
Reads JSON files and Neo4J data from [BloodHound Collector](https://github.com/BloodHoundAD) and prints data to the terminal. This can be useful for quickly identifying high value targets. Use these lists for password spraying, phishing, or anything your imagination can come up with against your target client (if it's in scope!). This project is a work-in-progress but I will only push updates when I have tested each new update or script to ensure a deliverable. 
## Scripts
### Bulk Update Owned Users
[This script](https://github.com/RackunSec/bloodhound-analysis-scripts/blob/main/bulk_update_owned_users.py) takes a file of users, [cmedb](https://github.com/byt3bl33d3r/CrackMapExec) export (CSV or line by line file from [Hashcat](https://hashcat.net/hashcat/) output, etc), and updates their record in the Neo4J BloodHound database as "owned." 
Let's say you got a lot of creds during the external phase of the penetration test from pihshing and password spraying. You get access to the internal network and use BloodHound collector(s) to pull data from the domain controller with the creds you have. Often times, your next step is to start doing research on those creds to find the quickest path to the domain admins group. Before I made this script, I had to search each one in BloodHound and right click and "Mark as owned". Well, this script makes this job quick and painless by doing that all at once and going straight to the source. The BloodHound UI will be updated immediately (well, you may have to re-search for the current user you have open).
#### Usage
1. Edit the scripe to have your Neo4J username and password. Then set your Neo4J hostname. 
2. Run the script with the following arguments
   1. What type of file is it? CrackMapExec database export, or line by line list of usernames?
   2. What domain should the script filter on?
   3. The export file/file name
   4. The path to your users.json file that BloodHound collectors create.
```bash
root@demon:~# python3 import_pwn3d.py (cmedb|file) (filter domain) (export file) (path to users.json)")
```
