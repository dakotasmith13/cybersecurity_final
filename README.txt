Dakota Smith
CS 166 Final Project

This program emulates CashCab's secret safe, from the world renowned TV show, Cash Cab. A user is prompted
to log in or create an account, and then is presented with a menu of items. If the user has the correct permissions, they will 
be able to access certain menu items. 

TO RUN: 
Navigate to werk.py and click the green play button to run the program. Click on the localhost link to bring you to the login screen.
You can either log in with credentials provided below, or click create an account below, and enter a username and password of your 
choosing, and then sign in using those credentials. If you have incorrectly entered in a password 3 times you will be locked out.
The database has already been created with users of 3 access levels: 
user (least privilege, no accounting or engineering), accounting (access to everything but engineering), and engineering (access to everything but accounting). 
User logins:
Username    Password    Access Level 
dakota	    Password123!   user
accounting  Password123!   accounting
engineering Password123!   engineering

Once logged in, you can select a menu item, and will either be brought to that page, or told that you do not have access. From there, you
can either return to the home page, or log out to return to the log in screen.
