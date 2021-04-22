# Mock-ATM-Project
This is a mock project that mimicks the performance of an Automated Teller Machine (ATM). 
In its current iteration, though, it works more like a mock online banking app.
The program launches unto a home page that allows the user create a new account or login to an existing one. 

## Create account
To create a new account, a user must provide their first and last names, and a valid email address and password, 
after which a unique 10-digit account number is generated. The generated account number must begin with '0' and must not match any other existing account numbers.
Email addresses are checked to match the pattern: name@website.domain or name@subdomain.website.domain. 
Likewise, passwords must be at least 5 characters in length to be approved.

## Login
To login to an existing account, user's would need their unique account number and password. For security reasons, the program exits after 5 incorrect password attempts.
Once login is confirmed, the user would be able to carry out any of a number of activities, including:
+ Withdrawing a specified amount
+ Depositing a specified amount
+ Checking account balance
+ Lodging a complaint
+ Changing password

## Latest Improvements
+ Users can no longer be allowed to open multiple accounts using the same email address. As part of the account creation process, any email addresses already existing in the system is flagged, and account creation blocked. 
+ User profiles are now stored permanently in a local directory. This means a user's info isn't lost at the end of a program's running cycle.

## Expected further improvements
+ Write directly to a SQL database rather than a local directory.
+ Improve expected password difficulty using regular expression
+ Build a complaint's database for each user
+ Keep a log of each user's activity.
