There was a project in my workplace to create a specific python script which use a database file (spam_organisations.csv) includes Spam Organisations url addresses for check and their status codes. 
Script make a check for every ip address from added networks: dig +short reverseip.spamorganisationname.com - if return status code match with discribed in database file IP address will be match as listed, if the status code does not match with codes in database file status will be OK, if there is no returning status code status again is OK, if there is a problem with check -- status code will be Unexpected error.
The script use multi workers/threads at same time.

Requirements to use script:

1. Install python on your device.
2. Upload both files:bl-final.py and spam_organisations.csv in same directory.
3. Before start the script you need to edit bl-final.py:
   - row 13: "timeout=3"  #waiting time for response from spam organisation - can put big number if you have problem with you Internet service (higher number if you have higher ping or package loose).
   - row 33: "max_workers=100" set number of simultaneously proccess at same time - by default is 100.If you have perfect internet connection and you have more than 8 Cores you can change to bigger number (Script use mostly CPU).
   - row 47: you neeed to add for check your networks (there is no limitations of theirs count)
   - row 48: you need to add output files for every network you`ll be checking Example if you check two networks you need to add two files:"blacklisted_ips_network1.csv", "blacklisted_ips_network2.
   - row 72: here you need to place email account/s where reports w`ll be send.
   - row 76: here you need to fill email account from which script w`ll send reports.  (SMTP:username)
   - row 77: here you need to fill the password for email from which script w`ll send reports. (SMTP:password)
   - row 96: here you need to change example.com with your SMTP server.
4. FInaly you can start the script with following command: $ python3 bl-final.py.

Some people ask me about add Abusix in Spam Organisations list:

combined.mail.abusix.zone,"127.0.0.2,127.0.0.3,127.0.0.4,127.0.0.11,127.0.0.12,127.0.0.200"
dblack.mail.abusix.zone,"127.0.1.1,127.0.1.2,127.0.1.3"

But thats not all, you need to create a free account at: https://abusix.com/ and authorise your networks, than you`ll get your API key. Than you can add in  spam_organisations.csv abusix like that:

yourAPIkey.combined.mail.abusix.zone,"127.0.0.2,127.0.0.3,127.0.0.4,127.0.0.11,127.0.0.12,127.0.0.200"
yourAPIkey.dblack.mail.abusix.zone,"127.0.1.1,127.0.1.2,127.0.1.3"

Abusix offers 6 url address for check for problems, but "combined.mail.abusix.zone" united 4 of them, for that reason we need to use only 2 links for check.
