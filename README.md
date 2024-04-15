There was a project in my workplace to create a specific python script which use a database file (spam_organisations.csv) includes Spam Organisations url addresses for check and their status codes. 
Script make a check for every ip address from added networks: dig +short reverseip.spamorganisationname.com - if return status code match with discribed in database file IP address will be match as listed, if the status code does not match with codes in database files status will be OK, if there is no returning status code status again is OK, if there is a problem with check -- status code will be Unexpected error.
The scropt use multi workers/threads at same time.

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
